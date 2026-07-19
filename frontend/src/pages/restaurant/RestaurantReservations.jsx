import { useState, useEffect } from 'react';
import api from '../../services/api';
import { ClipboardCheck, Phone, Check, X, ShieldCheck, Ticket } from 'lucide-react';

const RestaurantReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

  // Token Verification Modal states
  const [verifyingOrder, setVerifyingOrder] = useState(null);
  const [tokenInput, setTokenInput] = useState('');
  const [verifyLoading, setVerifyLoading] = useState(false);
  const [verifySuccess, setVerifySuccess] = useState(false);

  const fetchReservations = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const { data } = await api.get('/restaurant/reservations');
      setReservations(data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to fetch reservations list');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReservations();
  }, []);

  const handleOpenVerifyModal = (order) => {
    setVerifyingOrder(order);
    setTokenInput('');
    setVerifySuccess(false);
    setErrorMsg('');
  };

  const handleVerifyTokenSubmit = async (e) => {
    e.preventDefault();
    setVerifyLoading(true);
    setErrorMsg('');

    try {
      await api.post(`/restaurant/reservations/${verifyingOrder._id}/verify`, {
        token: tokenInput.replace(/\s/g, '') // remove spaces
      });

      setVerifySuccess(true);
      setTimeout(() => {
        setVerifyingOrder(null);
        fetchReservations(); // Refresh list to reflect collected status
      }, 1500);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Verification failed. Please verify the code.');
    } finally {
      setVerifyLoading(false);
    }
  };

  const handleCancelOrder = async (reservationId) => {
    if (!window.confirm('Cancel this reservation and release the items back to inventory?')) return;
    
    setErrorMsg('');
    try {
      await api.put(`/restaurant/reservations/${reservationId}`, { status: 'cancelled' });
      fetchReservations(); // Refresh list
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Status update failed');
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'reserved':
        return <span className="badge badge-warning">Reserved (Paid)</span>;
      case 'collected':
        return <span className="badge badge-success">Collected</span>;
      case 'cancelled':
        return <span className="badge badge-danger">Cancelled</span>;
      default:
        return <span className="badge">{status}</span>;
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      <header style={{ marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>Customer Reservations</h1>
        <p className="text-secondary">Verify customer collection OTP codes, claim reservation payouts, and track pickup history.</p>
      </header>

      {errorMsg && !verifyingOrder && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
          Retrieving active bookings...
        </div>
      ) : reservations.length === 0 ? (
        <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          <ClipboardCheck size={40} style={{ margin: '0 auto 1rem auto', opacity: 0.3 }} />
          <p>No reservations recorded yet.</p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Receipt / Date</th>
                <th>Customer Contact</th>
                <th>Surplus Item</th>
                <th>Quantity</th>
                <th>Price Paid</th>
                <th>Status</th>
                <th style={{ textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reservations.map((res) => (
                <tr key={res._id}>
                  {/* Receipt Code & Date */}
                  <td>
                    <div style={{ fontWeight: 600 }} className="text-indigo">
                      #{res.paymentDetails?.transactionId || res._id.substring(res._id.length - 8).toUpperCase()}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                      {new Date(res.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </td>

                  {/* Customer Info */}
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                      <span style={{ fontWeight: 500 }}>{res.customer?.name || 'Unknown User'}</span>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Phone size={10} /> {res.customer?.phoneNumber || 'No phone'}
                      </span>
                    </div>
                  </td>

                  {/* Food Item */}
                  <td>
                    <span style={{ fontWeight: 500 }}>{res.foodItem?.name || 'Deleted Listing'}</span>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                      Window: {res.foodItem?.pickupStartTime} - {res.foodItem?.pickupEndTime}
                    </div>
                  </td>

                  {/* Qty */}
                  <td>{res.quantity}</td>

                  {/* Price */}
                  <td style={{ fontWeight: 600 }} className="text-emerald">
                    ${res.totalPrice.toFixed(2)}
                  </td>

                  {/* Status */}
                  <td>{getStatusBadge(res.status)}</td>

                  {/* Actions */}
                  <td style={{ textAlign: 'right' }}>
                    {res.status === 'reserved' ? (
                      <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                        <button 
                          onClick={() => handleOpenVerifyModal(res)}
                          className="btn btn-primary btn-sm"
                          style={{ padding: '0.35rem 0.75rem', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.8rem' }}
                          title="Verify Code"
                        >
                          <Ticket size={12} /> Claim Food
                        </button>
                        <button 
                          onClick={() => handleCancelOrder(res._id)}
                          className="btn btn-secondary btn-sm"
                          style={{ padding: '0.35rem 0.5rem', display: 'flex', alignItems: 'center', color: 'var(--color-danger)', borderColor: 'rgba(239, 68, 68, 0.2)' }}
                          title="Cancel Booking & Refund"
                        >
                          <X size={12} />
                        </button>
                      </div>
                    ) : (
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        Processed
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Claim / Verify Token Modal Overlay */}
      {verifyingOrder && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '400px' }}>
            <button className="modal-close" onClick={() => setVerifyingOrder(null)}>×</button>
            
            <h3 style={{ fontSize: '1.4rem', marginBottom: '1.25rem', fontFamily: 'var(--font-display)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Ticket className="text-emerald" /> Claim Food Order
            </h3>

            {verifySuccess ? (
              <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
                <div style={{ width: '55px', height: '55px', borderRadius: '50%', background: 'var(--color-primary-glow)', display: 'flex', alignItems: 'center', justify: 'center', margin: '0 auto 1rem auto' }}>
                  <ShieldCheck className="text-emerald" size={28} />
                </div>
                <h4 className="text-emerald" style={{ marginBottom: '0.5rem' }}>Token Verified!</h4>
                <p className="text-secondary" style={{ fontSize: '0.9rem' }}>The food order has been successfully claimed and marked as collected.</p>
              </div>
            ) : (
              <form onSubmit={handleVerifyTokenSubmit}>
                <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
                  <p><strong>Item:</strong> {verifyingOrder.foodItem?.name}</p>
                  <p><strong>Qty:</strong> {verifyingOrder.quantity} | <strong>Amount:</strong> ${verifyingOrder.totalPrice.toFixed(2)}</p>
                  <p className="text-secondary" style={{ fontSize: '0.8rem', marginTop: '0.4rem' }}><strong>Customer:</strong> {verifyingOrder.customer?.name}</p>
                </div>

                {errorMsg && (
                  <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                    {errorMsg}
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label" style={{ textAlign: 'center', display: 'block' }}>Enter Customer Collection OTP</label>
                  <input 
                    type="text" 
                    maxLength="6"
                    required
                    placeholder="000 000"
                    className="form-control"
                    style={{ textAlign: 'center', fontSize: '1.5rem', letterSpacing: '4px', fontWeight: 'bold', width: '100%' }}
                    value={tokenInput}
                    onChange={(e) => setTokenInput(e.target.value.replace(/\D/g, ''))} // digits only
                  />
                </div>

                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1.5rem', justifyContent: 'flex-end' }}>
                  <button type="button" className="btn btn-secondary btn-sm" onClick={() => setVerifyingOrder(null)}>Cancel</button>
                  <button type="submit" className="btn btn-primary btn-sm" disabled={verifyLoading}>
                    {verifyLoading ? 'Verifying...' : 'Verify OTP'}
                  </button>
                </div>
              </form>
            )}

          </div>
        </div>
      )}

    </div>
  );
};

export default RestaurantReservations;
