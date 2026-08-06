import { BrowserRouter as Router, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';

// Public pages
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';

// Customer pages
import CustomerDashboard from './pages/customer/CustomerDashboard';
import CustomerOrders from './pages/customer/CustomerOrders';
import CustomerProfile from './pages/customer/CustomerProfile';

// Restaurant pages
import RestaurantDashboard from './pages/restaurant/RestaurantDashboard';
import RestaurantReservations from './pages/restaurant/RestaurantReservations';
import RestaurantProfileSetup from './pages/restaurant/RestaurantProfileSetup';

// Admin pages
import AdminDashboard from './pages/admin/AdminDashboard';
import RestaurantVerification from './pages/admin/RestaurantVerification';
import SystemListings from './pages/admin/SystemListings';

// Redirect global #admin hash to /auth#admin
function HashRedirect() {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (location.hash === '#admin' && location.pathname !== '/auth') {
      navigate('/auth#admin');
    }
  }, [location.hash, location.pathname, navigate]);

  return null;
}

function App() {
  return (
    <Router>
      <HashRedirect />
      <AuthProvider>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <main style={{ flexGrow: 1 }}>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/auth" element={<AuthPage />} />

              {/* Customer Protected Routes */}
              <Route 
                path="/customer/dashboard" 
                element={
                  <ProtectedRoute allowedRoles={['customer']}>
                    <CustomerDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/customer/orders" 
                element={
                  <ProtectedRoute allowedRoles={['customer']}>
                    <CustomerOrders />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/customer/profile" 
                element={
                  <ProtectedRoute allowedRoles={['customer']}>
                    <CustomerProfile />
                  </ProtectedRoute>
                } 
              />

              {/* Restaurant Protected Routes */}
              <Route 
                path="/restaurant/dashboard" 
                element={
                  <ProtectedRoute allowedRoles={['restaurant']}>
                    <RestaurantDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/restaurant/reservations" 
                element={
                  <ProtectedRoute allowedRoles={['restaurant']}>
                    <RestaurantReservations />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/restaurant/profile" 
                element={
                  <ProtectedRoute allowedRoles={['restaurant']}>
                    <RestaurantProfileSetup />
                  </ProtectedRoute>
                } 
              />

              {/* Admin Protected Routes */}
              <Route 
                path="/admin/dashboard" 
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <AdminDashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/admin/verifications" 
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <RestaurantVerification />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/admin/listings" 
                element={
                  <ProtectedRoute allowedRoles={['admin']}>
                    <SystemListings />
                  </ProtectedRoute>
                } 
              />

              {/* Fallback route */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;
