const RestaurantProfile = require('../models/RestaurantProfile');
const FoodItem = require('../models/FoodItem');
const Order = require('../models/Order');

// Helper to get restaurant profile of logged-in user
const getProfileOfUser = async (userId) => {
  return await RestaurantProfile.findOne({ user: userId });
};

// @desc    Add a new surplus food item listing
// @route   POST /api/restaurant/listings
// @access  Private (Restaurant only)
const addFoodItem = async (req, res) => {
  const { name, description, originalPrice, discountedPrice, quantity, pickupStartTime, pickupEndTime, dietaryType, allergens, isSurpriseBag, estimatedValue } = req.body;

  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    if (!profile.isVerified) {
      return res.status(403).json({ message: 'Your restaurant profile is pending admin verification. You cannot create listings yet.' });
    }

    // Calculate expiry date automatically based on pickupEndTime
    const [hours, minutes] = pickupEndTime.split(':');
    let expiryDate = new Date();
    expiryDate.setHours(parseInt(hours, 10), parseInt(minutes, 10), 0, 0);
    // If the expiry hour is in the past for today, set it for tomorrow
    if (expiryDate < new Date()) {
      expiryDate.setDate(expiryDate.getDate() + 1);
    }

    let imagePath = '';
    if (req.file) {
      imagePath = `/uploads/${req.file.filename}`;
    }

    let parsedAllergens = [];
    if (allergens) {
      if (Array.isArray(allergens)) {
        parsedAllergens = allergens;
      } else if (typeof allergens === 'string') {
        try {
          parsedAllergens = JSON.parse(allergens);
        } catch (e) {
          parsedAllergens = allergens.split(',').map(s => s.trim()).filter(Boolean);
        }
      }
    }

    const foodItem = await FoodItem.create({
      restaurant: profile._id,
      name,
      description,
      originalPrice: Number(originalPrice),
      discountedPrice: Number(discountedPrice),
      quantity: Number(quantity),
      pickupStartTime,
      pickupEndTime,
      imagePath,
      expiryDate,
      dietaryType: dietaryType || 'veg',
      allergens: parsedAllergens,
      isSurpriseBag: isSurpriseBag === true || isSurpriseBag === 'true',
      estimatedValue: estimatedValue ? Number(estimatedValue) : Number(originalPrice),
      status: Number(quantity) > 0 ? 'available' : 'sold-out'
    });

    res.status(201).json(foodItem);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get all listings of the restaurant
// @route   GET /api/restaurant/listings
// @access  Private (Restaurant only)
const getRestaurantFoodItems = async (req, res) => {
  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const items = await FoodItem.find({ restaurant: profile._id }).sort({ createdAt: -1 });
    res.json(items);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update a food item listing
// @route   PUT /api/restaurant/listings/:id
// @access  Private (Restaurant only)
const updateFoodItem = async (req, res) => {
  const { name, description, originalPrice, discountedPrice, quantity, pickupStartTime, pickupEndTime, status, dietaryType, allergens, isSurpriseBag, estimatedValue } = req.body;

  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const foodItem = await FoodItem.findById(req.params.id);
    if (!foodItem) {
      return res.status(404).json({ message: 'Food listing not found' });
    }

    // Verify ownership
    if (foodItem.restaurant.toString() !== profile._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to modify this listing' });
    }

    foodItem.name = name || foodItem.name;
    foodItem.description = description !== undefined ? description : foodItem.description;
    foodItem.originalPrice = originalPrice !== undefined ? Number(originalPrice) : foodItem.originalPrice;
    foodItem.discountedPrice = discountedPrice !== undefined ? Number(discountedPrice) : foodItem.discountedPrice;
    foodItem.quantity = quantity !== undefined ? Number(quantity) : foodItem.quantity;
    foodItem.pickupStartTime = pickupStartTime || foodItem.pickupStartTime;
    foodItem.pickupEndTime = pickupEndTime || foodItem.pickupEndTime;
    if (dietaryType) {
      foodItem.dietaryType = dietaryType;
    }
    if (allergens !== undefined) {
      if (Array.isArray(allergens)) {
        foodItem.allergens = allergens;
      } else if (typeof allergens === 'string') {
        try {
          foodItem.allergens = JSON.parse(allergens);
        } catch (e) {
          foodItem.allergens = allergens.split(',').map(s => s.trim()).filter(Boolean);
        }
      }
    }
    if (isSurpriseBag !== undefined) {
      foodItem.isSurpriseBag = isSurpriseBag === true || isSurpriseBag === 'true';
    }
    if (estimatedValue !== undefined) {
      foodItem.estimatedValue = Number(estimatedValue);
    }
    
    // Recalculate status based on quantity
    if (foodItem.quantity <= 0) {
      foodItem.status = 'sold-out';
    } else {
      foodItem.status = status || foodItem.status || 'available';
    }

    // Recalculate expiry date if pickupEndTime changed
    if (pickupEndTime) {
      const [hours, minutes] = pickupEndTime.split(':');
      let expiryDate = new Date();
      expiryDate.setHours(parseInt(hours, 10), parseInt(minutes, 10), 0, 0);
      if (expiryDate < new Date()) {
        expiryDate.setDate(expiryDate.getDate() + 1);
      }
      foodItem.expiryDate = expiryDate;
    }

    if (req.file) {
      foodItem.imagePath = `/uploads/${req.file.filename}`;
    }

    const updatedItem = await foodItem.save();
    res.json(updatedItem);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Delete a food item listing
// @route   DELETE /api/restaurant/listings/:id
// @access  Private (Restaurant only)
const deleteFoodItem = async (req, res) => {
  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const foodItem = await FoodItem.findById(req.params.id);
    if (!foodItem) {
      return res.status(404).json({ message: 'Food listing not found' });
    }

    // Verify ownership
    if (foodItem.restaurant.toString() !== profile._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to modify this listing' });
    }

    // Delete listing
    await FoodItem.findByIdAndDelete(req.params.id);
    res.json({ message: 'Food item deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get all reservations for a restaurant
// @route   GET /api/restaurant/reservations
// @access  Private (Restaurant only)
const getRestaurantReservations = async (req, res) => {
  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const reservations = await Order.find({ restaurant: profile._id })
      .populate('customer', 'name email phoneNumber')
      .populate('foodItem', 'name originalPrice discountedPrice imagePath pickupStartTime pickupEndTime')
      .sort({ createdAt: -1 });

    res.json(reservations);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Update status of a reservation (collected / cancelled)
// @route   PUT /api/restaurant/reservations/:id
// @access  Private (Restaurant only)
const updateReservationStatus = async (req, res) => {
  const { status } = req.body;

  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const order = await Order.findById(req.params.id);
    if (!order) {
      return res.status(404).json({ message: 'Reservation not found' });
    }

    // Verify ownership
    if (order.restaurant.toString() !== profile._id.toString()) {
      return res.status(401).json({ message: 'Not authorized' });
    }

    const previousStatus = order.status;

    if (previousStatus === status) {
      return res.status(400).json({ message: `Reservation is already in ${status} status` });
    }

    order.status = status;
    const updatedOrder = await order.save();

    // If reservation is cancelled, restore stock
    if (status === 'cancelled' && previousStatus !== 'cancelled') {
      const foodItem = await FoodItem.findById(order.foodItem);
      if (foodItem) {
        foodItem.quantity += order.quantity;
        if (foodItem.quantity > 0) {
          foodItem.status = 'available';
        }
        await foodItem.save();
      }
    }

    // If reservation goes from cancelled back to reserved (unlikely but safe), decrease stock
    if (previousStatus === 'cancelled' && status === 'reserved') {
      const foodItem = await FoodItem.findById(order.foodItem);
      if (foodItem) {
        if (foodItem.quantity < order.quantity) {
          return res.status(400).json({ message: 'Not enough inventory to restore reservation' });
        }
        foodItem.quantity -= order.quantity;
        if (foodItem.quantity === 0) {
          foodItem.status = 'sold-out';
        }
        await foodItem.save();
      }
    }

    res.json(updatedOrder);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Get dashboard metrics for restaurant
// @route   GET /api/restaurant/analytics
// @access  Private (Restaurant only)
const getRestaurantAnalytics = async (req, res) => {
  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const orders = await Order.find({ restaurant: profile._id });

    // Calculate details
    let totalRevenue = 0;
    let mealsSaved = 0;
    let activeReservationsCount = 0;

    orders.forEach((o) => {
      if (o.status === 'collected') {
        totalRevenue += o.totalPrice;
        mealsSaved += o.quantity;
      } else if (o.status === 'reserved') {
        activeReservationsCount += 1;
      }
    });

    res.json({
      profileId: profile._id,
      restaurantName: profile.restaurantName,
      cuisineType: profile.cuisineType,
      isVerified: profile.isVerified,
      rating: profile.rating,
      ratingCount: profile.ratingCount,
      totalRevenue,
      mealsSaved,
      activeReservationsCount,
      totalOrdersCount: orders.length
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Verify customer collection token (OTP) and mark order as collected
// @route   POST /api/restaurant/reservations/:id/verify
// @access  Private (Restaurant only)
const verifyReservationToken = async (req, res) => {
  const { token } = req.body;

  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    const order = await Order.findById(req.params.id)
      .populate('customer', 'name email phoneNumber')
      .populate('foodItem', 'name originalPrice discountedPrice imagePath pickupStartTime pickupEndTime');

    if (!order) {
      return res.status(404).json({ message: 'Reservation not found' });
    }

    // Verify ownership
    if (order.restaurant.toString() !== profile._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to manage this reservation' });
    }

    if (order.status !== 'reserved') {
      return res.status(400).json({ message: `Reservation is already in ${order.status} status` });
    }

    // Verify token
    if (order.token !== token) {
      return res.status(400).json({ message: 'Invalid verification token. Please double-check the customer code.' });
    }

    order.status = 'collected';
    const updatedOrder = await order.save();

    res.json(updatedOrder);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// @desc    Scan and verify customer QR code payload to mark order as collected
// @route   POST /api/restaurant/reservations/scan-qr
// @access  Private (Restaurant only)
const scanAndVerifyQRCode = async (req, res) => {
  const { qrData, orderId, token } = req.body;

  try {
    const profile = await getProfileOfUser(req.user._id);
    if (!profile) {
      return res.status(404).json({ message: 'Restaurant profile not found' });
    }

    let parsedOrderId = orderId;
    let parsedToken = token;

    if (qrData) {
      let data = qrData;
      if (typeof qrData === 'string') {
        try {
          data = JSON.parse(qrData);
        } catch (e) {
          if (qrData.startsWith('ORDER:')) {
            const parts = qrData.split(':');
            parsedOrderId = parts[1];
            parsedToken = parts[2];
          } else {
            parsedToken = qrData.trim();
          }
        }
      }
      if (data && typeof data === 'object') {
        if (data.orderId) parsedOrderId = data.orderId;
        if (data.token) parsedToken = data.token;
      }
    }

    let order = null;
    if (parsedOrderId) {
      order = await Order.findById(parsedOrderId)
        .populate('customer', 'name email phoneNumber')
        .populate('foodItem', 'name originalPrice discountedPrice imagePath pickupStartTime pickupEndTime');
    } else if (parsedToken) {
      order = await Order.findOne({ token: parsedToken, restaurant: profile._id, status: 'reserved' })
        .populate('customer', 'name email phoneNumber')
        .populate('foodItem', 'name originalPrice discountedPrice imagePath pickupStartTime pickupEndTime');
    }

    if (!order) {
      return res.status(404).json({ message: 'Reservation not found for scanned QR code or OTP token.' });
    }

    // Verify ownership
    if (order.restaurant.toString() !== profile._id.toString()) {
      return res.status(401).json({ message: 'Not authorized: This reservation belongs to another restaurant.' });
    }

    if (order.status !== 'reserved') {
      return res.status(400).json({ message: `Reservation is already in ${order.status} status.` });
    }

    // Verify token if parsedToken was provided
    if (parsedToken && order.token !== parsedToken) {
      return res.status(400).json({ message: 'Invalid verification token in QR code.' });
    }

    order.status = 'collected';
    const updatedOrder = await order.save();

    res.json({
      message: 'Order verified and collected successfully!',
      order: updatedOrder
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

module.exports = {
  addFoodItem,
  getRestaurantFoodItems,
  updateFoodItem,
  deleteFoodItem,
  getRestaurantReservations,
  updateReservationStatus,
  getRestaurantAnalytics,
  verifyReservationToken,
  scanAndVerifyQRCode
};
