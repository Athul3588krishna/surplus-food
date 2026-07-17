import { useState, useEffect } from 'react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { User, Phone, KeyRound, Mail, CheckCircle } from 'lucide-react';

const CustomerProfile = () => {
  const { user, updateProfile } = useAuth();
  
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setEmail(user.email || '');
      setPhoneNumber(user.phoneNumber || '');
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    if (password && password !== confirmPassword) {
      setErrorMsg('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const payload = { name, phoneNumber };
      if (password) payload.password = password;

      const { data } = await api.put('/auth/profile', payload);
      
      // Update global context state
      updateProfile(data);
      
      setSuccessMsg('Profile updated successfully!');
      setPassword('');
      setConfirmPassword('');
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to update profile settings');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem', maxWidth: '600px' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem' }}>Account Settings</h1>
        <p className="text-secondary">Manage your personal information, contact number, and security credentials.</p>
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
          
          <div className="form-group">
            <label className="form-label">Email Address (Read-only)</label>
            <div style={{ position: 'relative' }}>
              <Mail size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input 
                type="email" 
                className="form-control" 
                style={{ paddingLeft: '2.5rem', width: '100%', opacity: 0.6 }}
                value={email}
                readOnly
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Display Name</label>
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
            <label className="form-label">Phone Contact</label>
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

          <div style={{ borderTop: '1px solid var(--glass-border)', marginTop: '2rem', paddingTop: '1.5rem' }}>
            <h3 style={{ fontSize: '1.2rem', marginBottom: '1rem' }} className="text-secondary">Change Password</h3>
            
            <div className="form-group">
              <label className="form-label">New Password (Leave blank to keep current)</label>
              <div style={{ position: 'relative' }}>
                <KeyRound size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <input 
                  type="password" 
                  placeholder="••••••••" 
                  className="form-control" 
                  style={{ paddingLeft: '2.5rem', width: '100%' }}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Confirm New Password</label>
              <div style={{ position: 'relative' }}>
                <KeyRound size={16} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                <input 
                  type="password" 
                  placeholder="••••••••" 
                  className="form-control" 
                  style={{ paddingLeft: '2.5rem', width: '100%' }}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-block" 
            style={{ marginTop: '2rem' }}
            disabled={loading}
          >
            {loading ? 'Updating settings...' : 'Save Profile Changes'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CustomerProfile;
