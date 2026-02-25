require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const authRoutes = require('./routes/authRoutes');
const analyzeRoutes = require('./routes/analyzeRoutes');

const app = express();

app.use(cors());
app.use(express.json({ limit: '2mb' }));

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'mangoscan-backend' });
});

app.use('/api/auth', authRoutes);
app.use('/api/analyze', analyzeRoutes);

app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ message: 'Internal server error' });
});

const port = Number(process.env.PORT || 4000);

(async () => {
  await connectDB(process.env.MONGO_URI);
  app.listen(port, () => {
    console.log(`Backend running on port ${port}`);
  });
})();
