const mongoose = require('mongoose');

const foodItemSchema = new mongoose.Schema({
  restaurant: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'RestaurantProfile',
    required: true
  },
  name: {
    type: String,
    required: true,
    trim: true
  },
  description: {
    type: String,
    trim: true
  },
  originalPrice: {
    type: Number,
    required: true
  },
  discountedPrice: {
    type: Number,
    required: true
  },
  quantity: {
    type: Number,
    required: true,
    min: 0,
    default: 1
  },
  pickupStartTime: {
    type: String, // e.g. "18:00"
    required: true
  },
  pickupEndTime: {
    type: String, // e.g. "21:00"
    required: true
  },
  imagePath: {
    type: String,
    default: ''
  },
  status: {
    type: String,
    enum: ['available', 'sold-out'],
    default: 'available'
  },
  expiryDate: {
    type: Date,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('FoodItem', foodItemSchema);
