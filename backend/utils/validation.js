const mongoose = require('mongoose');

/**
 * Common validation utilities for backend controllers
 */

// Email validation
const isValidEmail = (email) => {
  if (!email || typeof email !== 'string') return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
};

// Phone number validation (at least 10 digits, allows +, -, spaces, parentheses)
const isValidPhone = (phone) => {
  if (!phone || typeof phone !== 'string') return false;
  const digitsOnly = phone.replace(/\D/g, '');
  return digitsOnly.length >= 10 && digitsOnly.length <= 15;
};

// Password validation (min 6 characters)
const isValidPassword = (password) => {
  if (!password || typeof password !== 'string') return false;
  return password.length >= 6;
};

// Name validation (min 2 characters, max 100)
const isValidName = (name) => {
  if (!name || typeof name !== 'string') return false;
  const trimmed = name.trim();
  return trimmed.length >= 2 && trimmed.length <= 100;
};

// MongoDB ObjectId validation
const isValidObjectId = (id) => {
  if (!id) return false;
  return mongoose.Types.ObjectId.isValid(id);
};

// 6-digit OTP code validation
const isValidOtp = (otp) => {
  if (!otp || typeof otp !== 'string') return false;
  return /^\d{6}$/.test(otp.trim());
};

// Time format HH:mm validation
const isValidTime = (time) => {
  if (!time || typeof time !== 'string') return false;
  return /^([01]\d|2[0-3]):([0-5]\d)$/.test(time.trim());
};

// Number validation (positive, optionally with min/max)
const isValidPositiveNumber = (num, min = 0.01) => {
  const val = Number(num);
  return !isNaN(val) && val >= min;
};

// Integer validation (min >= 1)
const isValidPositiveInteger = (num, min = 1) => {
  const val = Number(num);
  return Number.isInteger(val) && val >= min;
};

// Rating score validation (integer 1 - 5)
const isValidRating = (rating) => {
  const val = Number(rating);
  return Number.isInteger(val) && val >= 1 && val <= 5;
};

module.exports = {
  isValidEmail,
  isValidPhone,
  isValidPassword,
  isValidName,
  isValidObjectId,
  isValidOtp,
  isValidTime,
  isValidPositiveNumber,
  isValidPositiveInteger,
  isValidRating
};
