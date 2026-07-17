import { useState, useEffect } from 'react';
import api from '../../services/api';
import { Search, SlidersHorizontal, MapPin, Clock, Save, ShoppingBag, Utensils, Star, Check } from 'lucide-react';

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
  const [reserveSuccess, setReserveSuccess] = useState(false);

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
    setReserveSuccess(false);
    setErrorMsg('');
  };

  const handleReserveSubmit = async (e) => {
    e.preventDefault();
    setReserveLoading(true);
    setErrorMsg('');

    try {
      await api.post('/customer/reservations', {
        foodItemId: selectedItem._id,
        quantity: reserveQty
      });
      setReserveSuccess(true);
      setTimeout(() => {
        setSelectedItem(null);
        fetchListings(); // Refresh inventory
      }, 1500);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Reservation failed. Please try again.');
    } finally {
      setReserveLoading(false);
    }
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

      {/* Reservation Modal Overlay */}
      {selectedItem && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button className="modal-close" onClick={() => setSelectedItem(null)}>×</button>
            
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.25rem', fontFamily: 'var(--font-display)' }}>Reserve Surplus Food</h3>
            
            {reserveSuccess ? (
              <div style={{ textAlign: 'center', padding: '1.5rem 0' }}>
                <div style={{ width: '50px', height: '50px', borderRadius: '50%', background: 'rgba(16, 185, 129, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem auto' }}>
                  <Check className="text-emerald" size={28} />
                </div>
                <h4 className="text-emerald" style={{ marginBottom: '0.5rem' }}>Reservation Successful!</h4>
                <p className="text-secondary" style={{ fontSize: '0.9rem' }}>Go to "My Reservations" to view pickup details.</p>
              </div>
            ) : (
              <form onSubmit={handleReserveSubmit}>
                <div className="glass-panel" style={{ padding: '1rem', marginBottom: '1.5rem' }}>
                  <h4 style={{ fontSize: '1.1rem' }}>{selectedItem.name}</h4>
                  <p className="text-emerald" style={{ fontWeight: 600, fontSize: '0.95rem', margin: '0.25rem 0' }}>{selectedItem.restaurant.restaurantName}</p>
                  <p className="text-muted" style={{ fontSize: '0.85rem' }}>Pickup time: {selectedItem.pickupStartTime} - {selectedItem.pickupEndTime}</p>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.75rem', fontSize: '0.95rem', fontWeight: 600 }}>
                    <span>Discounted Price:</span>
                    <span className="text-emerald">${selectedItem.discountedPrice.toFixed(2)} each</span>
                  </div>
                </div>

                {errorMsg && (
                  <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                    {errorMsg}
                  </div>
                )}

                <div className="form-group">
                  <label className="form-label">Quantity to Reserve</label>
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

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                  <div>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Total Cost (Pay at Store):</p>
                    <p style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                      ${(selectedItem.discountedPrice * reserveQty).toFixed(2)}
                    </p>
                  </div>

                  <div style={{ display: 'flex', gap: '0.75rem' }}>
                    <button type="button" className="btn btn-secondary btn-sm" onClick={() => setSelectedItem(null)}>Cancel</button>
                    <button type="submit" className="btn btn-primary btn-sm" disabled={reserveLoading}>
                      {reserveLoading ? 'Reserving...' : 'Confirm'}
                    </button>
                  </div>
                </div>
              </form>
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
