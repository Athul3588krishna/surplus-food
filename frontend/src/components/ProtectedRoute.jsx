import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontFamily: 'var(--font-display)',
        color: 'var(--text-secondary)'
      }}>
        Loading session...
      </div>
    );
  }

  // User is not logged in, redirect to authentication page
  if (!user) {
    return <Navigate to="/auth" replace />;
  }

  // Check role restriction if provided
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // If not authorized for this portal, bounce back to index
    return <Navigate to="/" replace />;
  }

  return children;
};

export default ProtectedRoute;
