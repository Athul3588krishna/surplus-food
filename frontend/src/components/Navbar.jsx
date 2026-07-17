import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShoppingBag, 
  User as UserIcon, 
  LogOut, 
  LayoutDashboard, 
  ClipboardList, 
  BarChart3, 
  ShieldCheck, 
  Home, 
  Menu, 
  X,
  Compass
} from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/auth');
    setMobileMenuOpen(false);
  };

  const isActive = (path) => location.pathname === path;

  // Render role-specific navigation links
  const renderNavLinks = () => {
    if (!user) {
      return (
        <>
          <li>
            <Link 
              to="/" 
              className={`navbar-link ${isActive('/') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <Home size={18} /> Home
            </Link>
          </li>
          <li>
            <Link 
              to="/auth" 
              className={`navbar-link ${isActive('/auth') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <UserIcon size={18} /> Login / Sign Up
            </Link>
          </li>
        </>
      );
    }

    if (user.role === 'customer') {
      return (
        <>
          <li>
            <Link 
              to="/customer/dashboard" 
              className={`navbar-link ${isActive('/customer/dashboard') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <Compass size={18} /> Browse Food
            </Link>
          </li>
          <li>
            <Link 
              to="/customer/orders" 
              className={`navbar-link ${isActive('/customer/orders') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <ClipboardList size={18} /> My Reservations
            </Link>
          </li>
          <li>
            <Link 
              to="/customer/profile" 
              className={`navbar-link ${isActive('/customer/profile') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <UserIcon size={18} /> Profile
            </Link>
          </li>
        </>
      );
    }

    if (user.role === 'restaurant') {
      return (
        <>
          <li>
            <Link 
              to="/restaurant/dashboard" 
              className={`navbar-link ${isActive('/restaurant/dashboard') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <LayoutDashboard size={18} /> Listings
            </Link>
          </li>
          <li>
            <Link 
              to="/restaurant/reservations" 
              className={`navbar-link ${isActive('/restaurant/reservations') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <ClipboardList size={18} /> Reservations
            </Link>
          </li>
          <li>
            <Link 
              to="/restaurant/profile" 
              className={`navbar-link ${isActive('/restaurant/profile') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <UserIcon size={18} /> Biz Profile
            </Link>
          </li>
        </>
      );
    }

    if (user.role === 'admin') {
      return (
        <>
          <li>
            <Link 
              to="/admin/dashboard" 
              className={`navbar-link ${isActive('/admin/dashboard') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <BarChart3 size={18} /> Dashboard
            </Link>
          </li>
          <li>
            <Link 
              to="/admin/verifications" 
              className={`navbar-link ${isActive('/admin/verifications') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <ShieldCheck size={18} /> Verify Biz
            </Link>
          </li>
          <li>
            <Link 
              to="/admin/listings" 
              className={`navbar-link ${isActive('/admin/listings') ? 'active' : ''}`}
              onClick={() => setMobileMenuOpen(false)}
            >
              <ShoppingBag size={18} /> Monitor Posts
            </Link>
          </li>
        </>
      );
    }

    return null;
  };

  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">
          <ShoppingBag size={24} className="text-emerald" />
          <span>EcoBite</span>
        </Link>

        {/* Desktop Navigation */}
        <ul className="navbar-links" style={{ display: 'flex' }}>
          {renderNavLinks()}
          {user && (
            <li>
              <button 
                onClick={handleLogout} 
                className="btn btn-secondary btn-sm"
                style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', border: 'none', background: 'transparent', cursor: 'pointer', color: 'var(--text-muted)' }}
              >
                <LogOut size={16} /> Logout
              </button>
            </li>
          )}
        </ul>

        {/* Mobile menu toggle */}
        <button 
          className="mobile-toggle-btn"
          style={{ display: 'none', background: 'transparent', border: 'none', color: 'var(--text-primary)', cursor: 'pointer' }}
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* CSS overrides for mobile layouts */}
      <style>{`
        .mobile-toggle-btn {
          display: none !important;
        }
        @media (max-width: 768px) {
          .mobile-toggle-btn {
            display: block !important;
          }
          .navbar-links {
            display: ${mobileMenuOpen ? 'flex' : 'none'} !important;
            flex-direction: column;
            position: absolute;
            top: 70px;
            left: 0;
            width: 100%;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--glass-border);
            padding: 1.5rem;
            gap: 1.25rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
          }
          .navbar-links li {
            width: 100%;
          }
          .navbar-links li button {
            width: 100%;
            justify-content: flex-start;
          }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
