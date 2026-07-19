const express = require('express');
const router = express.Router();
const {
  addFoodItem,
  getRestaurantFoodItems,
  updateFoodItem,
  deleteFoodItem,
  getRestaurantReservations,
  updateReservationStatus,
  getRestaurantAnalytics,
  verifyReservationToken
} = require('../controllers/restaurantController');
const { protect, verifyRole } = require('../middleware/authMiddleware');
const upload = require('../middleware/uploadMiddleware');

// Lock down all routes to restaurant role
router.use(protect);
router.use(verifyRole(['restaurant']));

router.route('/listings')
  .post(upload.single('image'), addFoodItem)
  .get(getRestaurantFoodItems);

router.route('/listings/:id')
  .put(upload.single('image'), updateFoodItem)
  .delete(deleteFoodItem);

router.get('/reservations', getRestaurantReservations);
router.put('/reservations/:id', updateReservationStatus);
router.post('/reservations/:id/verify', verifyReservationToken);
router.get('/analytics', getRestaurantAnalytics);

module.exports = router;
