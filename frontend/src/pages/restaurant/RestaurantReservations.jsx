import { useState, useEffect } from 'react';
import api from '../../services/api';
import { ClipboardCheck, User, Phone, ShoppingBag, Calendar, Check, X, AlertCircle } from 'lucide-react';

const RestaurantReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

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

  const handleUpdateStatus = async (reservationId, newStatus) => {
    const confirmationText = newStatus === 'collected' 
      ? 'Confirm that the customer has collected and paid for this item?' 
      : 'Cancel this reservation and release the items back to inventory?';
      
    if (!window.confirm(confirmationText)) return;

    setErrorMsg('');
    try {
      await api.put(`/restaurant/reservations/${reservationId}`, { status: newStatus });
      fetchReservations(); // Refresh list
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Status update failed');
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'reserved':
        return <span className="badge badge-warning">Reserved</span>;
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
        <p className="text-secondary">Verify customer IDs, process payments upon collection, and track listing allocations.</p>
      </header>

      {errorMsg && (
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
                <th>Price Due</th>
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
                      #{res._id.substring(res._id.length - 8).toUpperCase()}
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
                          onClick={() => handleUpdateStatus(res._id, 'collected')}
                          className="btn btn-primary btn-sm"
                          style={{ padding: '0.35rem 0.75rem', display: 'flex', alignItems: 'center', gap: '0.25rem', fontSize: '0.8rem' }}
                          title="Mark as Collected"
                        >
                          <Check size={12} /> Collect
                        </button>
                        <button 
                          onClick={() => handleUpdateStatus(res._id, 'cancelled')}
                          className="btn btn-secondary btn-sm"
                          style={{ padding: '0.35rem 0.5rem', display: 'flex', alignItems: 'center', color: 'var(--color-danger)', borderColor: 'rgba(239, 68, 68, 0.2)' }}
                          title="Cancel Reservation"
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
    </div>
  );
};

export default RestaurantReservations;
