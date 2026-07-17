import { useState, useEffect } from 'react';
import api from '../../services/api';
import { ShoppingBag, Eye, Calendar, Sparkles, AlertCircle, RefreshCw } from 'lucide-react';

const SystemListings = () => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [cleanupResult, setCleanupResult] = useState('');
  const [cleanupLoading, setCleanupLoading] = useState(false);

  const fetchListings = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const { data } = await api.get('/admin/listings');
      setListings(data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to fetch platform listings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchListings();
  }, []);

  const handleCleanupExpired = async () => {
    if (!window.confirm('Delete all expired surplus food items from the platform database?')) return;
    
    setCleanupLoading(true);
    setCleanupResult('');
    try {
      const { data } = await api.delete('/admin/listings/expired');
      setCleanupResult(`Housekeeping complete: Cleared ${data.deletedCount} expired food items.`);
      fetchListings(); // Refresh list
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to execute database sweep');
    } finally {
      setCleanupLoading(false);
    }
  };

  const getListingStatusBadge = (item) => {
    const isExpired = new Date(item.expiryDate) < new Date();
    
    if (isExpired) {
      return <span className="badge badge-danger">Expired</span>;
    }
    if (item.quantity <= 0 || item.status === 'sold-out') {
      return <span className="badge badge-warning">Sold Out</span>;
    }
    return <span className="badge badge-success">Active</span>;
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <ShoppingBag className="text-emerald" /> Platform Postings
          </h1>
          <p className="text-secondary">Monitor active listings, check expiration clocks, and maintain marketplace health.</p>
        </div>

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button 
            onClick={fetchListings}
            className="btn btn-secondary btn-sm"
            style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}
          >
            <RefreshCw size={12} /> Sync
          </button>
          <button 
            onClick={handleCleanupExpired}
            className="btn btn-danger btn-sm"
            disabled={cleanupLoading}
            style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}
          >
            Sweep Expired ({listings.filter(i => new Date(i.expiryDate) < new Date()).length})
          </button>
        </div>
      </header>

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
          Retrieving all postings from database...
        </div>
      ) : listings.length === 0 ? (
        <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          <ShoppingBag size={40} style={{ margin: '0 auto 1rem auto', opacity: 0.3 }} />
          <p>No listings recorded on the platform yet.</p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Created</th>
                <th>Surplus Food Listing</th>
                <th>Restaurant Store</th>
                <th>Price (Orig / Offer)</th>
                <th>Stock Qty</th>
                <th>Expiration Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {listings.map((item) => (
                <tr key={item._id}>
                  {/* Created date */}
                  <td>{new Date(item.createdAt).toLocaleDateString()}</td>

                  {/* Item Name */}
                  <td style={{ fontWeight: 600 }}>{item.name}</td>

                  {/* Restaurant Name */}
                  <td className="text-indigo" style={{ fontWeight: 500 }}>{item.restaurant?.restaurantName || 'Unknown Store'}</td>

                  {/* Price */}
                  <td>
                    <span style={{ textDecoration: 'line-through', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                      ${item.originalPrice.toFixed(2)}
                    </span>
                    <span className="text-emerald" style={{ fontWeight: 600, marginLeft: '0.5rem' }}>
                      ${item.discountedPrice.toFixed(2)}
                    </span>
                  </td>

                  {/* Stock */}
                  <td>{item.quantity} items</td>

                  {/* Expiration */}
                  <td>
                    <div style={{ fontSize: '0.85rem' }} className={new Date(item.expiryDate) < new Date() ? 'text-rose' : 'text-secondary'}>
                      {new Date(item.expiryDate).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} at {new Date(item.expiryDate).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </td>

                  {/* Status Badge */}
                  <td>{getListingStatusBadge(item)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default SystemListings;
