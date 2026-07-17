import { useState, useEffect } from 'react';
import api from '../../services/api';
import { Shield, Users, Store, HeartHandshake, BadgeDollarSign, ShieldAlert, Sparkles, Trash2 } from 'lucide-react';

const AdminDashboard = () => {
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [cleanupResult, setCleanupResult] = useState('');
  const [cleanupLoading, setCleanupLoading] = useState(false);

  const fetchDashboardData = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const [statsRes, usersRes] = await Promise.all([
        api.get('/admin/analytics'),
        api.get('/admin/users')
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to fetch administrator data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleCleanupExpired = async () => {
    if (!window.confirm('Scan database and delete all expired listings?')) return;
    
    setCleanupLoading(true);
    setCleanupResult('');
    try {
      const { data } = await api.delete('/admin/listings/expired');
      setCleanupResult(`Success: Deleted ${data.deletedCount} expired food items.`);
      fetchDashboardData(); // Refresh analytics
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Housekeeping failed');
    } finally {
      setCleanupLoading(false);
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Shield className="text-indigo" /> Admin Panel
          </h1>
          <p className="text-secondary">Verify restaurants, monitor food posts, and track system metrics.</p>
        </div>

        <button 
          onClick={handleCleanupExpired}
          className="btn btn-danger btn-sm"
          disabled={cleanupLoading}
          style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
        >
          <Trash2 size={14} /> {cleanupLoading ? 'Cleaning...' : 'Clear Expired Listings'}
        </button>
      </header>

      {/* Housekeeping notifications */}
      {cleanupResult && (
        <div className="badge badge-success animate-fade-in" style={{ width: '100%', padding: '1rem', marginBottom: '1.5rem', textTransform: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}>
          <Sparkles size={16} /> {cleanupResult}
        </div>
      )}

      {errorMsg && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
          Loading system database stats...
        </div>
      ) : (
        <>
          {/* Analytics Stats Grid */}
          {stats && (
            <section style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '3rem' }} className="analytics-grid">
              
              <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ padding: '0.6rem', borderRadius: 'var(--border-radius-sm)', background: 'var(--color-primary-glow)' }}>
                  <BadgeDollarSign className="text-emerald" size={22} />
                </div>
                <div>
                  <p className="text-muted" style={{ fontSize: '0.75rem', fontWeight: 600 }}>Total Saved Sales</p>
                  <h3 style={{ fontSize: '1.35rem' }}>${stats.totalSales.toFixed(2)}</h3>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ padding: '0.6rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(99, 102, 241, 0.1)' }}>
                  <HeartHandshake className="text-indigo" size={22} />
                </div>
                <div>
                  <p className="text-muted" style={{ fontSize: '0.75rem', fontWeight: 600 }}>Meals Rescued</p>
                  <h3 style={{ fontSize: '1.35rem' }}>{stats.totalMealsSaved}</h3>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ padding: '0.6rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(255, 255, 255, 0.05)' }}>
                  <Users className="text-secondary" size={22} />
                </div>
                <div>
                  <p className="text-muted" style={{ fontSize: '0.75rem', fontWeight: 600 }}>Customers</p>
                  <h3 style={{ fontSize: '1.35rem' }}>{stats.totalCustomers}</h3>
                </div>
              </div>

              <div className="glass-panel" style={{ padding: '1.25rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ padding: '0.6rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(245, 158, 11, 0.1)' }}>
                  <Store className="text-amber" size={22} />
                </div>
                <div>
                  <p className="text-muted" style={{ fontSize: '0.75rem', fontWeight: 600 }}>Verified Stores</p>
                  <h3 style={{ fontSize: '1.35rem' }}>
                    {stats.verifiedRestaurants} <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>({stats.pendingRestaurants} pending)</span>
                  </h3>
                </div>
              </div>

            </section>
          )}

          {/* Pending Verifications Alert */}
          {stats && stats.pendingRestaurants > 0 && (
            <div className="glass-panel" style={{ padding: '1.25rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', border: '1px solid rgba(245, 158, 11, 0.3)', background: 'rgba(245, 158, 11, 0.02)', marginBottom: '3rem', flexWrap: 'wrap', gap: '1rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <ShieldAlert className="text-amber" size={24} />
                <div>
                  <h4 style={{ fontSize: '1rem' }}>Pending Restaurant Verifications</h4>
                  <p className="text-secondary" style={{ fontSize: '0.85rem' }}>There are {stats.pendingRestaurants} store profile audits awaiting admin validation.</p>
                </div>
              </div>
              <a href="/admin/verifications" className="btn btn-indigo btn-sm" style={{ textDecoration: 'none' }}>
                Verify Profiles
              </a>
            </div>
          )}

          {/* User Account Registry */}
          <div>
            <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>User Registry</h2>
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Registration Date</th>
                    <th>User Name</th>
                    <th>Email Address</th>
                    <th>Phone</th>
                    <th>Role</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u._id}>
                      <td>{new Date(u.createdAt).toLocaleDateString()}</td>
                      <td style={{ fontWeight: 600 }}>{u.name}</td>
                      <td>{u.email}</td>
                      <td>{u.phoneNumber || 'N/A'}</td>
                      <td>
                        <span className={`badge ${u.role === 'admin' ? 'badge-danger' : u.role === 'restaurant' ? 'badge-info' : 'badge-success'}`} style={{ fontSize: '0.65rem' }}>
                          {u.role}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

      <style>{`
        @media (max-width: 900px) {
          .analytics-grid {
            grid-template-columns: 1fr 1fr !important;
          }
        }
        @media (max-width: 480px) {
          .analytics-grid {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  );
};

export default AdminDashboard;
