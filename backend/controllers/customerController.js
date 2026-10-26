const RestaurantProfile = require('../models/RestaurantProfile');
const FoodItem = require('../models/FoodItem');
const Order = require('../models/Order');
const Review = require('../models/Review');
const { sendCollectionToken } = require('../config/mailer');
const { 
  isValidObjectId, 
  isValidPositiveInteger, 
  isValidPositiveNumber, 
  isValidRating 
} = require('../utils/validation');

// @desc    Browse verified restaurants
// @route   GET /api/customer/restaurants
// @access  Private (Customer only)
const getRestaurants = async (req, res) => {
  try {
    const restaurants = await RestaurantProfile.find({ isVerified: true })
      .populate('user', 'name email phoneNumber')
      .sort({ rating: -1 });
    res.json(restaurants);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get active, unexpired food listings
// @route   GET /api/customer/listings
// @access  Private (Customer only)
const getFoodListings = async (req, res) => {
  const { search, cuisine, maxPrice, dietaryType, allergen, isSurpriseBag } = req.query;

  if (maxPrice && !isValidPositiveNumber(maxPrice, 0)) {
    return res.status(400).json({ message: 'Max price filter must be a valid positive number' });
  }

  try {
    // 1. Find all verified restaurants
    let restaurantFilter = { isVerified: true };
    if (cuisine) {
      restaurantFilter.cuisineType = { $regex: cuisine, $options: 'i' };
    }

    const verifiedRestaurants = await RestaurantProfile.find(restaurantFilter);
    const verifiedIds = verifiedRestaurants.map(r => r._id);

    // 2. Find listings for verified restaurants that are unexpired and available
    let foodFilter = {
      restaurant: { $in: verifiedIds },
      expiryDate: { $gt: new Date() },
      quantity: { $gt: 0 },
      status: 'available'
    };

    if (maxPrice) {
      foodFilter.discountedPrice = { $lte: Number(maxPrice) };
    }

    if (search) {
      foodFilter.name = { $regex: search, $options: 'i' };
    }

    if (dietaryType && dietaryType !== 'all') {
      foodFilter.dietaryType = dietaryType;
    }

    if (allergen && allergen !== 'all') {
      foodFilter.allergens = allergen;
    }

    if (isSurpriseBag === 'true' || isSurpriseBag === true) {
      foodFilter.isSurpriseBag = true;
    }

    const listings = await FoodItem.find(foodFilter)
      .populate('restaurant', 'restaurantName address cuisineType rating imagePath')
      .sort({ expiryDate: 1 }); // Soonest expiring first

    res.json(listings);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Reserve a food item
// @route   POST /api/customer/reservations
// @access  Private (Customer only)
const reserveFoodItem = async (req, res) => {
  const { foodItemId, quantity } = req.body;

  if (!isValidObjectId(foodItemId)) {
    return res.status(400).json({ message: 'Invalid or missing food item ID' });
  }

  if (!isValidPositiveInteger(quantity, 1)) {
    return res.status(400).json({ message: 'Quantity must be a positive integer (at least 1)' });
  }

  const qtyToReserve = Number(quantity);

  try {
    const foodItem = await FoodItem.findById(foodItemId).populate('restaurant');
    if (!foodItem) {
      return res.status(404).json({ message: 'Food item not found' });
    }

    // Check expiry
    if (new Date(foodItem.expiryDate) < new Date()) {
      return res.status(400).json({ message: 'Cannot reserve: This food listing has expired' });
    }

    // Check quantity and out-of-stock condition
    if (foodItem.quantity <= 0) {
      return res.status(400).json({ message: 'Cannot reserve: This surplus food item is sold out' });
    }

    if (foodItem.quantity < qtyToReserve) {
      return res.status(400).json({
        message: `Only ${foodItem.quantity} items left in stock. Cannot reserve ${qtyToReserve} items.`
      });
    }

    // Verify restaurant is verified
    if (!foodItem.restaurant.isVerified) {
      return res.status(403).json({ message: 'Cannot reserve from an unverified restaurant profile' });
    }

    // Decrement stock safely (ensuring non-negative)
    foodItem.quantity = Math.max(0, foodItem.quantity - qtyToReserve);
    if (foodItem.quantity === 0) {
      foodItem.status = 'sold-out';
    }
    await foodItem.save();

    // Generate 6-digit collection OTP code
    const pickupToken = Math.floor(100000 + Math.random() * 900000).toString();

    // Create reservation order with non-negative total price
    const totalPrice = Math.max(0, Number((foodItem.discountedPrice * qtyToReserve).toFixed(2)));
    const order = await Order.create({
      customer: req.user._id,
      restaurant: foodItem.restaurant._id,
      foodItem: foodItem._id,
      quantity: qtyToReserve,
      totalPrice,
      status: 'reserved',
      token: pickupToken,
      paymentStatus: 'paid',
      paymentDetails: {
        transactionId: 'TXN-' + Math.floor(10000000 + Math.random() * 90000000),
        cardLast4: req.body.cardLast4 || '4242'
      }
    });

    // Send collection token email asynchronously
    sendCollectionToken(req.user.email, pickupToken, {
      itemName: foodItem.name,
      quantity: qtyToReserve,
      totalPrice,
      restaurantName: foodItem.restaurant.restaurantName,
      pickupStartTime: foodItem.pickupStartTime,
      pickupEndTime: foodItem.pickupEndTime,
      address: foodItem.restaurant.address
    }).catch(err => console.error('Failed to send collection email:', err));

    // Emit real-time Socket.io event to restaurant room
    const io = req.app.get('io');
    if (io) {
      const roomName = `restaurant_${foodItem.restaurant._id.toString()}`;
      io.to(roomName).emit('new_reservation', {
        orderId: order._id,
        customerName: req.user.name,
        customerEmail: req.user.email,
        itemName: foodItem.name,
        quantity: qtyToReserve,
        totalPrice,
        token: pickupToken,
        createdAt: order.createdAt
      });
      io.emit('listings_updated', { foodItemId: foodItem._id });
    }

    res.status(201).json(order);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Cancel a reservation
// @route   PUT /api/customer/reservations/:id/cancel
// @access  Private (Customer only)
const cancelReservation = async (req, res) => {
  if (!isValidObjectId(req.params.id)) {
    return res.status(400).json({ message: 'Invalid reservation ID' });
  }

  try {
    const order = await Order.findById(req.params.id);
    if (!order) {
      return res.status(404).json({ message: 'Reservation details not found' });
    }

    // Check ownership
    if (order.customer.toString() !== req.user._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to cancel this reservation' });
    }

    // Check current status
    if (order.status !== 'reserved') {
      return res.status(400).json({ message: `Cannot cancel a reservation that is already ${order.status}` });
    }

    // Update status
    order.status = 'cancelled';
    const updatedOrder = await order.save();

    // Restore stock
    const foodItem = await FoodItem.findById(order.foodItem);
    if (foodItem) {
      foodItem.quantity += order.quantity;
      if (foodItem.quantity > 0) {
        foodItem.status = 'available';
      }
      await foodItem.save();
    }

    res.json(updatedOrder);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get order/reservation history
// @route   GET /api/customer/orders
// @access  Private (Customer only)
const getCustomerOrders = async (req, res) => {
  try {
    const orders = await Order.find({ customer: req.user._id })
      .populate('restaurant', 'restaurantName address cuisineType rating ratingCount')
      .populate('foodItem', 'name originalPrice discountedPrice imagePath pickupStartTime pickupEndTime')
      .sort({ createdAt: -1 });

    // Find reviews for these orders to check if already rated
    const orderIds = orders.map(o => o._id);
    const reviews = await Review.find({ order: { $in: orderIds } });
    
    // Create a set of reviewed order IDs
    const reviewedOrderIds = new Set(reviews.map(r => r.order.toString()));

    const ordersWithReviewFlag = orders.map(order => {
      const orderObj = order.toObject();
      orderObj.isRated = reviewedOrderIds.has(order._id.toString());
      return orderObj;
    });

    res.json(ordersWithReviewFlag);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Rate a restaurant
// @route   POST /api/customer/rate
// @access  Private (Customer only)
const rateRestaurant = async (req, res) => {
  const { orderId, rating, comment } = req.body;

  if (!isValidObjectId(orderId)) {
    return res.status(400).json({ message: 'Invalid order ID' });
  }

  if (!isValidRating(rating)) {
    return res.status(400).json({ message: 'Rating must be an integer between 1 and 5 stars' });
  }

  const trimmedComment = comment ? String(comment).trim() : '';
  if (trimmedComment.length > 500) {
    return res.status(400).json({ message: 'Review comment cannot exceed 500 characters' });
  }

  const ratingNum = Number(rating);

  try {
    const order = await Order.findById(orderId);
    if (!order) {
      return res.status(404).json({ message: 'Order not found' });
    }

    // Verify ownership
    if (order.customer.toString() !== req.user._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to review this order' });
    }

    // Verify order collected status
    if (order.status !== 'collected') {
      return res.status(400).json({ message: 'You can only rate a restaurant after collecting your order' });
    }

    // Check duplicate reviews
    const existingReview = await Review.findOne({ order: orderId });
    if (existingReview) {
      return res.status(400).json({ message: 'You have already reviewed this order' });
    }

    // Create review
    const review = await Review.create({
      customer: req.user._id,
      restaurant: order.restaurant,
      order: orderId,
      rating: ratingNum,
      comment: trimmedComment
    });

    // Recalculate average rating of restaurant
    const reviews = await Review.find({ restaurant: order.restaurant });
    const totalRating = reviews.reduce((sum, r) => sum + r.rating, 0);
    const avgRating = totalRating / reviews.length;

    await RestaurantProfile.findByIdAndUpdate(order.restaurant, {
      rating: Number(avgRating.toFixed(1)),
      ratingCount: reviews.length
    });

    res.status(201).json(review);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  getRestaurants,
  getFoodListings,
  reserveFoodItem,
  cancelReservation,
  getCustomerOrders,
  rateRestaurant
};
