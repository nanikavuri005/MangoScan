const express = require('express');
const multer = require('multer');
const requireAuth = require('../middleware/auth');
const analyzeImageWithAI = require('../services/aiClient');
const Analysis = require('../models/Analysis');

const router = express.Router();

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: Number(process.env.MAX_IMAGE_SIZE_BYTES || 10 * 1024 * 1024)
  },
  fileFilter: (_req, file, cb) => {
    if (!file.mimetype || !file.mimetype.startsWith('image/')) {
      return cb(new Error('Only image files are allowed'));
    }
    cb(null, true);
  }
});

router.post('/', requireAuth, upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: 'image file is required (multipart form-data field: image)' });
    }

    const aiResult = await analyzeImageWithAI(req.file.buffer, req.file.originalname, req.file.mimetype);

    const analysis = await Analysis.create({
      userId: req.user.userId,
      filename: req.file.originalname,
      diagnosis: aiResult.diagnosis,
      confidence: aiResult.confidence,
      recommendedAction: aiResult.recommendedAction,
      modelVersion: aiResult.modelVersion || 'demo-v1'
    });

    return res.status(201).json({
      id: analysis._id,
      diagnosis: analysis.diagnosis,
      confidence: analysis.confidence,
      recommendedAction: analysis.recommendedAction,
      createdAt: analysis.createdAt
    });
  } catch (error) {
    return res.status(502).json({ message: 'Analysis failed', error: error.message });
  }
});

router.get('/', requireAuth, async (req, res) => {
  try {
    const analyses = await Analysis.find({ userId: req.user.userId }).sort({ createdAt: -1 }).lean();
    return res.json({ count: analyses.length, data: analyses });
  } catch (error) {
    return res.status(500).json({ message: 'Failed to list analyses', error: error.message });
  }
});

module.exports = router;
