const axios = require('axios');
const FormData = require('form-data');

async function analyzeImageWithAI(fileBuffer, filename, mimetype) {
  const form = new FormData();
  form.append('image', fileBuffer, {
    filename,
    contentType: mimetype
  });

  const { data } = await axios.post(`${process.env.AI_SERVICE_URL}/analyze`, form, {
    headers: form.getHeaders(),
    timeout: Number(process.env.AI_SERVICE_TIMEOUT_MS || 10000)
  });

  return data;
}

module.exports = analyzeImageWithAI;
