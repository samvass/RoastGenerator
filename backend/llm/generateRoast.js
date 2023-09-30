// server.js
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3001;

app.use(bodyParser.json());

// Define a route to handle requests from your React app
app.post('/generate-text', async (req, res) => {
  try {
    const { prompt } = req.body;

    // Replace 'YOUR_API_KEY' with your OpenAI API key
    const apiKey = 'YOUR_API_KEY';
    const apiUrl = 'https://api.openai.com/v1/engines/davinci-codex/completions'; // Adjust the engine and endpoint as needed

    const response = await axios.post(apiUrl, {
      prompt,
      max_tokens: 150, // Adjust based on your requirements
    }, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    res.json({ data: response.data.choices[0].text });
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
