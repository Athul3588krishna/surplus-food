import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { KeyRound, Mail, User as UserIcon, Phone, Store, MapPin, UtensilsCrossed, FileText, CheckCircle } from 'lucide-react';

const AuthPage = () => {
  const { login, register, verifyRegisterOTP, user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  // Tab states
  const [isLogin, setIsLogin] = useState(true);
  
  // Form fields
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [role, setRole] = useState('customer'); // customer or restaurant
  const [phoneNumber, setPhoneNumber] = useState('');
  
  // Restaurant specific fields
  const [restaurantName, setRestaurantName] = useState('');
  const [address, setAddress] = useState('');
  const [cuisineType, setCuisineType] = useState('');
  const [description, setDescription] = useState('');

  // OTP Verification state
  const [needsOtpVerify, setNeedsOtpVerify] = useState(false);
  const [otpEmail, setOtpEmail] = useState('');
  const [enteredOtp, setEnteredOtp] = useState('');

  // Status feedback
  const [errorMsg, setErrorMsg] = useState('');
  const [loadingMsg, setLoadingMsg] = useState(false);

  // Sync with search params (?tab=register or ?tab=login)
  useEffect(() => {
    const tab = searchParams.get('tab');
    if (tab === 'register') {
      setIsLogin(false);
    } else {
      setIsLogin(true);
    }
    setNeedsOtpVerify(false);
  }, [searchParams]);

  // If already logged in, redirect
  useEffect(() => {
    if (user) {
      if (user.role === 'customer') navigate('/customer/dashboard');
      else if (user.role === 'restaurant') navigate('/restaurant/dashboard');
      else if (user.role === 'admin') navigate('/admin/dashboard');
    }
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoadingMsg(true);

    if (isLogin) {
      const res = await login(email, password);
      setLoadingMsg(false);
      if (!res.success) {
        if (res.needsVerification) {
          setOtpEmail(res.email);
          setNeedsOtpVerify(true);
        } else {
          setErrorMsg(res.message);
        }
      }
    } else {
      // Build registration payload
      const payload = {
        name,
        email,
        password,
        role,
        phoneNumber
      };

      if (role === 'restaurant') {
        if (!restaurantName || !address || !cuisineType) {
          setErrorMsg('Please fill in all restaurant business details.');
          setLoadingMsg(false);
          return;
        }
        payload.restaurantName = restaurantName;
        payload.address = address;
        payload.cuisineType = cuisineType;
        payload.description = description;
      }

      const res = await register(payload);
      setLoadingMsg(false);
      if (res.success) {
        setOtpEmail(res.email);
        setNeedsOtpVerify(true);
      } else {
        setErrorMsg(res.message);
      }
    }
  };

  const handleOtpSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoadingMsg(true);

    const res = await verifyRegisterOTP(otpEmail, enteredOtp);
    setLoadingMsg(false);
    
    if (!res.success) {
      setErrorMsg(res.message);
    }
  };

  return (
    <div className="auth-container animate-fade-in" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 'calc(100vh - 70px)', padding: '2rem 1.5rem' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: needsOtpVerify ? '450px' : (role === 'restaurant' && !isLogin ? '650px' : '450px'), padding: '2.5rem', transition: 'max-width 0.3s ease' }}>
        
        {needsOtpVerify ? (
          /* OTP VERIFICATION VIEW */
          <div>
            <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
              <div style={{ width: '50px', height: '50px', borderRadius: '50%', background: 'var(--color-primary-glow)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem auto' }}>
                <Mail className="text-emerald" size={24} />
              </div>
              <h3 style={{ fontSize: '1.5rem', fontFamily: 'var(--font-display)', marginBottom: '0.5rem' }}>Verify Your Email</h3>
              <p className="text-secondary" style={{ fontSize: '0.9rem' }}>
                We sent a 6-digit OTP verification code to:<br />
                <strong className="text-indigo">{otpEmail}</strong>
              </p>
            </div>

            {errorMsg && (
              <div className="badge badge-danger" style={{ width: '100%', borderRadius: 'var(--border-radius-sm)', padding: '0.75rem', marginBottom: '1.5rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                {errorMsg}
              </div>
            )}

            <form onSubmit={handleOtpSubmit}>
              <div className="form-group">
                <label className="form-label" style={{ textAlign: 'center', display: 'block' }}>Enter 6-Digit Code</label>
                <input 
                  type="text" 
                  maxLength="6"
                  required 
                  placeholder="000000" 
                  className="form-control" 
                  style={{ textAlign: 'center', fontSize: '1.8rem', letterSpacing: '8px', fontWeight: 'bold', width: '100%', padding: '0.5rem 0' }}
                  value={enteredOtp} 
                  onChange={(e) => setEnteredOtp(e.target.value.replace(/\D/g, ''))} // digit only
                />
              </div>

              <button 
                type="submit" 
                className="btn btn-primary btn-block" 
                style={{ marginTop: '1.5rem' }}
                disabled={loadingMsg}
              >
                {loadingMsg ? 'Verifying Code...' : 'Verify & Sign In'}
              </button>

              <button 
                type="button" 
                className="btn btn-secondary btn-block btn-sm" 
                style={{ marginTop: '0.75rem', border: 'none', background: 'transparent' }}
                onClick={() => setNeedsOtpVerify(false)}
              >
                Back to Login
              </button>
            </form>
          </div>
        ) : (
          /* STANDARD LOGIN / SIGNUP VIEW */
          <>
            {/* Tab Headers */}
            <div style={{ display: 'flex', borderBottom: '1px solid var(--glass-border)', marginBottom: '2rem' }}>
              <button 
                type="button"
                className="tab-btn"
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  borderBottom: isLogin ? '2px solid var(--color-primary)' : '2px solid transparent',
                  padding: '1rem',
                  color: isLogin ? 'var(--text-primary)' : 'var(--text-muted)',
                  fontWeight: 600,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-display)',
                  fontSize: '1.05rem'
                }}
                onClick={() => { setIsLogin(true); setErrorMsg(''); }}
              >
                Sign In
              </button>
              <button 
                type="button"
                className="tab-btn"
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  borderBottom: !isLogin ? '2px solid var(--color-primary)' : '2px solid transparent',
                  padding: '1rem',
                  color: !isLogin ? 'var(--text-primary)' : 'var(--text-muted)',
                  fontWeight: 600,
                  cursor: 'pointer',
                  fontFamily: 'var(--font-display)',
                  fontSize: '1.05rem'
                }}
                onClick={() => { setIsLogin(false); setErrorMsg(''); }}
              >
                Create Account
              </button>
            </div>

            {errorMsg && (
              <div className="badge badge-danger" style={{ width: '100%', borderRadius: 'var(--border-radius-sm)', padding: '0.75rem', marginBottom: '1.5rem', textTransform: 'none', display: 'block', textAlign: 'center' }}>
                {errorMsg}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              {/* Main User Fields */}
              <div style={{ display: 'grid', gridTemplateColumns: role === 'restaurant' && !isLogin ? '1fr 1fr' : '1fr', gap: '1.5rem' }}>
                
                {/* Left Column / Main Fields */}
                <div>
                  {!isLogin && (
                    <>
                      <div className="form-group">
                        <label className="form-label">Full Name</label>
                        <div style={{ position: 'relative' }}>
                          <UserIcon size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                          <input 
                            type="text" 
                            required 
                            placeholder="John Doe" 
                            className="form-control" 
                            style={{ paddingLeft: '2.5rem', width: '100%' }}
                            value={name} 
                            onChange={(e) => setName(e.target.value)} 
                          />
                        </div>
                      </div>

                      <div className="form-group">
                        <label className="form-label">Account Type</label>
                        <div style={{ display: 'flex', gap: '1rem' }}>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', flex: 1, padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: role === 'customer' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(255,255,255,0.02)', border: role === 'customer' ? '1px solid var(--color-primary)' : '1px solid var(--glass-border)', transition: 'all 0.2s' }}>
                            <input type="radio" name="role" value="customer" checked={role === 'customer'} onChange={() => setRole('customer')} style={{ accentColor: 'var(--color-primary)' }} />
                            <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>Customer</span>
                          </label>
                          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', flex: 1, padding: '0.75rem', borderRadius: 'var(--border-radius-sm)', background: role === 'restaurant' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(255,255,255,0.02)', border: role === 'restaurant' ? '1px solid var(--color-primary)' : '1px solid var(--glass-border)', transition: 'all 0.2s' }}>
                            <input type="radio" name="role" value="restaurant" checked={role === 'restaurant'} onChange={() => setRole('restaurant')} style={{ accentColor: 'var(--color-primary)' }} />
                            <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>Restaurant</span>
                          </label>
                        </div>
                      </div>

                      <div className="form-group">
                        <label className="form-label">Phone Number</label>
                        <div style={{ position: 'relative' }}>
                          <Phone size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                          <input 
                            type="tel" 
                            required 
                            placeholder="555-123-4567" 
                            className="form-control" 
                            style={{ paddingLeft: '2.5rem', width: '100%' }}
                            value={phoneNumber} 
                            onChange={(e) => setPhoneNumber(e.target.value)} 
                          />
                        </div>
                      </div>
                    </>
                  )}

                  <div className="form-group">
                    <label className="form-label">Email Address</label>
                    <div style={{ position: 'relative' }}>
                      <Mail size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                      <input 
                        type="email" 
                        required 
                        placeholder="you@example.com" 
                        className="form-control" 
                        style={{ paddingLeft: '2.5rem', width: '100%' }}
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                      />
                    </div>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Password</label>
                    <div style={{ position: 'relative' }}>
                      <KeyRound size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                      <input 
                        type="password" 
                        required 
                        placeholder="••••••••" 
                        className="form-control" 
                        style={{ paddingLeft: '2.5rem', width: '100%' }}
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                      />
                    </div>
                  </div>
                </div>

                {/* Right Column / Restaurant Details */}
                {!isLogin && role === 'restaurant' && (
                  <div style={{ borderLeft: '1px solid var(--glass-border)', paddingLeft: '1.5rem' }} className="restaurant-details-pane">
                    <h4 style={{ fontSize: '1.1rem', marginBottom: '1rem', borderBottom: '1px solid var(--glass-border)', paddingBottom: '0.5rem' }} className="text-emerald">Restaurant Information</h4>
                    
                    <div className="form-group">
                      <label className="form-label">Business / Restaurant Name</label>
                      <div style={{ position: 'relative' }}>
                        <Store size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                        <input 
                          type="text" 
                          required={role === 'restaurant'}
                          placeholder="The Green Bakery" 
                          className="form-control" 
                          style={{ paddingLeft: '2.5rem', width: '100%' }}
                          value={restaurantName} 
                          onChange={(e) => setRestaurantName(e.target.value)} 
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label className="form-label">Street Address</label>
                      <div style={{ position: 'relative' }}>
                        <MapPin size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                        <input 
                          type="text" 
                          required={role === 'restaurant'}
                          placeholder="123 Bread St, Foodtown" 
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
                          required={role === 'restaurant'}
                          placeholder="Bakeries, Cafe, Italian, etc." 
                          className="form-control" 
                          style={{ paddingLeft: '2.5rem', width: '100%' }}
                          value={cuisineType} 
                          onChange={(e) => setCuisineType(e.target.value)} 
                        />
                      </div>
                    </div>

                    <div className="form-group">
                      <label className="form-label">Short Description</label>
                      <div style={{ position: 'relative' }}>
                        <FileText size={16} style={{ position: 'absolute', left: '1rem', top: '12px', color: 'var(--text-muted)' }} />
                        <textarea 
                          placeholder="Tell customers about your fresh bakes..." 
                          className="form-control" 
                          rows="2"
                          style={{ paddingLeft: '2.5rem', width: '100%', fontFamily: 'var(--font-body)', resize: 'none' }}
                          value={description} 
                          onChange={(e) => setDescription(e.target.value)} 
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <button 
                type="submit" 
                className="btn btn-primary btn-block" 
                style={{ marginTop: '2rem' }}
                disabled={loadingMsg}
              >
                {loadingMsg ? 'Authenticating...' : isLogin ? 'Sign In' : 'Register Account'}
              </button>
            </form>
          </>
        )}
      </div>

      <style>{`
        @media (max-width: 768px) {
          .auth-container .glass-panel {
            max-width: 100% !important;
          }
          .auth-container form > div {
            grid-template-columns: 1fr !important;
          }
          .restaurant-details-pane {
            border-left: none !important;
            padding-left: 0 !important;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--glass-border);
          }
        }
      `}</style>
    </div>
  );
};

export default AuthPage;
