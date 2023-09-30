from flask import Flask, request, jsonify
import os
import openai
import requests

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

@app.route('/')
def test():
    return 'Hello, World!'


@app.route('/generate', methods=['POST'])
def generate_text():
    # Get the input data (list of human features) from the React app
    data = request.json
    print(data)

    # Construct the prompt for the language model
    prompt = "Generate a roast style joke of a human face with the following features in the second person:\n"
    for feature in data['features']:
        prompt += f"- {feature}\n"

    # Call the OpenAI API to generate the description
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    # Return the response from the language model to the React app
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
