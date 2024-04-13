import express from 'express';
import axios from 'axios';
var bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.urlencoded({
  extended: false
}));
app.use(bodyParser.json());

app.post('/process-payload', async (req, res) => {
  const url = 'https://jerry-7x6r.onrender.com/route/';
  const payload = { query: req.body.query }

  try {
    const response = await axios.post(url, payload);
    console.log('Response from FastAPI server:', response.data);

    // Check if the response contains an 'answer' attribute
    if (response.data.answer) {
      console.log("Answer received from API");
      res.write(response.data.answer);
      res.end();
      return;
    }

    // If the response does not contain an 'answer' attribute, handle it accordingly
    console.log("No 'answer' attribute found in the response");
    res.status(500).send('Error: Invalid response format');
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Error: ' + error.message);
  }
});
