require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const connectDB = require('./config/db');

// Import routes
const authRoutes = require('./routes/authRoutes');
const restaurantRoutes = require('./routes/restaurantRoutes');
const customerRoutes = require('./routes/customerRoutes');
const adminRoutes = require('./routes/adminRoutes');

const http = require('http');
const { Server } = require('socket.io');
const startCronJobs = require('./config/cronJobs');

// Connect to Database
const seedData = require('./config/seed');
connectDB().then(() => {
  seedData();
});

const app = express();
const server = http.createServer(app);

// Initialize Socket.io
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE']
  }
});

// Save io instance to Express app so controllers can access it via req.app.get('io')
app.set('io', io);

// Handle Socket.io connections & room subscriptions
io.on('connection', (socket) => {
  console.log(`🔌 Socket client connected: ${socket.id}`);

  socket.on('join_room', (room) => {
    socket.join(room);
    console.log(`📡 Socket ${socket.id} joined room: ${room}`);
  });

  socket.on('disconnect', () => {
    console.log(`🔌 Socket client disconnected: ${socket.id}`);
  });
});

// Start background cron jobs (Auto Expiry & Dynamic Price Drop)
startCronJobs(io);

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static uploads folder
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Mount routes
app.use('/api/auth', authRoutes);
app.use('/api/restaurant', restaurantRoutes);
app.use('/api/customer', customerRoutes);
app.use('/api/admin', adminRoutes);

// Base route
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to the Surplus Food Marketplace API' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    message: err.message || 'An unexpected server error occurred',
    stack: process.env.NODE_ENV === 'development' ? err.stack : {}
  });
});

const PORT = process.env.PORT || 5000;

server.listen(PORT, () => {
  console.log(`🚀 Server with Socket.io running on port ${PORT}`);
});
