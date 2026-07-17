import { useState, useEffect } from 'react';
import api from '../../services/api';
import { Plus, BarChart3, Star, BadgeDollarSign, HeartHandshake, Utensils, Image, Trash2, Edit2, Check, X } from 'lucide-react';

const RestaurantDashboard = () => {
  const [listings, setListings] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');

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
  const [imageFile, setImageFile] = useState(null);

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
  }, []);

  const handleOpenAdd = () => {
    setEditingItem(null);
    setName('');
    setDescription('');
    setOriginalPrice('');
    setDiscountedPrice('');
    setQuantity('');
    setPickupStartTime('18:00');
    setPickupEndTime('21:00');
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
    setImageFile(null);
    setErrorMsg('');
    setShowModal(true);
  };

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  const handleModalSubmit = async (e) => {
    e.preventDefault();
    setModalLoading(true);
    setErrorMsg('');

    // Form data for file upload support
    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', description);
    formData.append('originalPrice', originalPrice);
    formData.append('discountedPrice', discountedPrice);
    formData.append('quantity', quantity);
    formData.append('pickupStartTime', pickupStartTime);
    formData.append('pickupEndTime', pickupEndTime);
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

      {errorMsg && !showModal && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {/* Analytics Widgets */}
      {analytics && (
        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem', marginBottom: '3rem' }} className="analytics-grid">
          
          <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div style={{ padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: 'var(--color-primary-glow)' }}>
              <BadgeDollarSign className="text-emerald" size={24} />
            </div>
            <div>
              <p className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>Total Revenue</p>
              <h3 style={{ fontSize: '1.5rem' }}>${analytics.totalRevenue.toFixed(2)}</h3>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div style={{ padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(99, 102, 241, 0.1)' }}>
              <HeartHandshake className="text-indigo" size={24} />
            </div>
            <div>
              <p className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>Meals Rescued</p>
              <h3 style={{ fontSize: '1.5rem' }}>{analytics.mealsSaved}</h3>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div style={{ padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(245, 158, 11, 0.1)' }}>
              <Star className="text-amber" size={24} fill="currentColor" />
            </div>
            <div>
              <p className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>Rating Average</p>
              <h3 style={{ fontSize: '1.5rem' }}>{analytics.rating} / 5</h3>
            </div>
          </div>

          <div className="glass-panel" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <div style={{ padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: 'rgba(255, 255, 255, 0.05)' }}>
              <BarChart3 className="text-secondary" size={24} />
            </div>
            <div>
              <p className="text-muted" style={{ fontSize: '0.8rem', fontWeight: 600 }}>Bookings Queue</p>
              <h3 style={{ fontSize: '1.5rem' }}>{analytics.activeReservationsCount} active</h3>
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
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.15rem' }}>{item.name}</h3>
                    <span className={`badge ${item.status === 'available' ? 'badge-success' : 'badge-danger'}`} style={{ fontSize: '0.65rem' }}>
                      {item.status}
                    </span>
                  </div>

                  <p className="text-secondary" style={{ fontSize: '0.85rem', marginBottom: '1rem', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {item.description || 'No description provided.'}
                  </p>

                  <div style={{ borderTop: '1px solid var(--glass-border)', paddingTop: '0.75rem', display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1.25rem' }}>
                    <p><strong>Original Price:</strong> ${item.originalPrice.toFixed(2)}</p>
                    <p><strong>Offer Price:</strong> <span className="text-emerald" style={{ fontWeight: 600 }}>${item.discountedPrice.toFixed(2)}</span></p>
                    <p><strong>In Stock:</strong> {item.quantity} bags</p>
                    <p><strong>Pickup window:</strong> {item.pickupStartTime} - {item.pickupEndTime}</p>
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
          <div className="modal-content" style={{ maxWidth: '550px' }}>
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
              <div className="form-group">
                <label className="form-label">Food Title / Name</label>
                <input 
                  type="text" 
                  required 
                  placeholder="e.g. Sourdough Loaf Mix, Croissant Box" 
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

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }} className="form-price-qty-row">
                <div className="form-group">
                  <label className="form-label">Original ($)</label>
                  <input 
                    type="number" 
                    required 
                    step="0.01" 
                    placeholder="12.50" 
                    className="form-control"
                    value={originalPrice} 
                    onChange={(e) => setOriginalPrice(e.target.value)} 
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Discount ($)</label>
                  <input 
                    type="number" 
                    required 
                    step="0.01" 
                    placeholder="4.00" 
                    className="form-control"
                    value={discountedPrice} 
                    onChange={(e) => setDiscountedPrice(e.target.value)} 
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Stock Qty</label>
                  <input 
                    type="number" 
                    required 
                    placeholder="5" 
                    className="form-control"
                    value={quantity} 
                    onChange={(e) => setQuantity(e.target.value)} 
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div className="form-group">
                  <label className="form-label">Pickup Start Time</label>
                  <input 
                    type="time" 
                    required 
                    className="form-control"
                    value={pickupStartTime} 
                    onChange={(e) => setPickupStartTime(e.target.value)} 
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Pickup End Time</label>
                  <input 
                    type="time" 
                    required 
                    className="form-control"
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
        @media (max-width: 768px) {
          .analytics-grid {
            grid-template-columns: 1fr 1fr !important;
          }
          .form-price-qty-row {
            grid-template-columns: 1fr !important;
            gap: 0 !important;
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

export default RestaurantDashboard;
