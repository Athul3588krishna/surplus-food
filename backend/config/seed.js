const User = require('../models/User');
const RestaurantProfile = require('../models/RestaurantProfile');
const FoodItem = require('../models/FoodItem');
const Order = require('../models/Order');
const Review = require('../models/Review');

const seedData = async () => {
  try {
    // Clear all existing data to start clean
    await Order.deleteMany({});
    await FoodItem.deleteMany({});
    await Review.deleteMany({});
    
    // Check if users exist. If so, don't re-seed users to prevent wiping active edits
    const userCount = await User.countDocuments({});
    if (userCount > 0) {
      console.log('Database already has seed accounts. Skipping user seeding.');
      return;
    }

    console.log('Database is empty. Seeding verified test accounts...');

    // 1. Create Admin (Auto-verified)
    const admin = await User.create({
      name: 'System Admin',
      email: 'admin@surplus.com',
      password: 'admin123',
      role: 'admin',
      phoneNumber: '111-222-3333',
      isVerified: true
    });
    console.log('Admin account seeded: admin@surplus.com / admin123');

    // 2. Create Customer (Auto-verified)
    const customer = await User.create({
      name: 'John Doe',
      email: 'customer@surplus.com',
      password: 'customer123',
      role: 'customer',
      phoneNumber: '555-123-4567',
      isVerified: true
    });
    console.log('Customer account seeded: customer@surplus.com / customer123');

    // 3. Create Verified Restaurant (Auto-verified)
    const r1User = await User.create({
      name: 'Baker Chef',
      email: 'restaurant@surplus.com',
      password: 'restaurant123',
      role: 'restaurant',
      phoneNumber: '555-987-6543',
      isVerified: true
    });

    const r1Profile = await RestaurantProfile.create({
      user: r1User._id,
      restaurantName: 'The Green Bakery',
      address: '123 Bread Street, Foodtown',
      cuisineType: 'Bakeries',
      description: 'An artisanal bakery crafting organic bread, pastries, and croissants fresh daily.',
      isVerified: true,
      rating: 5.0,
      ratingCount: 0
    });
    console.log('Verified Restaurant account seeded: restaurant@surplus.com / restaurant123');

    // 4. Create Unverified Restaurant (Auto-verified user, but profile is unverified)
    const r2User = await User.create({
      name: 'Cafe Barista',
      email: 'unverified@surplus.com',
      password: 'restaurant123',
      role: 'restaurant',
      phoneNumber: '555-555-5555',
      isVerified: true
    });

    const r2Profile = await RestaurantProfile.create({
      user: r2User._id,
      restaurantName: 'Neon Coffee & Cafe',
      address: '456 Caffeine Boulevard, Brew City',
      cuisineType: 'Café & Coffee',
      description: 'Vibrant coffee shop serving specialty espresso and fresh vegan cookies.',
      isVerified: false
    });
    console.log('Unverified Restaurant account seeded: unverified@surplus.com / restaurant123');

    console.log('Database seeding completed successfully! Ready for clean state testing.');
  } catch (error) {
    console.error('Seeding failed:', error);
  }
};

module.exports = seedData;
