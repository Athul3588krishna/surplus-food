const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');
const FoodItem = require('../models/FoodItem');
const Order = require('../models/Order');

// @desc    Get all unverified restaurant profiles
// @route   GET /api/admin/pending-restaurants
// @access  Private (Admin only)
const getPendingRestaurants = async (req, res) => {
  try {
    const pending = await RestaurantProfile.find({ isVerified: false })
      .populate('user', 'name email phoneNumber createdAt');
    res.json(pending);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Approve/Verify a restaurant profile
// @route   PUT /api/admin/verify-restaurant/:id
// @access  Private (Admin only)
const verifyRestaurant = async (req, res) => {
  const { action } = req.body; // 'approve' or 'reject'

  try {
    const profile = await RestaurantProfile.findById(req.params.id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    if (action === 'approve') {
      profile.isVerified = true;
      await profile.save();
      res.json({ message: 'Restaurant profile approved successfully', profile });
    } else if (action === 'reject') {
      // If rejected, we can delete the profile and the user account, or just keep it unverified.
      // Let's delete the restaurant profile and remove the user to keep database clean.
      const userId = profile.user;
      await RestaurantProfile.findByIdAndDelete(req.params.id);
      await User.findByIdAndDelete(userId);
      res.json({ message: 'Restaurant profile rejected and account removed' });
    } else {
      res.status(400).json({ message: 'Invalid action. Use approve or reject.' });
    }
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get all users in the system
// @route   GET /api/admin/users
// @access  Private (Admin only)
const getAllUsers = async (req, res) => {
  try {
    const users = await User.find({}).select('-password').sort({ createdAt: -1 });
    res.json(users);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get all food listings (for monitoring)
// @route   GET /api/admin/listings
// @access  Private (Admin only)
const getAllListings = async (req, res) => {
  try {
    const listings = await FoodItem.find({})
      .populate('restaurant', 'restaurantName address cuisineType rating')
      .sort({ createdAt: -1 });
    res.json(listings);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Remove all expired food listings from the database
// @route   DELETE /api/admin/listings/expired
// @access  Private (Admin only)
const removeExpiredListings = async (req, res) => {
  try {
    const result = await FoodItem.deleteMany({ expiryDate: { $lt: new Date() } });
    res.json({
      message: `Cleaned up expired listings successfully.`,
      deletedCount: result.deletedCount
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get system-wide analytics for admin dashboard
// @route   GET /api/admin/analytics
// @access  Private (Admin only)
const getDashboardAnalytics = async (req, res) => {
  try {
    const totalCustomers = await User.countDocuments({ role: 'customer' });
    const totalRestaurants = await User.countDocuments({ role: 'restaurant' });
    const verifiedRestaurants = await RestaurantProfile.countDocuments({ isVerified: true });
    const pendingRestaurants = await RestaurantProfile.countDocuments({ isVerified: false });

    const totalListings = await FoodItem.countDocuments({});
    const activeListings = await FoodItem.countDocuments({
      expiryDate: { $gt: new Date() },
      quantity: { $gt: 0 },
      status: 'available'
    });

    const orders = await Order.find({});
    let totalSales = 0;
    let totalMealsSaved = 0;
    let totalCollectedOrders = 0;
    let totalActiveReservations = 0;
    let totalCancelledOrders = 0;

    orders.forEach((o) => {
      if (o.status === 'collected') {
        totalSales += o.totalPrice;
        totalMealsSaved += o.quantity;
        totalCollectedOrders += 1;
      } else if (o.status === 'reserved') {
        totalActiveReservations += 1;
      } else if (o.status === 'cancelled') {
        totalCancelledOrders += 1;
      }
    });

    res.json({
      totalCustomers,
      totalRestaurants,
      verifiedRestaurants,
      pendingRestaurants,
      totalListings,
      activeListings,
      totalSales,
      totalMealsSaved,
      totalOrders: orders.length,
      totalCollectedOrders,
      totalActiveReservations,
      totalCancelledOrders
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getPendingRestaurants,
  verifyRestaurant,
  getAllUsers,
  getAllListings,
  removeExpiredListings,
  getDashboardAnalytics
};
