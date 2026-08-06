const mongoose = require('mongoose');
let mongod = null;

const connectDB = async () => {
  try {
    let dbUrl = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/surplus-food';
    const isLocal = dbUrl.includes('localhost') || dbUrl.includes('127.0.0.1');

    if (isLocal) {
      try {
        console.log(`Attempting connection to local database: ${dbUrl}`);
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
    } else {
      // Mask password for safe logging
      const safeLogUrl = dbUrl.replace(/:([^@/]+)@/, ':****@');
      console.log(`Attempting connection to remote database (Atlas): ${safeLogUrl}`);
      
      const conn = await mongoose.connect(dbUrl, {
        serverSelectionTimeoutMS: 10000 // 10 seconds timeout for remote Atlas connection
      });
      console.log(`MongoDB Connected: ${conn.connection.host}`);
    }
  } catch (error) {
    console.error(`Database Connection Error: ${error.message}`);
    console.error('If using MongoDB Atlas, please check:');
    console.error('1. Your database username and password in the connection string');
    console.error('2. Network connection and IP Whitelist settings in your MongoDB Atlas dashboard');
    process.exit(1);
  }
};

module.exports = connectDB;
