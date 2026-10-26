const jwt = require('jsonwebtoken');
const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');
const { sendOTP } = require('../config/mailer');
const { isValidEmail, isValidPhone, isValidPassword, isValidName, isValidOtp } = require('../utils/validation');

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
  let { name, email, password, role, phoneNumber, restaurantName, address, cuisineType, description } = req.body;

  name = name?.trim();
  email = email?.trim().toLowerCase();
  phoneNumber = phoneNumber?.trim();
  restaurantName = restaurantName?.trim();
  address = address?.trim();
  cuisineType = cuisineType?.trim();
  description = description?.trim();

  // Validate fields
  if (!name || !isValidName(name)) {
    return res.status(400).json({ message: 'Full name is required and must be between 2 and 100 characters' });
  }

  if (!email || !isValidEmail(email)) {
    return res.status(400).json({ message: 'Please provide a valid email address' });
  }

  if (!password || !isValidPassword(password)) {
    return res.status(400).json({ message: 'Password must be at least 6 characters long' });
  }

  if (!phoneNumber || !isValidPhone(phoneNumber)) {
    return res.status(400).json({ message: 'Please provide a valid phone number with at least 10 digits' });
  }

  const userRole = role === 'restaurant' ? 'restaurant' : 'customer';

  if (userRole === 'restaurant') {
    if (!restaurantName || restaurantName.length < 2) {
      return res.status(400).json({ message: 'Restaurant name is required and must be at least 2 characters' });
    }
    if (!address || address.length < 5) {
      return res.status(400).json({ message: 'Street address is required and must be at least 5 characters' });
    }
    if (!cuisineType || cuisineType.length < 2) {
      return res.status(400).json({ message: 'Cuisine category is required and must be at least 2 characters' });
    }
  }

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
      role: userRole,
      phoneNumber,
      isVerified: false,
      otpCode,
      otpExpiry
    });

    if (user) {
      // If user is a restaurant, initialize restaurant profile
      if (user.role === 'restaurant') {
        await RestaurantProfile.create({
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
  let { email, otp } = req.body;
  email = email?.trim().toLowerCase();
  otp = typeof otp === 'string' ? otp.trim() : String(otp || '').trim();

  if (!email || !isValidEmail(email)) {
    return res.status(400).json({ message: 'Please provide a valid email address' });
  }

  if (!otp || !isValidOtp(otp)) {
    return res.status(400).json({ message: 'Please enter a valid 6-digit verification code' });
  }

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
  let { email, password } = req.body;
  email = email?.trim().toLowerCase();

  if (!email || !isValidEmail(email)) {
    return res.status(400).json({ message: 'Please provide a valid email address' });
  }

  if (!password) {
    return res.status(400).json({ message: 'Password is required' });
  }

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

    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }

    if (req.body.name !== undefined) {
      const trimmedName = req.body.name.trim();
      if (!isValidName(trimmedName)) {
        return res.status(400).json({ message: 'Name must be between 2 and 100 characters' });
      }
      user.name = trimmedName;
    }

    if (req.body.phoneNumber !== undefined) {
      const trimmedPhone = req.body.phoneNumber.trim();
      if (!isValidPhone(trimmedPhone)) {
        return res.status(400).json({ message: 'Phone number must have at least 10 digits' });
      }
      user.phoneNumber = trimmedPhone;
    }

    if (req.body.password) {
      if (!isValidPassword(req.body.password)) {
        return res.status(400).json({ message: 'New password must be at least 6 characters long' });
      }
      user.password = req.body.password;
    }

    const updatedUser = await user.save();

    let updatedProfile = null;
    if (user.role === 'restaurant') {
      const profile = await RestaurantProfile.findOne({ user: user._id });
      if (profile) {
        if (req.body.restaurantName !== undefined) {
          const rName = req.body.restaurantName.trim();
          if (rName.length < 2) {
            return res.status(400).json({ message: 'Restaurant name must be at least 2 characters' });
          }
          profile.restaurantName = rName;
        }

        if (req.body.address !== undefined) {
          const addr = req.body.address.trim();
          if (addr.length < 5) {
            return res.status(400).json({ message: 'Street address must be at least 5 characters' });
          }
          profile.address = addr;
        }

        if (req.body.cuisineType !== undefined) {
          const cType = req.body.cuisineType.trim();
          if (cType.length < 2) {
            return res.status(400).json({ message: 'Cuisine category must be at least 2 characters' });
          }
          profile.cuisineType = cType;
        }

        if (req.body.description !== undefined) {
          profile.description = req.body.description.trim();
        }

        if (req.body.latitude !== undefined) profile.latitude = req.body.latitude;
        if (req.body.longitude !== undefined) profile.longitude = req.body.longitude;
        
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
