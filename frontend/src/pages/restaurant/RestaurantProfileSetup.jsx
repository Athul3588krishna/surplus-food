import { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Store, MapPin, UtensilsCrossed, FileText, User, Phone, CheckCircle, Image } from 'lucide-react';

const RestaurantProfileSetup = () => {
  const { user, updateProfile } = useAuth();

  // User fields
  const [name, setName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  // Restaurant fields
  const [restaurantName, setRestaurantName] = useState('');
  const [address, setAddress] = useState('');
  const [cuisineType, setCuisineType] = useState('');
  const [description, setDescription] = useState('');
  const [imagePath, setImagePath] = useState('');
  
  // Image Upload state
  const [imageFile, setImageFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setPhoneNumber(user.phoneNumber || '');
      
      if (user.restaurantProfile) {
        setRestaurantName(user.restaurantProfile.restaurantName || '');
        setAddress(user.restaurantProfile.address || '');
        setCuisineType(user.restaurantProfile.cuisineType || '');
        setDescription(user.restaurantProfile.description || '');
        setImagePath(user.restaurantProfile.imagePath || '');
      }
    }
  }, [user]);

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    const formData = new FormData();
    formData.append('name', name);
    formData.append('phoneNumber', phoneNumber);
    formData.append('restaurantName', restaurantName);
    formData.append('address', address);
    formData.append('cuisineType', cuisineType);
    formData.append('description', description);
    
    if (imageFile) {
      formData.append('image', imageFile);
    }

    try {
      const { data } = await api.put('/auth/profile', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Update local storage and context
      updateProfile(data);

      setSuccessMsg('Business profile settings saved successfully!');
      setImageFile(null); // Clear selected file state
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to save business settings');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem', maxWidth: '800px' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>Business Settings</h1>
        <p className="text-secondary">Update your store address, description, cuisine type, and restaurant display photos.</p>
      </header>

      <div className="glass-panel" style={{ padding: '2rem' }}>
        {errorMsg && (
          <div className="badge badge-danger" style={{ width: '100%', padding: '0.75rem', marginBottom: '1.5rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
            {errorMsg}
          </div>
        )}

        {successMsg && (
          <div className="badge badge-success" style={{ width: '100%', padding: '0.75rem', marginBottom: '1.5rem', textTransform: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}>
            <CheckCircle size={16} /> {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }} className="profile-grid">
            
            {/* Left Side: Owner details & Logo */}
            <div>
              <h3 style={{ fontSize: '1.15rem', marginBottom: '1.25rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }} className="text-emerald">Owner Account</h3>
              
              <div className="form-group">
                <label className="form-label">Contact Name</label>
                <div style={{ position: 'relative' }}>
                  <User size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                  <input 
                    type="text" 
                    required 
                    className="form-control" 
                    style={{ paddingLeft: '2.5rem', width: '100%' }}
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Contact Phone</label>
                <div style={{ position: 'relative' }}>
                  <Phone size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                  <input 
                    type="tel" 
                    required 
                    className="form-control" 
                    style={{ paddingLeft: '2.5rem', width: '100%' }}
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                  />
                </div>
              </div>

              {/* Logo preview */}
              <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
                <label className="form-label" style={{ textAlign: 'left', display: 'block' }}>Store Profile Banner</label>
                {imagePath ? (
                  <img 
                    src={`http://localhost:5000${imagePath}`} 
                    alt="Store Logo" 
                    style={{ width: '100%', height: '150px', objectFit: 'cover', borderRadius: 'var(--border-radius-sm)', border: '1px solid var(--glass-border)', marginBottom: '1rem' }}
                  />
                ) : (
                  <div className="card-img-placeholder" style={{ height: '150px', margin: '0 auto 1rem auto' }}>
                    <Store size={36} />
                  </div>
                )}
                
                <label style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.03)', border: '1px dashed var(--glass-border)', padding: '0.6rem', borderRadius: 'var(--border-radius-sm)', cursor: 'pointer', fontSize: '0.8rem' }}>
                  <Image size={14} className="text-emerald" />
                  <span>{imageFile ? imageFile.name : 'Change Profile Photo'}</span>
                  <input 
                    type="file" 
                    accept="image/*"
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                  />
                </label>
              </div>
            </div>

            {/* Right Side: Restaurant Store details */}
            <div style={{ borderLeft: '1px solid var(--glass-border)', paddingLeft: '2rem' }} className="biz-details-pane">
              <h3 style={{ fontSize: '1.15rem', marginBottom: '1.25rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }} className="text-emerald">Store Information</h3>

              <div className="form-group">
                <label className="form-label">Restaurant / Brand Name</label>
                <div style={{ position: 'relative' }}>
                  <Store size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                  <input 
                    type="text" 
                    required 
                    className="form-control" 
                    style={{ paddingLeft: '2.5rem', width: '100%' }}
                    value={restaurantName}
                    onChange={(e) => setRestaurantName(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Store Street Address</label>
                <div style={{ position: 'relative' }}>
                  <MapPin size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                  <input 
                    type="text" 
                    required 
                    className="form-control" 
                    style={{ paddingLeft: '2.5rem', width: '100%' }}
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Cuisine Category</label>
                <div style={{ position: 'relative' }}>
                  <UtensilsCrossed size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                  <input 
                    type="text" 
                    required 
                    className="form-control" 
                    style={{ paddingLeft: '2.5rem', width: '100%' }}
                    value={cuisineType}
                    onChange={(e) => setCuisineType(e.target.value)}
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Description / Bio</label>
                <div style={{ position: 'relative' }}>
                  <FileText size={16} style={{ position: 'absolute', left: '1rem', top: '12px', color: 'var(--text-muted)' }} />
                  <textarea 
                    className="form-control" 
                    rows="4"
                    style={{ paddingLeft: '2.5rem', width: '100%', fontFamily: 'var(--font-body)', resize: 'none' }}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  />
                </div>
              </div>
            </div>

          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block" 
            style={{ marginTop: '2.5rem' }}
            disabled={loading}
          >
            {loading ? 'Saving settings...' : 'Save Settings'}
          </button>
        </form>
      </div>

      <style>{`
        @media (max-width: 768px) {
          .profile-grid {
            grid-template-columns: 1fr !important;
          }
          .biz-details-pane {
            border-left: none !important;
            padding-left: 0 !important;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--glass-border);
          }
        }
      `}</style>
    </div>
  );
};

export default RestaurantProfileSetup;
