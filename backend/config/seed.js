const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');
const FoodItem = require('../models/FoodItem');

const seedData = async () => {
  try {
    const userCount = await User.countDocuments({});
    if (userCount > 0) {
      console.log('Database already has data. Skipping automatic seed.');
      return;
    }

    console.log('Database is empty. Seeding test accounts and listings...');

    // 1. Create Admin
    const admin = await User.create({
      name: 'System Admin',
      email: 'admin@surplus.com',
      password: 'admin123',
      role: 'admin',
      phoneNumber: '111-222-3333'
    });
    console.log('Admin account created (admin@surplus.com / admin123)');

    // 2. Create Customer
    const customer = await User.create({
      name: 'John Doe',
      email: 'customer@surplus.com',
      password: 'customer123',
      role: 'customer',
      phoneNumber: '555-123-4567'
    });
    console.log('Customer account created (customer@surplus.com / customer123)');

    // 3. Create Verified Restaurant
    const r1User = await User.create({
      name: 'Baker Chef',
      email: 'restaurant@surplus.com',
      password: 'restaurant123',
      role: 'restaurant',
      phoneNumber: '555-987-6543'
    });

    const r1Profile = await RestaurantProfile.create({
      user: r1User._id,
      restaurantName: 'The Green Bakery',
      address: '123 Bread Street, Foodtown',
      cuisineType: 'Bakeries',
      description: 'An artisanal bakery crafting organic bread, pastries, and croissants fresh daily.',
      isVerified: true,
      rating: 4.8,
      ratingCount: 12
    });
    console.log('Verified Restaurant created (restaurant@surplus.com / restaurant123)');

    // 4. Create Unverified Restaurant
    const r2User = await User.create({
      name: 'Cafe Barista',
      email: 'unverified@surplus.com',
      password: 'restaurant123',
      role: 'restaurant',
      phoneNumber: '555-555-5555'
    });

    const r2Profile = await RestaurantProfile.create({
      user: r2User._id,
      restaurantName: 'Neon Coffee & Cafe',
      address: '456 Caffeine Boulevard, Brew City',
      cuisineType: 'Café & Coffee',
      description: 'Vibrant coffee shop serving specialty espresso and fresh vegan cookies.',
      isVerified: false
    });
    console.log('Unverified Restaurant created (unverified@surplus.com / restaurant123)');

    // 5. Create some food items for the verified restaurant
    const todayEnd = new Date();
    todayEnd.setHours(22, 0, 0, 0); // 10 PM today

    await FoodItem.create({
      restaurant: r1Profile._id,
      name: 'Surplus Croissant Box',
      description: 'A box of 4 butter and almond croissants baked this morning.',
      originalPrice: 16.00,
      discountedPrice: 5.50,
      quantity: 3,
      pickupStartTime: '18:00',
      pickupEndTime: '20:30',
      expiryDate: todayEnd,
      status: 'available'
    });

    await FoodItem.create({
      restaurant: r1Profile._id,
      name: 'Assorted Sourdough Loaf',
      description: 'One large rustic country sourdough loaf.',
      originalPrice: 8.50,
      discountedPrice: 3.00,
      quantity: 2,
      pickupStartTime: '18:00',
      pickupEndTime: '20:30',
      expiryDate: todayEnd,
      status: 'available'
    });

    console.log('Seeded initial food items for The Green Bakery.');
    console.log('Database seeding completed successfully!');
  } catch (error) {
    console.error('Seeding failed:', error);
  }
};

module.exports = seedData;
