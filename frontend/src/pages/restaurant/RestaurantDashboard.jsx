import { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, BarChart3, Star, BadgeDollarSign, HeartHandshake, Utensils, Image, Trash2, Edit2, Bell, Clock, ShoppingBag } from 'lucide-react';
import { io } from 'socket.io-client';

// Live Expiry & Pickup Countdown Timer Component
const ExpiryTimer = ({ expiryDate, pickupEndTime }) => {
  const [timeLeft, setTimeLeft] = useState('');
  const [isUrgent, setIsUrgent] = useState(false);
  const [isExpired, setIsExpired] = useState(false);

  useEffect(() => {
    const calculateTime = () => {
      let target = expiryDate ? new Date(expiryDate).getTime() : null;
      if (!target && pickupEndTime) {
        const [hours, minutes] = pickupEndTime.split(':');
        const d = new Date();
        d.setHours(parseInt(hours, 10), parseInt(minutes, 10), 0, 0);
        if (d.getTime() < Date.now()) d.setDate(d.getDate() + 1);
        target = d.getTime();
      }

      if (!target) return;

      const diff = target - Date.now();
      if (diff <= 0) {
        setIsExpired(true);
        setTimeLeft('Expired');
        return;
      }

      setIsExpired(false);
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const secs = Math.floor((diff % (1000 * 60)) / 1000);

      setIsUrgent(diff < 30 * 60 * 1000);

      const pad = (n) => String(n).padStart(2, '0');
      if (hours > 0) {
        setTimeLeft(`${pad(hours)}h ${pad(mins)}m ${pad(secs)}s`);
      } else {
        setTimeLeft(`${pad(mins)}m ${pad(secs)}s`);
      }
    };

    calculateTime();
    const interval = setInterval(calculateTime, 1000);

    return () => clearInterval(interval);
  }, [expiryDate, pickupEndTime]);

  if (isExpired) {
    return (
      <span className="badge badge-danger" style={{ fontSize: '0.65rem', display: 'inline-flex', alignItems: 'center', gap: '0.2rem' }}>
        🔴 Expired
      </span>
    );
  }

  return (
    <span 
      className={`badge ${isUrgent ? 'badge-danger' : 'badge-secondary'}`} 
      style={{ 
        fontSize: '0.65rem', 
        display: 'inline-flex', 
        alignItems: 'center', 
        gap: '0.25rem',
        background: isUrgent ? 'linear-gradient(135deg, #ef4444, #f59e0b)' : 'rgba(255,255,255,0.08)',
        color: '#fff',
        fontWeight: isUrgent ? 700 : 600
      }}
    >
      <Clock size={10} /> {isUrgent ? '🔥 Ending Soon:' : '⏳ Ends In:'} {timeLeft}
    </span>
  );
};

const RestaurantDashboard = () => {
  const [listings, setListings] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [liveNotification, setLiveNotification] = useState(null);

  // Add/Edit Listing Modal states
  const [showModal, setShowModal] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);
  
  // Listing Form states
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [originalPrice, setOriginalPrice] = useState('');
  const [discountedPrice, setDiscountedPrice] = useState('');
  const [quantity, setQuantity] = useState('');
  const [pickupStartTime, setPickupStartTime] = useState('18:00');
  const [pickupEndTime, setPickupEndTime] = useState('21:00');
  const [dietaryType, setDietaryType] = useState('veg');
  const [allergens, setAllergens] = useState([]);
  const [isSurpriseBag, setIsSurpriseBag] = useState(false);
  const [estimatedValue, setEstimatedValue] = useState('');
  const [imageFile, setImageFile] = useState(null);

  const availableAllergens = ['Gluten-Free', 'Dairy-Free', 'Nut-Free', 'Halal'];

  const fetchData = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const [listingsRes, analyticsRes] = await Promise.all([
        api.get('/restaurant/listings'),
        api.get('/restaurant/analytics')
      ]);
      setListings(listingsRes.data);
      setAnalytics(analyticsRes.data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Initialize Socket.io connection for live notifications
    const socket = io('http://localhost:5000');

    socket.on('connect', () => {
      console.log('⚡ Connected to Socket.io server');
    });

    socket.on('new_reservation', (data) => {
      setLiveNotification(`🔔 LIVE RESERVATION: ${data.customerName} reserved ${data.quantity}x ${data.itemName} ($${data.totalPrice.toFixed(2)})! Token: ${data.token}`);
      // Refresh inventory and revenue stats live without page reload
      fetchData();
    });

    socket.on('listings_updated', () => {
      fetchData();
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // Join private room once analytics/profileId is available
  useEffect(() => {
    if (analytics && analytics.profileId) {
      const socket = io('http://localhost:5000');
      socket.emit('join_room', `restaurant_${analytics.profileId}`);
      return () => {
        socket.disconnect();
      };
    }
  }, [analytics?.profileId]);

  const handleOpenAdd = () => {
    setEditingItem(null);
    setName('');
    setDescription('');
    setOriginalPrice('');
    setDiscountedPrice('');
    setQuantity('');
    setPickupStartTime('18:00');
    setPickupEndTime('21:00');
    setDietaryType('veg');
    setAllergens([]);
    setIsSurpriseBag(false);
    setEstimatedValue('');
    setImageFile(null);
    setErrorMsg('');
    setShowModal(true);
  };

  const handleOpenEdit = (item) => {
    setEditingItem(item);
    setName(item.name || '');
    setDescription(item.description || '');
    setOriginalPrice(item.originalPrice || '');
    setDiscountedPrice(item.discountedPrice || '');
    setQuantity(item.quantity || '');
    setPickupStartTime(item.pickupStartTime || '18:00');
    setPickupEndTime(item.pickupEndTime || '21:00');
    setDietaryType(item.dietaryType || 'veg');
    setAllergens(item.allergens || []);
    setIsSurpriseBag(item.isSurpriseBag || false);
    setEstimatedValue(item.estimatedValue || item.originalPrice || '');
    setImageFile(null);
    setErrorMsg('');
    setShowModal(true);
  };

  const handleSurpriseBagToggle = (e) => {
    const checked = e.target.checked;
    setIsSurpriseBag(checked);
    if (checked) {
      if (!name) setName('Daily Surplus Mystery Bag 🎁');
      if (!description) setDescription('A surprise assortment of delicious daily surplus items valued at $15 for just $4.99!');
      if (!originalPrice) setOriginalPrice('15.00');
      if (!discountedPrice) setDiscountedPrice('4.99');
      if (!estimatedValue) setEstimatedValue('15.00');
    }
  };

  const handleAllergenToggle = (tag) => {
    if (allergens.includes(tag)) {
      setAllergens(allergens.filter((t) => t !== tag));
    } else {
      setAllergens([...allergens, tag]);
    }
  };

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  const handleModalSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    const trimmedName = name.trim();
    if (!trimmedName || trimmedName.length < 2) {
      setErrorMsg('Please enter a valid title (at least 2 characters)');
      return;
    }

    const origPriceNum = parseFloat(originalPrice);
    if (isNaN(origPriceNum) || origPriceNum <= 0) {
      setErrorMsg('Original price must be a valid positive amount greater than $0');
      return;
    }

    const discPriceNum = parseFloat(discountedPrice);
    if (isNaN(discPriceNum) || discPriceNum < 0) {
      setErrorMsg('Offer price cannot be negative');
      return;
    }

    if (discPriceNum > origPriceNum) {
      setErrorMsg(`Discounted price ($${discPriceNum.toFixed(2)}) cannot be greater than original price ($${origPriceNum.toFixed(2)})`);
      return;
    }

    const qtyNum = parseInt(quantity, 10);
    const minAllowedQty = editingItem ? 0 : 1;
    if (isNaN(qtyNum) || qtyNum < minAllowedQty) {
      setErrorMsg(editingItem ? 'Stock quantity cannot be negative (must be 0 or more)' : 'Stock quantity must be at least 1 item');
      return;
    }

    if (!pickupStartTime || !pickupEndTime) {
      setErrorMsg('Both pickup start time and end time are required');
      return;
    }

    setModalLoading(true);

    // Form data for file upload support
    const formData = new FormData();
    formData.append('name', trimmedName);
    formData.append('description', description.trim());
    formData.append('originalPrice', origPriceNum);
    formData.append('discountedPrice', discPriceNum);
    formData.append('quantity', qtyNum);
    formData.append('pickupStartTime', pickupStartTime);
    formData.append('pickupEndTime', pickupEndTime);
    formData.append('dietaryType', dietaryType);
    formData.append('allergens', JSON.stringify(allergens));
    formData.append('isSurpriseBag', isSurpriseBag);
    formData.append('estimatedValue', estimatedValue ? parseFloat(estimatedValue) : origPriceNum);
    if (imageFile) {
      formData.append('image', imageFile);
    }

    try {
      if (editingItem) {
        await api.put(`/restaurant/listings/${editingItem._id}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        await api.post('/restaurant/listings', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      setShowModal(false);
      fetchData(); // Refresh list and stats
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Action failed. Check fields and file size.');
    } finally {
      setModalLoading(false);
    }
  };

  const handleDeleteListing = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this listing permanently?')) return;
    
    setErrorMsg('');
    try {
      await api.delete(`/restaurant/listings/${itemId}`);
      fetchData();
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Deletion failed');
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      {/* Header */}
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '0.25rem' }}>Business Hub</h1>
          <p className="text-secondary">Track customer collections, list surplus items, and analyze impact.</p>
        </div>

        {analytics && analytics.isVerified ? (
          <button onClick={handleOpenAdd} className="btn btn-primary">
            <Plus size={18} /> Add Surplus Item
          </button>
        ) : (
          <span className="badge badge-warning" style={{ padding: '0.75rem 1.25rem' }}>
            Awaiting Admin Verification
          </span>
        )}
      </header>

      {/* Live Socket.io Notification Banner */}
      {liveNotification && (
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
            <span>{liveNotification}</span>
          </div>
          <button 
            className="btn btn-secondary btn-sm" 
            style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem' }}
            onClick={() => setLiveNotification(null)}
          >
            Dismiss
          </button>
        </div>
      )}

      {errorMsg && !showModal && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {/* Analytics Widgets */}
      {analytics && (
        <section className="analytics-grid">
          
          <div className="glass-panel analytics-widget">
            <div className="analytics-widget-icon" style={{ background: 'var(--color-primary-glow)' }}>
              <BadgeDollarSign className="text-emerald" size={24} />
            </div>
            <div className="analytics-widget-content">
              <p className="analytics-widget-label">Total Revenue</p>
              <h3 className="analytics-widget-value">${Math.max(0, analytics.totalRevenue || 0).toFixed(2)}</h3>
            </div>
          </div>

          <div className="glass-panel analytics-widget">
            <div className="analytics-widget-icon" style={{ background: 'rgba(16, 185, 129, 0.12)' }}>
              <ShoppingBag className="text-emerald" size={24} />
            </div>
            <div className="analytics-widget-content">
              <p className="analytics-widget-label">Available Stock</p>
              <h3 className="analytics-widget-value">
                {Math.max(0, analytics.totalStockAvailable ?? listings.filter(i => i.status === 'available').reduce((sum, item) => sum + Math.max(0, item.quantity), 0))} bags
              </h3>
            </div>
          </div>

          <div className="glass-panel analytics-widget">
            <div className="analytics-widget-icon" style={{ background: 'rgba(99, 102, 241, 0.1)' }}>
              <HeartHandshake className="text-indigo" size={24} />
            </div>
            <div className="analytics-widget-content">
              <p className="analytics-widget-label">Meals Rescued</p>
              <h3 className="analytics-widget-value">{Math.max(0, analytics.mealsSaved || 0)}</h3>
            </div>
          </div>

          <div className="glass-panel analytics-widget">
            <div className="analytics-widget-icon" style={{ background: 'rgba(245, 158, 11, 0.1)' }}>
              <Star className="text-amber" size={24} fill="currentColor" />
            </div>
            <div className="analytics-widget-content">
              <p className="analytics-widget-label">Rating Average</p>
              <h3 className="analytics-widget-value">{analytics.rating ? Number(analytics.rating).toFixed(1) : '5.0'} / 5</h3>
            </div>
          </div>

          <div className="glass-panel analytics-widget">
            <div className="analytics-widget-icon" style={{ background: 'rgba(255, 255, 255, 0.05)' }}>
              <BarChart3 className="text-secondary" size={24} />
            </div>
            <div className="analytics-widget-content">
              <p className="analytics-widget-label">Bookings Queue</p>
              <h3 className="analytics-widget-value">{Math.max(0, analytics.activeReservationsCount || 0)} active</h3>
            </div>
          </div>

        </section>
      )}

      {/* Verification warning block */}
      {analytics && !analytics.isVerified && (
        <div className="glass-panel" style={{ padding: '2rem', textAlign: 'center', marginBottom: '3rem', border: '1px solid rgba(245, 158, 11, 0.3)', background: 'rgba(245, 158, 11, 0.02)' }}>
          <Star size={32} className="text-amber" style={{ marginBottom: '1rem' }} />
          <h3>Profile verification is pending</h3>
          <p className="text-secondary" style={{ maxWidth: '600px', margin: '0.5rem auto 0 auto', fontSize: '0.95rem' }}>
            Our administrators are currently auditing your restaurant credentials. Once verified, you will receive full permissions to list items and collect customer reservations.
          </p>
        </div>
      )}

      {/* Inventory Listings */}
      <div>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Surplus Inventory</h2>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
            Retrieving inventory...
          </div>
        ) : listings.length === 0 ? (
          <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            <Utensils size={40} style={{ margin: '0 auto 1rem auto', opacity: 0.3 }} />
            <p>No surplus listings found. Get started by clicking "Add Surplus Item".</p>
          </div>
        ) : (
          <div className="grid-cols-3">
            {listings.map((item) => (
              <div key={item._id} className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                
                {/* Image / Icon */}
                {item.imagePath ? (
                  <img src={`http://localhost:5000${item.imagePath}`} alt={item.name} className="card-img" />
                ) : (
                  <div className="card-img-placeholder">
                    <Utensils size={32} />
                  </div>
                )}

                {/* Details */}
                <div style={{ flexGrow: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem', gap: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.15rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', minWidth: 0, flex: 1 }} title={item.name}>
                      {item.name}
                    </h3>
                    <span className={`badge ${item.status === 'available' && item.quantity > 0 ? 'badge-success' : 'badge-danger'}`} style={{ fontSize: '0.65rem', flexShrink: 0 }}>
                      {item.status === 'available' && item.quantity > 0 ? `${item.quantity} in stock` : 'Sold out'}
                    </span>
                  </div>

                  <p className="text-secondary" style={{ fontSize: '0.85rem', marginBottom: '1rem', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {item.description || 'No description provided.'}
                  </p>

                  <div style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
                    <p><strong>Original Price:</strong> ${Math.max(0, item.originalPrice || 0).toFixed(2)}</p>
                    <p><strong>Offer Price:</strong> <span className="text-emerald" style={{ fontWeight: 600 }}>${Math.max(0, item.discountedPrice || 0).toFixed(2)}</span></p>
                    <p>
                      <strong>In Stock:</strong>{' '}
                      <span className={item.quantity > 0 ? 'text-emerald' : 'text-rose'} style={{ fontWeight: 600 }}>
                        {Math.max(0, item.quantity)} {item.quantity === 1 ? 'bag' : 'bags'} {item.quantity <= 0 ? '(Sold Out)' : ''}
                      </span>
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.4rem', marginTop: '0.2rem' }}>
                      <p style={{ margin: 0, fontSize: '0.78rem' }}><strong>Pickup:</strong> {item.pickupStartTime} - {item.pickupEndTime}</p>
                      <ExpiryTimer expiryDate={item.expiryDate} pickupEndTime={item.pickupEndTime} />
                    </div>
                    <div style={{ display: 'flex', gap: '0.3rem', flexWrap: 'wrap', marginTop: '0.4rem' }}>
                      {item.isSurpriseBag && (
                        <span className="badge" style={{ fontSize: '0.65rem', background: 'linear-gradient(135deg, #ec4899, #8b5cf6)', color: '#fff', fontWeight: 700 }}>
                          🎁 MYSTERY BAG
                        </span>
                      )}
                      <span className={`badge ${item.dietaryType === 'veg' ? 'badge-success' : item.dietaryType === 'vegan' ? 'badge-info' : 'badge-warning'}`} style={{ fontSize: '0.65rem' }}>
                        {item.dietaryType === 'veg' ? '🟢 Veg' : item.dietaryType === 'vegan' ? '🌱 Vegan' : '🔴 Non-Veg'}
                      </span>
                      {item.allergens && item.allergens.map((tag) => (
                        <span key={tag} className="badge badge-secondary" style={{ fontSize: '0.6rem', background: 'rgba(255,255,255,0.06)' }}>
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div style={{ display: 'flex', gap: '0.5rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem', marginTop: 'auto' }}>
                  <button 
                    onClick={() => handleOpenEdit(item)}
                    className="btn btn-secondary btn-sm"
                    style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.3rem' }}
                  >
                    <Edit2 size={12} /> Edit
                  </button>
                  <button 
                    onClick={() => handleDeleteListing(item._id)}
                    className="btn btn-danger btn-sm"
                    style={{ flex: '0 0 40px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                  >
                    <Trash2 size={14} />
                  </button>
                </div>

              </div>
            ))}
          </div>
        )}
      </div>

      {/* Creation/Editing Modal Overlay */}
      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '560px', width: '100%', maxHeight: '90vh', overflowY: 'auto', overflowX: 'hidden', boxSizing: 'border-box' }}>
            <button className="modal-close" onClick={() => setShowModal(false)}>×</button>
            
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', fontFamily: 'var(--font-display)' }}>
              {editingItem ? 'Edit Surplus Offer' : 'Create Surplus Offer'}
            </h3>

            {errorMsg && (
              <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1.25rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                {errorMsg}
              </div>
            )}

            <form onSubmit={handleModalSubmit}>
              {/* Surprise Bag / Mystery Box Toggle */}
              <div 
                style={{ 
                  background: 'rgba(236, 72, 153, 0.08)', 
                  border: '1px border-radius var(--border-radius-sm)', 
                  borderLeft: '4px solid #ec4899', 
                  padding: '0.85rem 1rem', 
                  marginBottom: '1.25rem',
                  borderRadius: '8px'
                }}
              >
                <label style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', cursor: 'pointer', fontWeight: 600, fontSize: '0.9rem', color: '#f472b6' }}>
                  <input 
                    type="checkbox" 
                    checked={isSurpriseBag} 
                    onChange={handleSurpriseBagToggle}
                    style={{ width: '16px', height: '16px', accentColor: '#ec4899' }}
                  />
                  🎁 Mark as Surprise Bag / Mystery Box (Too Good To Go Style)
                </label>
                <p className="text-secondary" style={{ fontSize: '0.78rem', margin: '0.25rem 0 0 1.6rem' }}>
                  Select if exact contents are unknown ahead of time. Customers get a surprise mix worth an estimated retail value!
                </p>
              </div>

              <div className="form-group">
                <label className="form-label">{isSurpriseBag ? 'Surprise Bag Title' : 'Food Title / Name'}</label>
                <input 
                  type="text" 
                  required 
                  placeholder={isSurpriseBag ? "e.g. Evening Bakery Surprise Bag 🎁" : "e.g. Sourdough Loaf Mix, Croissant Box"} 
                  className="form-control"
                  value={name} 
                  onChange={(e) => setName(e.target.value)} 
                />
              </div>

              <div className="form-group">
                <label className="form-label">Description / Contents</label>
                <textarea 
                  placeholder="e.g. A mixed pack of 4 vanilla muffins and 2 cookies baked this morning." 
                  className="form-control"
                  rows="2"
                  style={{ fontFamily: 'var(--font-body)', resize: 'none' }}
                  value={description} 
                  onChange={(e) => setDescription(e.target.value)} 
                />
              </div>

              {/* Dietary Category */}
              <div className="form-group">
                <label className="form-label">Dietary Preference</label>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', fontSize: '0.85rem' }}>
                    <input type="radio" name="dietaryType" value="veg" checked={dietaryType === 'veg'} onChange={(e) => setDietaryType(e.target.value)} />
                    🟢 Vegetarian
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', fontSize: '0.85rem' }}>
                    <input type="radio" name="dietaryType" value="non-veg" checked={dietaryType === 'non-veg'} onChange={(e) => setDietaryType(e.target.value)} />
                    🔴 Non-Veg
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', cursor: 'pointer', fontSize: '0.85rem' }}>
                    <input type="radio" name="dietaryType" value="vegan" checked={dietaryType === 'vegan'} onChange={(e) => setDietaryType(e.target.value)} />
                    🌱 Vegan
                  </label>
                </div>
              </div>

              {/* Allergen & Dietary Tags */}
              <div className="form-group">
                <label className="form-label">Allergen & Dietary Tags</label>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {availableAllergens.map((tag) => {
                    const isSelected = allergens.includes(tag);
                    return (
                      <button
                        type="button"
                        key={tag}
                        onClick={() => handleAllergenToggle(tag)}
                        className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
                        style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
                      >
                        {isSelected ? '✓ ' : '+ '} {tag}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div 
                className="form-price-qty-row" 
                style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', 
                  gap: '0.75rem', 
                  width: '100%',
                  boxSizing: 'border-box' 
                }}
              >
                <div className="form-group" style={{ minWidth: 0, width: '100%' }}>
                  <label className="form-label">Original ($)</label>
                  <input 
                    type="number" 
                    required 
                    min="0.01"
                    step="0.01" 
                    placeholder="12.50" 
                    className="form-control"
                    style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
                    value={originalPrice} 
                    onKeyDown={(e) => { if (e.key === '-' || e.key === 'Subtract' || e.key === 'e' || e.key === 'E') e.preventDefault(); }}
                    onPaste={(e) => {
                      const text = e.clipboardData.getData('text');
                      if (text.includes('-')) {
                        e.preventDefault();
                        setOriginalPrice(text.replace(/-/g, ''));
                      }
                    }}
                    onChange={(e) => {
                      const v = e.target.value.replace(/-/g, '');
                      setOriginalPrice(v);
                    }} 
                  />
                </div>
                <div className="form-group" style={{ minWidth: 0, width: '100%' }}>
                  <label className="form-label">Discount ($)</label>
                  <input 
                    type="number" 
                    required 
                    min="0"
                    step="0.01" 
                    placeholder="4.00" 
                    className="form-control"
                    style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
                    value={discountedPrice} 
                    onKeyDown={(e) => { if (e.key === '-' || e.key === 'Subtract' || e.key === 'e' || e.key === 'E') e.preventDefault(); }}
                    onPaste={(e) => {
                      const text = e.clipboardData.getData('text');
                      if (text.includes('-')) {
                        e.preventDefault();
                        setDiscountedPrice(text.replace(/-/g, ''));
                      }
                    }}
                    onChange={(e) => {
                      const v = e.target.value.replace(/-/g, '');
                      setDiscountedPrice(v);
                    }} 
                  />
                </div>
                <div className="form-group" style={{ minWidth: 0, width: '100%' }}>
                  <label className="form-label">Stock Qty</label>
                  <input 
                    type="number" 
                    required 
                    min={editingItem ? '0' : '1'}
                    step="1"
                    placeholder="5" 
                    className="form-control"
                    style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
                    value={quantity} 
                    onKeyDown={(e) => { if (e.key === '-' || e.key === 'Subtract' || e.key === '.' || e.key === 'e' || e.key === 'E') e.preventDefault(); }}
                    onPaste={(e) => {
                      const text = e.clipboardData.getData('text');
                      if (text.includes('-') || text.includes('.')) {
                        e.preventDefault();
                        setQuantity(text.replace(/[^0-9]/g, ''));
                      }
                    }}
                    onChange={(e) => {
                      const v = e.target.value.replace(/[^0-9]/g, '');
                      setQuantity(v);
                    }} 
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: '0.75rem', width: '100%', boxSizing: 'border-box' }}>
                <div className="form-group" style={{ minWidth: 0, width: '100%' }}>
                  <label className="form-label">Pickup Start Time</label>
                  <input 
                    type="time" 
                    required 
                    className="form-control"
                    style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
                    value={pickupStartTime} 
                    onChange={(e) => setPickupStartTime(e.target.value)} 
                  />
                </div>
                <div className="form-group" style={{ minWidth: 0, width: '100%' }}>
                  <label className="form-label">Pickup End Time</label>
                  <input 
                    type="time" 
                    required 
                    className="form-control"
                    style={{ width: '100%', minWidth: 0, boxSizing: 'border-box' }}
                    value={pickupEndTime} 
                    onChange={(e) => setPickupEndTime(e.target.value)} 
                  />
                </div>
              </div>

              <div className="form-group" style={{ marginTop: '0.5rem' }}>
                <label className="form-label">Upload Food Photo (Optional)</label>
                <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px dashed var(--glass-border)', padding: '0.75rem 1.25rem', borderRadius: 'var(--border-radius-sm)', cursor: 'pointer', fontSize: '0.85rem', width: '100%' }}>
                    <Image size={16} className="text-emerald" />
                    <span>{imageFile ? imageFile.name : 'Select file (JPEG, PNG, WebP)...'}</span>
                    <input 
                      type="file" 
                      accept="image/*"
                      style={{ display: 'none' }}
                      onChange={handleFileChange}
                    />
                  </label>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '2rem', borderTop: '1px solid var(--glass-border)', paddingTop: '1rem' }}>
                <button type="button" className="btn btn-secondary btn-sm" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary btn-sm" disabled={modalLoading}>
                  {modalLoading ? 'Saving...' : editingItem ? 'Save Updates' : 'Publish Offer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`
        @media (max-width: 520px) {
          .form-price-qty-row {
            grid-template-columns: 1fr !important;
            gap: 0.75rem !important;
          }
        }
      `}</style>
    </div>
  );
};

export default RestaurantDashboard;
