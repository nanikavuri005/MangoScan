require('dotenv').config();
const connectDB = require('./config/db');
const createApp = require('./app');

const requiredEnvVars = ['MONGO_URI', 'JWT_SECRET', 'AI_SERVICE_URL'];
const missing = requiredEnvVars.filter((name) => !process.env[name]);

if (missing.length > 0) {
  console.error(`Missing required environment variables: ${missing.join(', ')}`);
  process.exit(1);
}

const app = createApp();
const port = Number(process.env.PORT || 4000);

(async () => {
  await connectDB(process.env.MONGO_URI);
  app.listen(port, () => {
    console.log(`Backend running on port ${port}`);
  });
})();
