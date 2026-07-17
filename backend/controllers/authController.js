const jwt = require('jsonwebtoken');
const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');

// Generate JWT Token
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET || 'surplus_food_secret_key_12345', {
    expiresIn: '30d'
  });
};

// @desc    Register a new user (Customer, Restaurant, or Admin)
// @route   POST /api/auth/register
// @access  Public
const registerUser = async (req, res) => {
  const { name, email, password, role, phoneNumber, restaurantName, address, cuisineType, description } = req.body;

  try {
    // Check if user already exists
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ message: 'User already exists with this email' });
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password,
      role: role || 'customer',
      phoneNumber
    });

    if (user) {
      let restaurantProfile = null;

      // If user is a restaurant, initialize restaurant profile
      if (user.role === 'restaurant') {
        if (!restaurantName || !address || !cuisineType) {
          // If we fail restaurant creation parameters, rollback user creation
          await User.findByIdAndDelete(user._id);
          return res.status(400).json({ message: 'Restaurant Name, Address, and Cuisine Type are required for restaurants' });
        }

        restaurantProfile = await RestaurantProfile.create({
          user: user._id,
          restaurantName,
          address,
          cuisineType,
          description: description || '',
          isVerified: false // Needs admin verification
        });
      }

      res.status(201).json({
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        phoneNumber: user.phoneNumber,
        token: generateToken(user._id),
        restaurantProfile: restaurantProfile
      });
    } else {
      res.status(400).json({ message: 'Invalid user data' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Auth user & get token
// @route   POST /api/auth/login
// @access  Public
const loginUser = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.findOne({ email });

    if (user && (await user.matchPassword(password))) {
      let restaurantProfile = null;

      if (user.role === 'restaurant') {
        restaurantProfile = await RestaurantProfile.findOne({ user: user._id });
      }

      res.json({
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        phoneNumber: user.phoneNumber,
        token: generateToken(user._id),
        restaurantProfile: restaurantProfile
      });
    } else {
      res.status(401).json({ message: 'Invalid email or password' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get user profile
// @route   GET /api/auth/profile
// @access  Private
const getUserProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user._id);

    if (user) {
      let restaurantProfile = null;

      if (user.role === 'restaurant') {
        restaurantProfile = await RestaurantProfile.findOne({ user: user._id });
      }

      res.json({
        _id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        phoneNumber: user.phoneNumber,
        restaurantProfile: restaurantProfile
      });
    } else {
      res.status(404).json({ message: 'User not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update user profile
// @route   PUT /api/auth/profile
// @access  Private
const updateUserProfile = async (req, res) => {
  try {
    const user = await User.findById(req.user._id);

    if (user) {
      user.name = req.body.name || user.name;
      user.phoneNumber = req.body.phoneNumber || user.phoneNumber;

      if (req.body.password) {
        user.password = req.body.password; // Pre-save hook hashes it automatically
      }

      const updatedUser = await user.save();

      let updatedProfile = null;
      if (user.role === 'restaurant') {
        const profile = await RestaurantProfile.findOne({ user: user._id });
        if (profile) {
          profile.restaurantName = req.body.restaurantName || profile.restaurantName;
          profile.address = req.body.address || profile.address;
          profile.cuisineType = req.body.cuisineType || profile.cuisineType;
          profile.description = req.body.description || profile.description;
          profile.latitude = req.body.latitude || profile.latitude;
          profile.longitude = req.body.longitude || profile.longitude;
          
          if (req.file) {
            updatedProfile = `/uploads/${req.file.filename}`;
            profile.imagePath = updatedProfile;
          }

          updatedProfile = await profile.save();
        }
      }

      res.json({
        _id: updatedUser._id,
        name: updatedUser.name,
        email: updatedUser.email,
        role: updatedUser.role,
        phoneNumber: updatedUser.phoneNumber,
        token: generateToken(updatedUser._id),
        restaurantProfile: updatedProfile
      });
    } else {
      res.status(404).json({ message: 'User not found' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  registerUser,
  loginUser,
  getUserProfile,
  updateUserProfile
};
