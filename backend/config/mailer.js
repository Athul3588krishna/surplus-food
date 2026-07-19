const nodemailer = require('nodemailer');

let transporter = null;

// Initialize transport
const getTransporter = async () => {
  if (transporter) return transporter;

  const useConfig = process.env.SMTP_HOST && process.env.SMTP_USER;

  if (useConfig) {
    console.log('Mailer: Using configured SMTP server settings.');
    transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT) || 587,
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });
  } else {
    console.log('Mailer: No SMTP settings in .env. Creating temporary Ethereal Mail test account...');
    const testAccount = await nodemailer.createTestAccount();
    console.log(`Mailer: Ethereal test account created: User = ${testAccount.user}`);
    transporter = nodemailer.createTransport({
      host: 'smtp.ethereal.email',
      port: 587,
      secure: false,
      auth: {
        user: testAccount.user,
        pass: testAccount.pass
      }
    });
  }

  return transporter;
};

// Send Registration OTP
const sendOTP = async (email, otp) => {
  try {
    const mailClient = await getTransporter();
    const mailOptions = {
      from: '"EcoBite Marketplace" <no-reply@ecobite.com>',
      to: email,
      subject: 'EcoBite - Verify Your Email Account',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
          <h2 style="color: #10b981; text-align: center;">Welcome to EcoBite!</h2>
          <p>Thank you for signing up to save surplus food. To complete your registration, please verify your email address by entering the following One-Time Password (OTP):</p>
          <div style="text-align: center; margin: 30px 0;">
            <span style="font-size: 2.5rem; font-weight: bold; letter-spacing: 5px; color: #4f46e5; padding: 10px 20px; background: #f3f4f6; border-radius: 8px; border: 1px solid #e5e7eb;">${otp}</span>
          </div>
          <p>This code is valid for <strong>15 minutes</strong>. If you did not request this code, you can safely ignore this email.</p>
          <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;" />
          <p style="font-size: 0.8rem; color: #888; text-align: center;">EcoBite Surplus Food Marketplace &copy; 2026</p>
        </div>
      `
    };

    const info = await mailClient.sendMail(mailOptions);
    const previewUrl = nodemailer.getTestMessageUrl(info);
    if (previewUrl) {
      console.log(`\n=============================================================`);
      console.log(`Mailer: Verification OTP Sent to ${email}!`);
      console.log(`Mailer: Preview simulated email at: ${previewUrl}`);
      console.log(`=============================================================\n`);
    } else {
      console.log(`Mailer: Verification OTP email sent to ${email}`);
    }
  } catch (error) {
    console.error('Mailer: Error sending OTP email:', error);
  }
};

// Send Collection Token
const sendCollectionToken = async (email, token, orderDetails) => {
  try {
    const mailClient = await getTransporter();
    const mailOptions = {
      from: '"EcoBite Marketplace" <no-reply@ecobite.com>',
      to: email,
      subject: `EcoBite - Your Reservation Collection Token [${token}]`,
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
          <h2 style="color: #10b981; text-align: center;">Reservation Confirmed!</h2>
          <p>Your payment has been simulated successfully. Below is your 6-digit collection OTP token. Show this code to the restaurant staff to claim your surplus food.</p>
          
          <div style="text-align: center; margin: 30px 0;">
            <p style="font-size: 0.9rem; color: #666; margin-bottom: 5px;">COLLECTION TOKEN (OTP)</p>
            <span style="font-size: 2.2rem; font-weight: bold; letter-spacing: 3px; color: #10b981; padding: 10px 20px; background: #e6f7f2; border-radius: 8px; border: 1px solid #a7f3d0;">${token}</span>
          </div>

          <div style="background: #f9fafb; padding: 15px; border-radius: 6px; border: 1px solid #f3f4f6; margin-bottom: 20px;">
            <h3 style="margin-top: 0; color: #333; font-size: 1rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 5px;">Order Information</h3>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Item:</strong> ${orderDetails.itemName}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Quantity:</strong> ${orderDetails.quantity}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Amount Paid:</strong> $${orderDetails.totalPrice.toFixed(2)}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Store Name:</strong> ${orderDetails.restaurantName}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Pickup Window:</strong> ${orderDetails.pickupStartTime} - ${orderDetails.pickupEndTime}</p>
            <p style="margin: 5px 0; font-size: 0.9rem;"><strong>Store Address:</strong> ${orderDetails.address}</p>
          </div>
          
          <p style="font-size: 0.85rem; color: #ef4444;">Please arrive during the pickup window. Uncollected items are non-refundable and will be discarded at the end of the window.</p>
          <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;" />
          <p style="font-size: 0.8rem; color: #888; text-align: center;">EcoBite Surplus Food Marketplace &copy; 2026</p>
        </div>
      `
    };

    const info = await mailClient.sendMail(mailOptions);
    const previewUrl = nodemailer.getTestMessageUrl(info);
    if (previewUrl) {
      console.log(`\n=============================================================`);
      console.log(`Mailer: Collection Token Sent to ${email}!`);
      console.log(`Mailer: Preview simulated email at: ${previewUrl}`);
      console.log(`=============================================================\n`);
    } else {
      console.log(`Mailer: Collection Token email sent to ${email}`);
    }
  } catch (error) {
    console.error('Mailer: Error sending collection token email:', error);
  }
};

module.exports = {
  sendOTP,
  sendCollectionToken
};
