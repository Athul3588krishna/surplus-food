const jwt = require('jsonwebtoken');
const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');
const { sendOTP } = require('../config/mailer');

// Generate JWT Token
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET || 'surplus_food_secret_key_12345', {
    expiresIn: '30d'
  });
};

// @desc    Register a new user & Send OTP
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

    // Generate 6-digit OTP
    const otpCode = Math.floor(100000 + Math.random() * 900000).toString();
    const otpExpiry = new Date(Date.now() + 15 * 60 * 1000); // 15 minutes expiry

    // Create user (unverified by default)
    const user = await User.create({
      name,
      email,
      password,
      role: role || 'customer',
      phoneNumber,
      isVerified: false,
      otpCode,
      otpExpiry
    });

    if (user) {
      let restaurantProfile = null;

      // If user is a restaurant, initialize restaurant profile
      if (user.role === 'restaurant') {
        if (!restaurantName || !address || !cuisineType) {
          // Rollback user creation
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

      // Send OTP via Nodemailer
      await sendOTP(user.email, otpCode);

      res.status(201).json({
        message: 'Registration successful. Verification OTP sent to email.',
        email: user.email,
        role: user.role
      });
    } else {
      res.status(400).json({ message: 'Invalid user data' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Verify OTP to activate account
// @route   POST /api/auth/verify-otp
// @access  Public
const verifyOTP = async (req, res) => {
  const { email, otp } = req.body;

  try {
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({ message: 'User account not found' });
    }

    if (user.isVerified) {
      return res.status(400).json({ message: 'This account is already verified' });
    }

    // Check OTP match
    if (user.otpCode !== otp) {
      return res.status(400).json({ message: 'Invalid OTP code. Please check your verification email.' });
    }

    // Check OTP expiry
    if (new Date(user.otpExpiry) < new Date()) {
      return res.status(400).json({ message: 'Verification OTP code has expired. Please register again.' });
    }

    // Mark as verified and clear OTP fields
    user.isVerified = true;
    user.otpCode = '';
    user.otpExpiry = undefined;
    await user.save();

    let restaurantProfile = null;
    if (user.role === 'restaurant') {
      restaurantProfile = await RestaurantProfile.findOne({ user: user._id });
    }

    res.status(200).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      phoneNumber: user.phoneNumber,
      token: generateToken(user._id),
      restaurantProfile: restaurantProfile
    });
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
      // Check email verification status
      if (!user.isVerified) {
        return res.status(401).json({ 
          message: 'Account email is unverified. Please verify your email first.',
          email: user.email,
          needsVerification: true
        });
      }

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
        user.password = req.body.password;
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
            profile.imagePath = `/uploads/${req.file.filename}`;
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
  verifyOTP,
  loginUser,
  getUserProfile,
  updateUserProfile
};
