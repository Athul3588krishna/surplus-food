import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Leaf, ArrowRight, ShieldCheck, ShoppingBag, Clock } from 'lucide-react';

const LandingPage = () => {
  const { user } = useAuth();

  return (
    <div className="landing-container animate-fade-in" style={{ paddingBottom: '4rem' }}>
      {/* Hero Section */}
      <section className="hero-section" style={{ padding: '6rem 0 4rem 0', textAlign: 'center' }}>
        <div className="container" style={{ maxWidth: '800px' }}>
          <div className="badge badge-success" style={{ marginBottom: '1.5rem', textTransform: 'none', padding: '0.4rem 1rem' }}>
            <Leaf size={14} style={{ marginRight: '0.4rem' }} /> Join the anti-food-waste revolution
          </div>
          
          <h1 style={{ fontSize: '3.5rem', lineHeight: '1.2', marginBottom: '1.5rem' }}>
            Rescue Delicious Surplus Food, <br />
            <span className="text-emerald">Save Money & the Planet</span>
          </h1>
          
          <p className="text-secondary" style={{ fontSize: '1.2rem', marginBottom: '2.5rem' }}>
            Local restaurants, bakeries, and cafés list their fresh unsold food at deep discounts at the end of the day. Browse, reserve, and pick up your meal.
          </p>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            {user ? (
              user.role === 'customer' ? (
                <Link to="/customer/dashboard" className="btn btn-primary">
                  Browse Surplus Deals <ArrowRight size={18} />
                </Link>
              ) : user.role === 'restaurant' ? (
                <Link to="/restaurant/dashboard" className="btn btn-primary">
                  Manage Listings <ArrowRight size={18} />
                </Link>
              ) : (
                <Link to="/admin/dashboard" className="btn btn-indigo">
                  Admin Panel <ArrowRight size={18} />
                </Link>
              )
            ) : (
              <>
                <Link to="/auth?tab=register" className="btn btn-primary">
                  Get Started <ArrowRight size={18} />
                </Link>
                <Link to="/auth?tab=login" className="btn btn-secondary">
                  Restaurant Sign In
                </Link>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Impact Stats */}
      <section className="stats-section" style={{ padding: '2rem 0' }}>
        <div className="container">
          <div className="glass-panel" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', padding: '2rem', textAlign: 'center', gap: '2rem' }}>
            <div>
              <h3 style={{ fontSize: '2.5rem', color: 'var(--color-primary)' }}>12,450+</h3>
              <p className="text-secondary" style={{ fontSize: '0.95rem', marginTop: '0.25rem' }}>Meals Rescued</p>
            </div>
            <div style={{ borderLeft: '1px solid var(--glass-border)', borderRight: '1px solid var(--glass-border)' }}>
              <h3 style={{ fontSize: '2.5rem', color: 'var(--color-accent)' }}>$48,900+</h3>
              <p className="text-secondary" style={{ fontSize: '0.95rem', marginTop: '0.25rem' }}>Customer Savings</p>
            </div>
            <div>
              <h3 style={{ fontSize: '2.5rem', color: 'var(--color-indigo)' }}>8.4 Tons</h3>
              <p className="text-secondary" style={{ fontSize: '0.95rem', marginTop: '0.25rem' }}>CO₂ Emissions Prevented</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works" style={{ marginTop: '5rem' }}>
        <div className="container">
          <h2 style={{ textAlign: 'center', fontSize: '2.2rem', marginBottom: '3rem' }}>How It Works</h2>
          
          <div style={{ display: 'flex', gap: '2rem', justifyContent: 'space-between', flexWrap: 'wrap' }}>
            <div className="glass-card" style={{ flex: '1 1 300px', textAlign: 'center', padding: '2.5rem 1.5rem' }}>
              <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
                <ShoppingBag className="text-emerald" size={28} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.75rem' }}>1. Find Unsold Surplus</h3>
              <p className="text-secondary" style={{ fontSize: '0.9rem' }}>
                Restaurants upload their safe, delicious unsold items with original vs. discounted prices and quantities.
              </p>
            </div>

            <div className="glass-card" style={{ flex: '1 1 300px', textAlign: 'center', padding: '2.5rem 1.5rem' }}>
              <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'rgba(245, 158, 11, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
                <Clock className="text-amber" size={28} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.75rem' }}>2. Reserve Instantly</h3>
              <p className="text-secondary" style={{ fontSize: '0.9rem' }}>
                Browse listings near you, reserve your favorite bag or dish, and lock in the collection price instantly.
              </p>
            </div>

            <div className="glass-card" style={{ flex: '1 1 300px', textAlign: 'center', padding: '2.5rem 1.5rem' }}>
              <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'rgba(99, 102, 241, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
                <ShieldCheck className="text-indigo" size={28} />
              </div>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '0.75rem' }}>3. Pick Up at Restaurant</h3>
              <p className="text-secondary" style={{ fontSize: '0.9rem' }}>
                Walk into the restaurant during their specified pickup window, show your reservation receipt, and enjoy!
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Interactive styles for landing page */}
      <style>{`
        @media (max-width: 768px) {
          .stats-section .glass-panel {
            grid-template-columns: 1fr !important;
            gap: 1.5rem;
          }
          .stats-section .glass-panel div {
            border: none !important;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--glass-border) !important;
          }
          .stats-section .glass-panel div:last-child {
            border-bottom: none !important;
            padding-bottom: 0;
          }
          h1 {
            font-size: 2.2rem !important;
          }
        }
      `}</style>
    </div>
  );
};

export default LandingPage;
