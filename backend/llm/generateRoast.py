from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import openai
import base64
import re
from PIL import Image
from io import BytesIO


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
CORS(app)

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

        return image

    else:
        raise ValueError("Invalid data URL format")

@app.route('/')
def test():
    return 'Hello, World!'


@app.route('/generate', methods=['POST'])
def generate_text():
    # Get the input data (list of human features) from the React app
    data = request.json

    # Construct the prompt for the language model
    prompt = "Generate a roast style joke of a human face with the following features in the second person:\n"
    for feature in data['features']:
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
    print("WORK")
    data = request.json['image']
    data_url_to_image(data)

    return "worked"

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

