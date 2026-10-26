/**
 * Frontend Validation Helpers for Surplus Food Web App
 */

// Validate email address format
export const isValidEmail = (email) => {
  if (!email || typeof email !== 'string') return false;
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email.trim());
};

// Validate phone number (at least 10 digits)
export const isValidPhone = (phone) => {
  if (!phone || typeof phone !== 'string') return false;
  const digits = phone.replace(/\D/g, '');
  return digits.length >= 10 && digits.length <= 15;
};

// Validate password (min 6 characters)
export const isValidPassword = (password) => {
  return typeof password === 'string' && password.length >= 6;
};

// Validate 6-digit OTP code
export const isValidOtp = (otp) => {
  if (!otp) return false;
  const str = String(otp).trim();
  return /^\d{6}$/.test(str);
};

// Validate mock credit card number (16 digits)
export const isValidCardNumber = (cardNumber) => {
  if (!cardNumber) return false;
  const digits = String(cardNumber).replace(/\D/g, '');
  return digits.length === 16;
};

// Validate mock card expiry (MM/YY, valid month 01-12, not in past)
export const isValidCardExpiry = (expiry) => {
  if (!expiry) return false;
  const trimmed = String(expiry).trim();
  if (!/^\d{2}\/\d{2}$/.test(trimmed)) return false;

  const [mm, yy] = trimmed.split('/').map(Number);
  if (mm < 1 || mm > 12) return false;

  const currentYear = new Date().getFullYear() % 100; // e.g. 26
  const currentMonth = new Date().getMonth() + 1; // 1-12

  if (yy < currentYear) return false;
  if (yy === currentYear && mm < currentMonth) return false;

  return true;
};

// Validate CVV (3 digits)
export const isValidCvv = (cvv) => {
  if (!cvv) return false;
  const digits = String(cvv).replace(/\D/g, '');
  return digits.length === 3;
};

// Validate Time string (HH:mm)
export const isValidTime = (timeStr) => {
  if (!timeStr) return false;
  return /^([01]\d|2[0-3]):([0-5]\d)$/.test(String(timeStr).trim());
};
