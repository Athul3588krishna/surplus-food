const express = require('express');
const router = express.Router();
const {
  getPendingRestaurants,
  verifyRestaurant,
  getAllUsers,
  getAllListings,
  removeExpiredListings,
  getDashboardAnalytics
} = require('../controllers/adminController');
const { protect, verifyRole } = require('../middleware/authMiddleware');

// Lock down all routes to admin role
router.use(protect);
router.use(verifyRole(['admin']));

router.get('/pending-restaurants', getPendingRestaurants);
router.put('/verify-restaurant/:id', verifyRestaurant);
router.get('/users', getAllUsers);
router.get('/listings', getAllListings);
router.delete('/listings/expired', removeExpiredListings);
router.get('/analytics', getDashboardAnalytics);

module.exports = router;
