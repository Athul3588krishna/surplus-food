import { useState, useEffect, useRef } from 'react';
import api from '../../services/api';
import { ClipboardCheck, Phone, Check, X, ShieldCheck, Ticket, QrCode, Camera, Bell } from 'lucide-react';
import { Html5Qrcode } from 'html5-qrcode';
import { io } from 'socket.io-client';

const RestaurantReservations = () => {
  const [reservations, setReservations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [liveAlert, setLiveAlert] = useState(null);

  // Token Verification Modal states
  const [verifyingOrder, setVerifyingOrder] = useState(null);
  const [tokenInput, setTokenInput] = useState('');
  const [verifyLoading, setVerifyLoading] = useState(false);
  const [verifySuccess, setVerifySuccess] = useState(false);

  // QR Scanner Modal states
  const [scannerOpen, setScannerOpen] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);
  const [manualQrInput, setManualQrInput] = useState('');
  const [scanLoading, setScanLoading] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [scanError, setScanError] = useState('');

  const html5QrCodeRef = useRef(null);

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

    // Socket.io for live reservation updates
    const socket = io('http://localhost:5000');

    socket.on('new_reservation', (data) => {
      setLiveAlert(`🔔 New Order from ${data.customerName} for ${data.quantity}x ${data.itemName}! OTP Token: ${data.token}`);
      fetchReservations(); // Live update table
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Handle QR Camera Scanner initialization & cleanup
  useEffect(() => {
    if (scannerOpen && !scanResult) {
      const qrRegionId = 'qr-reader-container';
      const html5QrCode = new Html5Qrcode(qrRegionId);
      html5QrCodeRef.current = html5QrCode;

      const config = { fps: 10, qrbox: { width: 220, height: 220 } };

      html5QrCode.start(
        { facingMode: 'environment' },
        config,
        async (decodedText) => {
          // Successfully scanned QR text
          try {
            await html5QrCode.stop();
            setCameraActive(false);
          } catch (e) {
            console.error('Error stopping scanner:', e);
          }
          handleVerifyQRData(decodedText);
        },
        () => {
          // Scan frame tick, ignore error
        }
      ).then(() => {
        setCameraActive(true);
        setScanError('');
      }).catch((err) => {
        console.warn('Unable to start camera scanner:', err);
        setCameraActive(false);
        setScanError('Camera not accessible or permission denied. You can manually enter/paste the QR payload or OTP code below.');
      });

      return () => {
        if (html5QrCodeRef.current && html5QrCodeRef.current.isScanning) {
          html5QrCodeRef.current.stop().catch(err => console.error('Cleanup stop error:', err));
        }
      };
    }
  }, [scannerOpen, scanResult]);

  const closeScannerModal = async () => {
    if (html5QrCodeRef.current && html5QrCodeRef.current.isScanning) {
      try {
        await html5QrCodeRef.current.stop();
      } catch (e) {
        console.error('Stop scanner error:', e);
      }
    }
    setScannerOpen(false);
    setScanResult(null);
    setScanError('');
    setManualQrInput('');
    setCameraActive(false);
  };

  const handleVerifyQRData = async (qrDataString) => {
    if (!qrDataString || !qrDataString.trim()) return;

    setScanLoading(true);
    setScanError('');
    setScanResult(null);

    try {
      const { data } = await api.post('/restaurant/reservations/scan-qr', {
        qrData: qrDataString.trim()
      });

      setScanResult(data.order);
      fetchReservations(); // Refresh list immediately
    } catch (err) {
      setScanError(err.response?.data?.message || 'Failed to verify QR Code. Please ensure the code is valid and unpaid/uncollected.');
    } finally {
      setScanLoading(false);
    }
  };

  const handleManualQrSubmit = (e) => {
    e.preventDefault();
    handleVerifyQRData(manualQrInput);
  };

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
      
      <header style={{ marginBottom: '2.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>Customer Reservations</h1>
          <p className="text-secondary">Scan customer QR codes, verify OTP collection tokens, and complete food pickups.</p>
        </div>

        <button 
          onClick={() => { setScanResult(null); setScanError(''); setScannerOpen(true); }}
          className="btn btn-primary"
          style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem 1.25rem', fontSize: '1rem', fontWeight: 600 }}
        >
          <QrCode size={20} /> Scan Customer QR
        </button>
      </header>

      {/* Live Socket.io Notification Banner */}
      {liveAlert && (
        <div 
          className="animate-fade-in" 
          style={{ 
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(59, 130, 246, 0.15))', 
            border: '1px solid var(--color-primary)', 
            borderRadius: '12px', 
            padding: '1rem 1.25rem', 
            marginBottom: '2rem', 
            display: 'flex', 
            alignItems: 'center', 
            justify: 'space-between',
            boxShadow: '0 4px 16px rgba(16, 185, 129, 0.2)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontWeight: 600, color: 'var(--text-primary)' }}>
            <Bell size={20} className="text-emerald" style={{ animation: 'bounce 1s infinite' }} />
            <span>{liveAlert}</span>
          </div>
          <button 
            className="btn btn-secondary btn-sm" 
            style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
            onClick={() => setLiveAlert(null)}
          >
            Dismiss
          </button>
        </div>
      )}

      {errorMsg && !verifyingOrder && !scannerOpen && (
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

      {/* QR Camera Scanner Modal Overlay */}
      {scannerOpen && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '440px' }}>
            <button className="modal-close" onClick={closeScannerModal}>×</button>

            <h3 style={{ fontSize: '1.4rem', marginBottom: '0.25rem', fontFamily: 'var(--font-display)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Camera className="text-emerald" size={22} /> Scan Customer QR Code
            </h3>
            <p className="text-secondary" style={{ fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              Align the customer's QR code within the camera frame below to automatically complete their order pickup.
            </p>

            {scanResult ? (
              <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'var(--color-primary-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem auto' }}>
                  <ShieldCheck className="text-emerald" size={32} />
                </div>
                <h4 className="text-emerald" style={{ marginBottom: '0.25rem', fontSize: '1.2rem' }}>Order Verified & Completed!</h4>
                
                <div className="glass-panel" style={{ padding: '1rem', margin: '1rem 0', textAlign: 'left', fontSize: '0.9rem' }}>
                  <p><strong>Item:</strong> {scanResult.foodItem?.name || 'Surplus Item'}</p>
                  <p><strong>Customer:</strong> {scanResult.customer?.name || 'Customer'}</p>
                  <p><strong>Quantity:</strong> {scanResult.quantity} | <strong>Paid:</strong> ${scanResult.totalPrice?.toFixed(2)}</p>
                  <p style={{ marginTop: '0.4rem' }}>
                    <span className="badge badge-success">COLLECTED</span>
                  </p>
                </div>

                <button className="btn btn-primary" style={{ width: '100%' }} onClick={() => setScanResult(null)}>
                  Scan Another Code
                </button>
              </div>
            ) : (
              <div>
                {/* Camera Scanner Viewport */}
                <div 
                  id="qr-reader-container" 
                  style={{ 
                    width: '100%', 
                    borderRadius: '12px', 
                    overflow: 'hidden', 
                    background: '#000', 
                    minHeight: '250px',
                    border: '2px solid var(--color-primary)'
                  }}
                />

                {scanLoading && (
                  <div style={{ textAlign: 'center', padding: '1rem', color: 'var(--color-primary)', fontWeight: 600 }}>
                    Verifying scanned QR code...
                  </div>
                )}

                {scanError && (
                  <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', margin: '1rem 0', textTransform: 'none', display: 'block', textAlign: 'center', fontSize: '0.85rem' }}>
                    {scanError}
                  </div>
                )}

                {/* Manual fallback input */}
                <form onSubmit={handleManualQrSubmit} style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid var(--glass-border)' }}>
                  <label className="form-label" style={{ fontSize: '0.8rem', marginBottom: '0.3rem', color: 'var(--text-secondary)' }}>
                    Manual Code / Scanned Text Entry
                  </label>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="Paste QR payload or OTP token" 
                      value={manualQrInput} 
                      onChange={(e) => setManualQrInput(e.target.value)}
                      style={{ fontSize: '0.85rem' }}
                    />
                    <button type="submit" className="btn btn-secondary btn-sm" disabled={scanLoading || !manualQrInput.trim()}>
                      Submit
                    </button>
                  </div>
                </form>

                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.25rem' }}>
                  <button type="button" className="btn btn-secondary btn-sm" onClick={closeScannerModal}>
                    Close Scanner
                  </button>
                </div>
              </div>
            )}
          </div>
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
