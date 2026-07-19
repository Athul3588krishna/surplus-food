import { useState, useEffect } from 'react';
import api from '../../services/api';
import { Search, MapPin, Clock, ShoppingBag, Utensils, Star, Check, CreditCard, ShieldCheck } from 'lucide-react';

const CustomerDashboard = () => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  
  // Search & Filter state
  const [search, setSearch] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  // Modal Reservation states
  const [selectedItem, setSelectedItem] = useState(null);
  const [reserveQty, setReserveQty] = useState(1);
  const [reserveLoading, setReserveLoading] = useState(false);
  const [checkoutStep, setCheckoutStep] = useState('details'); // details, payment, success
  const [generatedToken, setGeneratedToken] = useState('');

  // Mock card inputs
  const [cardName, setCardName] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [cardExpiry, setCardExpiry] = useState('');
  const [cardCvv, setCardCvv] = useState('');

  const fetchListings = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const params = {};
      if (search) params.search = search;
      if (cuisine) params.cuisine = cuisine;
      if (maxPrice) params.maxPrice = maxPrice;

      const { data } = await api.get('/customer/listings', { params });
      setListings(data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to retrieve food listings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      fetchListings();
    }, 400);

    return () => clearTimeout(delayDebounce);
  }, [search, cuisine, maxPrice]);

  const handleOpenReserve = (item) => {
    setSelectedItem(item);
    setReserveQty(1);
    setCheckoutStep('details');
    setGeneratedToken('');
    setCardName('');
    setCardNumber('');
    setCardExpiry('');
    setCardCvv('');
    setErrorMsg('');
  };

  const handleProceedToPayment = (e) => {
    e.preventDefault();
    setCheckoutStep('payment');
  };

  const handleReserveSubmit = async (e) => {
    e.preventDefault();
    setReserveLoading(true);
    setErrorMsg('');

    try {
      // Extract last 4 digits of simulated card
      const last4 = cardNumber.replace(/\s/g, '').slice(-4) || '4242';

      const { data } = await api.post('/customer/reservations', {
        foodItemId: selectedItem._id,
        quantity: reserveQty,
        cardLast4: last4
      });
      
      setGeneratedToken(data.token);
      setCheckoutStep('success');
      
      // Refresh inventory behind modal
      fetchListings();
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Reservation failed. Please try again.');
    } finally {
      setReserveLoading(false);
    }
  };

  const formatCardNumber = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || '';
    const parts = [];

    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }

    if (parts.length > 0) {
      return parts.join(' ');
    } else {
      return v;
    }
  };

  const formatExpiry = (value) => {
    const v = value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
    if (v.length >= 2) {
      return `${v.slice(0, 2)}/${v.slice(2, 4)}`;
    }
    return v;
  };

  // Unique list of cuisines for filtering
  const cuisinesList = ['Bakeries', 'Café & Coffee', 'Fast Food', 'Indian', 'Italian', 'Chinese', 'Sushi', 'Desserts'];

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      {/* Header */}
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>Rescue Surplus Near You</h1>
        <p className="text-secondary">Save delicious meals from going to waste at 50% to 80% off original prices.</p>
      </header>

      {/* Search and Filters Bar */}
      <section className="glass-panel" style={{ padding: '1.5rem', marginBottom: '2.5rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '1rem', flexWrap: 'wrap' }} className="filters-grid">
          
          {/* Search */}
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
            <input 
              type="text" 
              placeholder="Search food items (e.g. Sourdough, Box, Croissant)..." 
              className="form-control" 
              style={{ paddingLeft: '2.75rem', width: '100%' }}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          {/* Cuisine Selector */}
          <div>
            <select 
              className="form-control form-select" 
              style={{ width: '100%' }}
              value={cuisine}
              onChange={(e) => setCuisine(e.target.value)}
            >
              <option value="">All Cuisines</option>
              {cuisinesList.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Max Price filter */}
          <div>
            <input 
              type="number" 
              placeholder="Max Price ($)" 
              className="form-control" 
              style={{ width: '100%' }}
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              min="0"
            />
          </div>

        </div>
      </section>

      {/* Error state */}
      {errorMsg && !selectedItem && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {/* Grid of Listings */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
          Finding delicious options...
        </div>
      ) : listings.length === 0 ? (
        <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <ShoppingBag size={48} style={{ margin: '0 auto 1rem auto', opacity: 0.4 }} className="text-muted" />
          <h3>No Surplus Food Found</h3>
          <p className="text-muted" style={{ marginTop: '0.5rem' }}>Try adjusting your search terms or filters.</p>
        </div>
      ) : (
        <div className="grid-cols-3">
          {listings.map((item) => {
            const savings = item.originalPrice - item.discountedPrice;
            const savingsPercent = Math.round((savings / item.originalPrice) * 100);
            
            return (
              <div key={item._id} className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                {/* Image or Placeholder */}
                {item.imagePath ? (
                  <img src={`http://localhost:5000${item.imagePath}`} alt={item.name} className="card-img" />
                ) : (
                  <div className="card-img-placeholder">
                    <Utensils size={32} />
                  </div>
                )}

                {/* Content */}
                <div style={{ flexGrow: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.2rem' }}>{item.name}</h3>
                    <span className="badge badge-danger">{savingsPercent}% OFF</span>
                  </div>

                  <p className="text-emerald" style={{ fontSize: '0.85rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.25rem', marginBottom: '0.75rem' }}>
                    <Star size={14} fill="currentColor" /> {item.restaurant.rating} ({item.restaurant.ratingCount} ratings)
                  </p>

                  <p className="text-secondary" style={{ fontSize: '0.9rem', marginBottom: '1rem', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {item.description || 'No description provided.'}
                  </p>
                  
                  {/* Restaurant details */}
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', borderTop: '1px solid var(--glass-border)', paddingTop: '0.75rem', marginBottom: '1rem' }}>
                    <p style={{ fontSize: '0.85rem', fontWeight: 600 }} className="text-emerald">{item.restaurant.restaurantName}</p>
                    <p style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }} className="text-secondary">
                      <MapPin size={12} /> {item.restaurant.address}
                    </p>
                    <p style={{ fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.3rem' }} className="text-secondary">
                      <Clock size={12} /> Pickup: {item.pickupStartTime} - {item.pickupEndTime}
                    </p>
                  </div>
                </div>

                {/* Footer / Pricing & Action */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem', marginTop: 'auto' }}>
                  <div>
                    <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)' }}>${item.discountedPrice.toFixed(2)}</span>
                    <span style={{ textDecoration: 'line-through', fontSize: '0.85rem', color: 'var(--text-muted)', marginLeft: '0.5rem' }}>${item.originalPrice.toFixed(2)}</span>
                  </div>

                  <button 
                    onClick={() => handleOpenReserve(item)}
                    className="btn btn-primary btn-sm"
                  >
                    Reserve ({item.quantity})
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Reservation & Payment Modal Overlay */}
      {selectedItem && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '480px' }}>
            <button className="modal-close" onClick={() => setSelectedItem(null)}>×</button>
            
            {/* STEP 1: QUANTITY SELECTOR DETAILS */}
            {checkoutStep === 'details' && (
              <form onSubmit={handleProceedToPayment}>
                <h3 style={{ fontSize: '1.4rem', marginBottom: '1.25rem', fontFamily: 'var(--font-display)' }}>Reserve Surplus Food</h3>
                
                <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1.5rem' }}>
                  <h4 style={{ fontSize: '1.05rem' }}>{selectedItem.name}</h4>
                  <p className="text-emerald" style={{ fontWeight: 600, fontSize: '0.9rem', margin: '0.25rem 0' }}>{selectedItem.restaurant.restaurantName}</p>
                  <p className="text-muted" style={{ fontSize: '0.8rem' }}>Pickup: {selectedItem.pickupStartTime} - {selectedItem.pickupEndTime}</p>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.75rem', fontSize: '0.9rem', fontWeight: 600 }}>
                    <span>Price per item:</span>
                    <span className="text-emerald">${selectedItem.discountedPrice.toFixed(2)}</span>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Select Quantity</label>
                  <select 
                    className="form-control" 
                    value={reserveQty} 
                    onChange={(e) => setReserveQty(Number(e.target.value))}
                  >
                    {[...Array(selectedItem.quantity).keys()].map((q) => (
                      <option key={q + 1} value={q + 1}>{q + 1}</option>
                    ))}
                  </select>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '2rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                  <div>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Subtotal:</p>
                    <p style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                      ${(selectedItem.discountedPrice * reserveQty).toFixed(2)}
                    </p>
                  </div>
                  <button type="submit" className="btn btn-primary btn-sm">
                    Proceed to Payment
                  </button>
                </div>
              </form>
            )}

            {/* STEP 2: CREDIT CARD PAYMENT SIMULATION */}
            {checkoutStep === 'payment' && (
              <form onSubmit={handleReserveSubmit}>
                <h3 style={{ fontSize: '1.4rem', marginBottom: '1.25rem', fontFamily: 'var(--font-display)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CreditCard className="text-emerald" /> Simulated Checkout
                </h3>

                {errorMsg && (
                  <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                    {errorMsg}
                  </div>
                )}

                <div style={{ background: 'linear-gradient(135deg, #1e1b4b 0%, #311042 100%)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px', padding: '1.25rem', marginBottom: '1.5rem', color: '#fff', boxShadow: '0 8px 16px rgba(0,0,0,0.3)' }}>
                  <p style={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.6)', letterSpacing: '0.05em' }}>MOCK CARD SIMULATION</p>
                  <div style={{ fontSize: '1.25rem', letterSpacing: '2px', fontWeight: 'bold', margin: '1rem 0' }}>
                    {cardNumber ? cardNumber : '•••• •••• •••• ••••'}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'rgba(255,255,255,0.8)' }}>
                    <span>{cardName ? cardName.toUpperCase() : 'CARDHOLDER NAME'}</span>
                    <span>{cardExpiry ? cardExpiry : 'MM/YY'}</span>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">Cardholder Name</label>
                  <input 
                    type="text" 
                    required 
                    placeholder="e.g. John Doe"
                    className="form-control"
                    value={cardName}
                    onChange={(e) => setCardName(e.target.value)}
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Card Number</label>
                  <input 
                    type="text" 
                    required 
                    maxLength="19"
                    placeholder="4242 4242 4242 4242"
                    className="form-control"
                    value={cardNumber}
                    onChange={(e) => setCardNumber(formatCardNumber(e.target.value))}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                  <div className="form-group">
                    <label className="form-label">Expiry (MM/YY)</label>
                    <input 
                      type="text" 
                      required 
                      maxLength="5"
                      placeholder="12/29"
                      className="form-control"
                      value={cardExpiry}
                      onChange={(e) => setCardExpiry(formatExpiry(e.target.value))}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">CVV / CVN</label>
                    <input 
                      type="password" 
                      required 
                      maxLength="3"
                      placeholder="•••"
                      className="form-control"
                      value={cardCvv}
                      onChange={(e) => setCardCvv(e.target.value.replace(/\D/g, ''))}
                    />
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                  <div>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Total Cost:</p>
                    <p style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                      ${(selectedItem.discountedPrice * reserveQty).toFixed(2)}
                    </p>
                  </div>

                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button type="button" className="btn btn-secondary btn-sm" onClick={() => setCheckoutStep('details')}>Back</button>
                    <button type="submit" className="btn btn-primary btn-sm" disabled={reserveLoading}>
                      {reserveLoading ? 'Simulating...' : 'Simulate Pay'}
                    </button>
                  </div>
                </div>
              </form>
            )}

            {/* STEP 3: MOCK PAYMENT & OTP TOKEN GENERATION SUCCESS */}
            {checkoutStep === 'success' && (
              <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'var(--color-primary-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem auto' }}>
                  <ShieldCheck className="text-emerald" size={32} />
                </div>
                
                <h3 className="text-emerald" style={{ fontSize: '1.5rem', fontFamily: 'var(--font-display)', marginBottom: '0.5rem' }}>Simulated Payment Approved!</h3>
                <p className="text-secondary" style={{ fontSize: '0.9rem', marginBottom: '1.5rem' }}>
                  Your reservation is confirmed. Give this OTP token to the hotel to collect your food:
                </p>

                {/* Big Verification Token Code */}
                <div style={{ margin: '1.5rem 0', padding: '1rem 0', background: 'rgba(16, 185, 129, 0.1)', border: '1px dashed var(--color-primary)', borderRadius: '12px' }}>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', letterSpacing: '1px', marginBottom: '0.25rem' }}>COLLECTION TOKEN (OTP)</p>
                  <span style={{ fontSize: '2.5rem', fontWeight: 800, letterSpacing: '4px', color: 'var(--text-primary)' }}>
                    {generatedToken ? `${generatedToken.slice(0, 3)} ${generatedToken.slice(3, 6)}` : '000 000'}
                  </span>
                </div>

                <div className="badge badge-success" style={{ width: '100%', borderRadius: 'var(--border-radius-sm)', padding: '0.6rem', marginBottom: '1.5rem', textTransform: 'none', display: 'block' }}>
                  Token code emailed via Nodemailer!
                </div>

                <button 
                  type="button" 
                  className="btn btn-primary btn-block" 
                  onClick={() => setSelectedItem(null)}
                >
                  Done
                </button>
              </div>
            )}

          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 768px) {
          .filters-grid {
            grid-template-columns: 1fr !important;
            gap: 0.75rem;
          }
        }
      `}</style>
    </div>
  );
};

export default CustomerDashboard;
