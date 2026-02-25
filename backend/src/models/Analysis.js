const mongoose = require('mongoose');

const analysisSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true
    },
    filename: {
      type: String,
      required: true
    },
    diagnosis: {
      type: String,
      required: true
    },
    confidence: {
      type: Number,
      required: true
    },
    recommendedAction: {
      type: String,
      required: true
    },
    modelVersion: {
      type: String,
      default: 'demo-v1'
    }
  },
  { timestamps: true }
);

module.exports = mongoose.model('Analysis', analysisSchema);
