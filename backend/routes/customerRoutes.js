const express = require('express');
const router = express.Router();
const {
  getRestaurants,
  getFoodListings,
  reserveFoodItem,
  cancelReservation,
  getCustomerOrders,
  rateRestaurant
} = require('../controllers/customerController');
const { protect, verifyRole } = require('../middleware/authMiddleware');

// Lock down all routes to customer role
router.use(protect);
router.use(verifyRole(['customer']));

router.get('/restaurants', getRestaurants);
router.get('/listings', getFoodListings);
router.post('/reservations', reserveFoodItem);
router.put('/reservations/:id/cancel', cancelReservation);
router.get('/orders', getCustomerOrders);
router.post('/rate', rateRestaurant);

module.exports = router;
