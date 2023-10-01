from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import openai
import base64
import re
from PIL import Image
from io import BytesIO
import sys
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import pandas as pd


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
CORS(app)

#input: numpy arr of predicted labels
def get_label_names(bin_label_tensor):
    df = pd.read_csv('../Model/attributes.csv')
    attr_arr = df.columns.values[1:]
    #print(attr_arr)
    attr_indices = torch.nonzero(bin_label_tensor == 1).tolist()
    attr_indices = [x[1] for x in attr_indices]
    print(attr_indices)
    predicted_attributes = [attr_arr[i] for i in attr_indices]
    print(predicted_attributes)
    return predicted_attributes

def pre_process_image(img_path):
    image = Image.open(img_path)

    transform = transforms.Compose([transforms.ToTensor()])
    image = transform(image)
    image = image.unsqueeze(0)
    return image

def data_url_to_image(data_url):
    # Parse the data URL using regular expressions
    match = re.match(r"data:(?P<type>.*?);base64,(?P<data>.*)", data_url)
    if match:
        image_type = match.group("type")
        image_data_base64 = match.group("data")

        # Decode the base64 image data
        image_data_binary = base64.b64decode(image_data_base64)

        # Create a PIL Image object from binary data
        image = Image.open(BytesIO(image_data_binary))

        save_path = "images/captured_image.jpg"
        image.save(save_path)

        return save_path

    else:
        raise ValueError("Invalid data URL format")

@app.route('/')
def test():
    return 'Hello, World!'


#@app.route('/generate', methods=['POST'])
def generate_text(features):
    # Get the input data (list of human features) from the React app

    # Construct the prompt for the language model
    prompt = "Generate a roast style joke of a human face with the following features in the second person:\n"
    for feature in features:
        prompt += f"- {feature}\n"

    # Call the OpenAI API to generate the description
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    # Return the response from the language model to the React app
    return response.choices[0].message.content

@app.route('/api/upload')
def work():
    return "Hello"

@app.route('/api/upload', methods=['POST'])
def upload_image():

    data = request.json['image']
    image_path = data_url_to_image(data)

    # open model
    model = torch.load('../Model/model.pth')

    model.eval()

    # pre process input image
    img = pre_process_image(image_path)

    with torch.no_grad():
        output = model(img).data
        output = torch.abs(output) / 10
        print(output)
        threshold = 0.8
        output_binary = torch.where(output >= threshold, torch.tensor(1), torch.tensor(0))
        
        print(output_binary)
        predicted_attributes = get_label_names(output_binary)
        output_text = generate_text(predicted_attributes)
        print(output_text)

        response_data = {
            "result": "success",
            "output_text": output_text
        }

        # Convert the response data to JSON and send it as the HTTP response
        return jsonify(response_data)

    # # Check if a file was provided in the request
    # if 'image' not in request.files:
    #     print("NOTWORK")
    #     return jsonify({'error': 'No image provided'}), 400

    # print("WORK2")
    # image = request.files['image']

    # # Check if the file has an allowed extension
    # if image and allowed_file(image.filename):
    #     print("WORK3")
    #     # Generate a unique filename for the image
    #     filename = str(uuid.uuid4()) + '.jpg'
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    #     # Save the image to the uploads folder
    #     image.save(filepath)

    #     # Return a success response with the filename or URL
    #     return jsonify({'message': 'Image uploaded successfully', 'filename': filename}), 200
    # else:
    #     return jsonify({'error': 'Invalid file format'}), 400


if __name__ == '__main__':
    app.run(debug=True)

