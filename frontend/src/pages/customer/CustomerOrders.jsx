import { useState, useEffect } from 'react';
import api from '../../services/api';
import { ClipboardList, Clock, AlertTriangle, Star, Check, XCircle } from 'lucide-react';

const CustomerOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  // Review states
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  const fetchOrders = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const { data } = await api.get('/customer/orders');
      setOrders(data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to fetch reservation history');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm('Are you sure you want to cancel this reservation?')) return;
    
    setErrorMsg('');
    try {
      await api.put(`/customer/reservations/${orderId}/cancel`);
      fetchOrders(); // Refresh status
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to cancel reservation');
    }
  };

  const handleOpenReview = (order) => {
    setSelectedOrder(order);
    setRating(5);
    setComment('');
    setReviewSuccess(false);
    setErrorMsg('');
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    setReviewLoading(true);
    setErrorMsg('');

    try {
      await api.post('/customer/rate', {
        orderId: selectedOrder._id,
        rating,
        comment
      });
      setReviewSuccess(true);
      setTimeout(() => {
        setSelectedOrder(null);
        fetchOrders(); // Refresh isRated flag
      }, 1500);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to submit review');
    } finally {
      setReviewLoading(false);
    }
  };

  // Filter orders
  const activeReservations = orders.filter(o => o.status === 'reserved');
  const pastOrders = orders.filter(o => o.status === 'collected' || o.status === 'cancelled');

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      <header style={{ marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>My Reservations</h1>
        <p className="text-secondary">Track your active bookings, view pickup locations, and see your collection history.</p>
      </header>

      {errorMsg && !selectedOrder && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
          Loading your reservation history...
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '2rem' }} className="orders-grid">
          
          {/* Active Reservations Column */}
          <div>
            <h2 style={{ fontSize: '1.4rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Clock className="text-emerald" size={20} /> Active Reservations
            </h2>

            {activeReservations.length === 0 ? (
              <div className="glass-panel" style={{ padding: '3rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                <ClipboardList size={32} style={{ margin: '0 auto 1rem auto', opacity: 0.3 }} />
                <p>No active reservations.</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {activeReservations.map((order) => (
                  <div key={order._id} className="glass-panel" style={{ padding: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                      <div>
                        <span className="badge badge-warning" style={{ marginBottom: '0.5rem' }}>Reserved</span>
                        <h3 style={{ fontSize: '1.15rem' }}>{order.foodItem.name}</h3>
                        <p className="text-emerald" style={{ fontWeight: 600, fontSize: '0.9rem', margin: '0.25rem 0' }}>{order.restaurant.restaurantName}</p>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <p style={{ fontSize: '1.25rem', fontWeight: 800 }}>${order.totalPrice.toFixed(2)}</p>
                        <p className="text-muted" style={{ fontSize: '0.8rem' }}>Qty: {order.quantity}</p>
                      </div>
                    </div>

                    <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: 'var(--border-radius-sm)', border: '1px solid var(--glass-border)', margin: '1rem 0 1.25rem 0', fontSize: '0.85rem' }}>
                      <p style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.4rem' }} className="text-secondary">
                        <strong>Pickup Window:</strong> {order.foodItem.pickupStartTime} - {order.foodItem.pickupEndTime}
                      </p>
                      <p style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }} className="text-secondary">
                        <strong>Store Address:</strong> {order.restaurant.address}
                      </p>
                      <p style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginTop: '0.4rem' }} className="text-muted">
                        <strong>Reservation ID:</strong> {order._id.substring(order._id.length - 8).toUpperCase()}
                      </p>
                    </div>

                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <p style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }} className="text-amber">
                        <AlertTriangle size={14} /> Pay at restaurant upon collection.
                      </p>
                      <button 
                        onClick={() => handleCancelOrder(order._id)}
                        className="btn btn-danger btn-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Past Orders Column */}
          <div>
            <h2 style={{ fontSize: '1.4rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ClipboardList className="text-secondary" size={20} /> Past Activity
            </h2>

            {pastOrders.length === 0 ? (
              <div className="glass-panel" style={{ padding: '3rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
                <p>No historical transactions found.</p>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {pastOrders.map((order) => {
                  const isCollected = order.status === 'collected';
                  return (
                    <div key={order._id} className="glass-panel" style={{ padding: '1.25rem', borderLeft: isCollected ? '3px solid var(--color-primary)' : '3px solid var(--color-danger)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <p style={{ fontSize: '0.85rem', fontWeight: 600, margin: 0 }}>{order.foodItem.name}</p>
                          <p className="text-muted" style={{ fontSize: '0.75rem' }}>{order.restaurant.restaurantName}</p>
                        </div>
                        <div style={{ textAlign: 'right' }}>
                          <span className={`badge ${isCollected ? 'badge-success' : 'badge-danger'}`} style={{ fontSize: '0.65rem' }}>
                            {order.status}
                          </span>
                          <p style={{ fontSize: '0.9rem', fontWeight: 700, marginTop: '0.2rem' }}>${order.totalPrice.toFixed(2)}</p>
                        </div>
                      </div>

                      {/* Review Action */}
                      {isCollected && (
                        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.75rem', borderTop: '1px solid var(--glass-border)', paddingTop: '0.75rem' }}>
                          {order.isRated ? (
                            <span className="badge badge-info" style={{ fontSize: '0.65rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                              <Star size={10} fill="currentColor" /> Reviewed
                            </span>
                          ) : (
                            <button 
                              onClick={() => handleOpenReview(order)}
                              className="btn btn-secondary btn-sm"
                              style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
                            >
                              Leave Review
                            </button>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </div>
      )}

      {/* Review & Rating Modal */}
      {selectedOrder && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button className="modal-close" onClick={() => setSelectedOrder(null)}>×</button>
            
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.25rem', fontFamily: 'var(--font-display)' }}>Rate Restaurant</h3>
            
            {reviewSuccess ? (
              <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
                <div style={{ width: '50px', height: '50px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem auto' }}>
                  <Check className="text-emerald" size={28} />
                </div>
                <h4 className="text-emerald" style={{ marginBottom: '0.5rem' }}>Thank You!</h4>
                <p className="text-secondary" style={{ fontSize: '0.9rem' }}>Your feedback has been saved and shared.</p>
              </div>
            ) : (
              <form onSubmit={handleReviewSubmit}>
                <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1.5rem' }}>
                  <h4 style={{ fontSize: '1rem' }}>{selectedOrder.foodItem.name}</h4>
                  <p className="text-emerald" style={{ fontWeight: 600, fontSize: '0.85rem' }}>{selectedOrder.restaurant.restaurantName}</p>
                </div>

                {errorMsg && (
                  <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                    {errorMsg}
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label" style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Rating Score</span>
                    <span className="text-amber" style={{ display: 'flex', alignItems: 'center', gap: '0.2rem', fontWeight: 600 }}>
                      <Star size={14} fill="currentColor" /> {rating} / 5
                    </span>
                  </label>
                  
                  {/* Star selector */}
                  <div style={{ display: 'flex', gap: '0.5rem', margin: '0.5rem 0' }}>
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: star <= rating ? 'var(--color-accent)' : 'var(--text-muted)' }}
                        onClick={() => setRating(star)}
                      >
                        <Star size={28} fill={star <= rating ? 'currentColor' : 'none'} />
                      </button>
                    ))}
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Review Comment (Optional)</label>
                  <textarea 
                    placeholder="Share your experience (food quality, collection process, friendliness)..." 
                    className="form-control" 
                    rows="3"
                    style={{ fontFamily: 'var(--font-body)', resize: 'none' }}
                    value={comment} 
                    onChange={(e) => setComment(e.target.value)} 
                  />
                </div>

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1.5rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                  <button type="button" className="btn btn-secondary btn-sm" onClick={() => setSelectedOrder(null)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm" disabled={reviewLoading}>
                    {reviewLoading ? 'Submitting...' : 'Submit'}
                  </button>
                </div>
              </form>
            )}

          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .orders-grid {
            grid-template-columns: 1fr !important;
            gap: 2rem;
          }
        }
      `}</style>
    </div>
  );
};

export default CustomerOrders;
