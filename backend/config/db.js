const mongoose = require('mongoose');
let mongod = null;

const connectDB = async () => {
  try {
    let dbUrl = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/surplus-food';
    
    try {
      console.log(`Attempting connection to database: ${dbUrl}`);
      // Use a short timeout of 2 seconds for local connection check
      const conn = await mongoose.connect(dbUrl, {
        serverSelectionTimeoutMS: 2000
      });
      console.log(`MongoDB Connected: ${conn.connection.host}`);
    } catch (err) {
      console.log(`Local MongoDB connection failed: ${err.message}`);
      console.log('Spinning up MongoMemoryServer in-memory fallback...');
      
      const { MongoMemoryServer } = require('mongodb-memory-server');
      mongod = await MongoMemoryServer.create();
      dbUrl = mongod.getUri();
      console.log(`In-Memory MongoDB Server started at: ${dbUrl}`);
      
      const conn = await mongoose.connect(dbUrl);
      console.log(`MongoDB Connected (In-Memory): ${conn.connection.host}`);
    }
  } catch (error) {
    console.error(`Database Connection Error: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB;
