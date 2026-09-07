const cron = require('node-cron');
const FoodItem = require('../models/FoodItem');

/**
 * Initializes automated background cron jobs:
 * 1. Auto-expiry of surplus items past pickup window
 * 2. Dynamic price drops in final 30 minutes before store pickup window closes
 */
const startCronJobs = (io) => {
  console.log('⏰ Starting background Cron Jobs (Auto-expiry & Dynamic Price Drops)...');

  // Run every minute
  cron.schedule('* * * * *', async () => {
    try {
      const now = new Date();

      // 1. AUTO EXPIRY: Mark food items as 'sold-out' if expiryDate has passed
      const expiredResult = await FoodItem.updateMany(
        {
          status: 'available',
          expiryDate: { $lte: now }
        },
        {
          $set: { status: 'sold-out' }
        }
      );

      if (expiredResult.modifiedCount > 0) {
        console.log(`[CRON AUTO-EXPIRY] Automatically expired ${expiredResult.modifiedCount} listing(s) past pickup window.`);
        if (io) {
          io.emit('listings_updated', { message: 'Listings auto-expired' });
        }
      }

      // 2. DYNAMIC PRICE DROP: Reduce price by extra 20% in final 30 minutes before expiry
      const thirtyMinsFromNow = new Date(now.getTime() + 30 * 60 * 1000);
      const itemsNearExpiry = await FoodItem.find({
        status: 'available',
        expiryDate: { $gt: now, $lte: thirtyMinsFromNow },
        isDynamicDiscounted: { $ne: true }
      });

      for (const item of itemsNearExpiry) {
        // Apply extra 20% price drop
        const newPrice = Math.max(0.99, Number((item.discountedPrice * 0.8).toFixed(2)));
        if (newPrice < item.discountedPrice) {
          item.discountedPrice = newPrice;
          item.isDynamicDiscounted = true;
          await item.save();
          console.log(`[CRON DYNAMIC PRICE DROP] Reduced price for '${item.name}' to $${newPrice} in final 30 mins!`);
          
          if (io) {
            io.emit('price_drop', {
              itemId: item._id,
              name: item.name,
              newPrice
            });
          }
        }
      }

    } catch (error) {
      console.error('[CRON ERROR] Error executing cron task:', error.message);
    }
  });
};

module.exports = startCronJobs;
