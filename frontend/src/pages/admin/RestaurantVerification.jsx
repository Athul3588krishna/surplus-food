import { useState, useEffect } from 'react';
import api from '../../services/api';
import { ShieldCheck, Mail, Phone, MapPin, Store, Check, X, ShieldX } from 'lucide-react';

const RestaurantVerification = () => {
  const [pendingList, setPendingList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [actionSuccess, setActionSuccess] = useState('');

  const fetchPending = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const { data } = await api.get('/admin/pending-restaurants');
      setPendingList(data);
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Failed to retrieve pending profiles');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPending();
  }, []);

  const handleVerifyAction = async (profileId, action) => {
    const confirmMsg = action === 'approve' 
      ? 'Approve and verify this restaurant profile?' 
      : 'Reject this restaurant profile? (This will delete the account from database)';

    if (!window.confirm(confirmMsg)) return;

    setErrorMsg('');
    setActionSuccess('');
    try {
      const { data } = await api.put(`/admin/verify-restaurant/${profileId}`, { action });
      setActionSuccess(data.message);
      fetchPending(); // Refresh list
    } catch (err) {
      setErrorMsg(err.response?.data?.message || 'Profile audit action failed');
    }
  };

  return (
    <div className="container animate-fade-in" style={{ paddingTop: '2.5rem', paddingBottom: '4rem' }}>
      
      <header style={{ marginBottom: '2.5rem' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <ShieldCheck className="text-emerald" /> Profile Audit
        </h1>
        <p className="text-secondary">Verify store names, street addresses, and cuisines before publishing items.</p>
      </header>

      {actionSuccess && (
        <div className="badge badge-success animate-fade-in" style={{ width: '100%', padding: '1rem', marginBottom: '1.5rem', textTransform: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem' }}>
          <Check size={16} /> {actionSuccess}
        </div>
      )}

      {errorMsg && (
        <div className="badge badge-danger" style={{ width: '100%', padding: '1rem', marginBottom: '2rem', display: 'block', textTransform: 'none', textAlign: 'center' }}>
          {errorMsg}
        </div>
      )}

      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem 0', color: 'var(--text-muted)' }}>
          Retrieving pending profiles...
        </div>
      ) : pendingList.length === 0 ? (
        <div className="glass-panel" style={{ padding: '4rem 2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
          <ShieldCheck size={40} style={{ margin: '0 auto 1rem auto', opacity: 0.3 }} />
          <p>No profiles currently awaiting audit. All stores are verified!</p>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Restaurant Name</th>
                <th>Cuisine Category</th>
                <th>Street Address</th>
                <th>Owner details</th>
                <th>Description</th>
                <th style={{ textAlign: 'right' }}>Review Action</th>
              </tr>
            </thead>
            <tbody>
              {pendingList.map((profile) => (
                <tr key={profile._id}>
                  {/* Restaurant name */}
                  <td style={{ fontWeight: 600 }} className="text-indigo">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <Store size={14} /> {profile.restaurantName}
                    </div>
                  </td>

                  {/* Cuisine */}
                  <td>{profile.cuisineType}</td>

                  {/* Address */}
                  <td>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.2rem', fontSize: '0.85rem' }} className="text-secondary">
                      <MapPin size={12} style={{ flexShrink: 0, marginTop: '0.2rem' }} /> {profile.address}
                    </div>
                  </td>

                  {/* Owner info */}
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.15rem', fontSize: '0.85rem' }}>
                      <span style={{ fontWeight: 500 }}>{profile.user?.name || 'N/A'}</span>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{profile.user?.email}</span>
                      <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>{profile.user?.phoneNumber}</span>
                    </div>
                  </td>

                  {/* Description */}
                  <td style={{ maxWidth: '250px' }}>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {profile.description || 'No business description provided.'}
                    </p>
                  </td>

                  {/* Actions */}
                  <td style={{ textAlign: 'right' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', justifyContent: 'flex-end' }}>
                      <button 
                        onClick={() => handleVerifyAction(profile._id, 'approve')}
                        className="btn btn-primary btn-sm"
                        style={{ padding: '0.35rem 0.6rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.2rem' }}
                      >
                        <Check size={12} /> Approve
                      </button>
                      <button 
                        onClick={() => handleVerifyAction(profile._id, 'reject')}
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '0.35rem 0.6rem', fontSize: '0.8rem', color: 'var(--color-danger)', borderColor: 'rgba(239, 68, 68, 0.2)', display: 'flex', alignItems: 'center', gap: '0.2rem' }}
                      >
                        <ShieldX size={12} /> Decline
                      </button>
                    </div>
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

export default RestaurantVerification;
