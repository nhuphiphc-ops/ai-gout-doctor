import React, { useState, useEffect } from 'react';
import { User, Save, Info } from 'lucide-react';
import apiService from '../services/api';

export default function ProfileView({ onProfileUpdate }) {
  const [name, setName] = useState('');
  const [age, setAge] = useState(47);
  const [height, setHeight] = useState(1.70);
  const [targetWeight, setTargetWeight] = useState(62.5);
  const [googleFitConnected, setGoogleFitConnected] = useState(false);
  const [avatarUrl, setAvatarUrl] = useState('');
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const user = await apiService.getProfile();
        setName(user.name || '');
        setAge(user.age || 47);
        setHeight(user.height || 1.70);
        setTargetWeight(user.target_weight || 62.5);
        setGoogleFitConnected(user.google_fit_connected || false);
        setAvatarUrl(user.avatar_url || '');
      } catch (err) {
        console.error('Lỗi khi tải thông tin cá nhân', err);
      }
    };
    loadProfile();
  }, []);

  const handleAvatarUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    setUploadingAvatar(true);
    setError('');
    setMessage('');
    
    try {
      const res = await apiService.uploadAvatar(file);
      setAvatarUrl(res.avatar_url);
      setMessage('Tải ảnh đại diện thành công!');
      if (onProfileUpdate) {
        const updatedUser = await apiService.getProfile();
        onProfileUpdate(updatedUser);
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Lỗi khi tải ảnh đại diện lên.');
    } finally {
      setUploadingAvatar(false);
    }
  };

  const handleConnectGoogleFit = async () => {
    try {
      const res = await apiService.getGoogleFitUrl();
      if (res.url) {
        window.location.href = res.url;
      }
    } catch (err) {
      setError('Lỗi khi lấy link liên kết Google Fit.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    const payload = {
      email: apiService.getCurrentUser()?.email || 'mrphi@health.local',
      name: name,
      age: parseInt(age),
      height: parseFloat(height),
      target_weight: parseFloat(targetWeight),
    };

    try {
      const response = await apiService.updateProfile(payload);
      setMessage('Cập nhật thông tin cá nhân thành công!');
      if (onProfileUpdate) {
        onProfileUpdate(response);
      }
    } catch (err) {
      setError('Có lỗi xảy ra khi cập nhật thông tin.');
    } finally {
      setLoading(false);
    }
  };

  const bmi = targetWeight / (height * height);

  return (
    <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2 className="form-title">
        <User size={28} />
        <span>Thông tin cá nhân & Mục tiêu sức khỏe</span>
      </h2>

      {message && (
        <div style={{ background: 'var(--color-safe-light)', border: '1px solid var(--color-safe)', color: 'var(--color-safe)', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '16px' }}>
          {message}
        </div>
      )}

      {error && (
        <div style={{ background: 'var(--color-danger-light)', border: '1px solid var(--color-danger)', color: 'var(--color-danger)', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '16px' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Avatar Upload Section */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', marginBottom: '28px', background: 'rgba(255,255,255,0.01)', padding: '20px', borderRadius: '16px', border: '1px solid var(--border-color)' }}>
          <div style={{ position: 'relative', width: '100px', height: '100px', borderRadius: '50%', border: '3px solid var(--color-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '36px', fontWeight: '800', background: '#334155', overflow: 'hidden' }}>
            {avatarUrl ? (
              <img src={avatarUrl} alt="Avatar" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            ) : (
              name ? name.charAt(0) : 'P'
            )}
            {uploadingAvatar && (
              <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '14px', color: '#fff' }}>
                Đang tải...
              </div>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
            <label className="btn btn-secondary" style={{ width: 'auto', padding: '8px 16px', fontSize: '15px', cursor: 'pointer', display: 'inline-flex', gap: '8px' }}>
              <span>{uploadingAvatar ? 'Đang tải...' : 'Chọn ảnh khuôn mặt'}</span>
              <input 
                type="file" 
                accept="image/*" 
                onChange={handleAvatarUpload} 
                style={{ display: 'none' }} 
                disabled={uploadingAvatar}
              />
            </label>
            <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Hỗ trợ ảnh định dạng JPG, PNG hoặc WEBP</span>
          </div>
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="name">Họ và tên</label>
          <input 
            type="text" 
            id="name"
            className="form-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="age">Tuổi (năm)</label>
          <input 
            type="number" 
            id="age"
            className="form-input"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="height">Chiều cao (m)</label>
            <input 
              type="number" 
              step="0.01"
              id="height"
              className="form-input"
              value={height}
              onChange={(e) => setHeight(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="target_weight">Cân nặng mục tiêu (kg)</label>
            <input 
              type="number" 
              step="0.1"
              id="target_weight"
              className="form-input"
              value={targetWeight}
              onChange={(e) => setTargetWeight(e.target.value)}
              required
            />
          </div>
        </div>

        {/* BMI Card Display */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', marginBottom: '24px', display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ background: 'var(--color-safe-light)', padding: '12px', borderRadius: '50%', color: 'var(--color-safe)', fontSize: '24px', fontWeight: '800', width: '60px', height: '60px', display: 'flex', alignItems: 'center', justify: 'center' }}>
            {bmi.toFixed(1)}
          </div>
          <div>
            <strong>Chỉ số BMI lý thuyết của anh: {bmi.toFixed(1)}</strong>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px' }}>
              Trạng thái: <strong>{bmi >= 18.5 && bmi < 25.0 ? 'Bình thường (Lý tưởng)' : 'Ngoài ngưỡng tối ưu'}</strong>. Anh Phi không béo phì, cân nặng ở mức cân đối.
            </p>
          </div>
        </div>

        {/* Google Fit Integration Card */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', marginBottom: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <strong style={{ fontSize: '17px' }}>Đồng bộ bước chân Google Fit</strong>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginTop: '4px' }}>
                {googleFitConnected 
                  ? '✓ Đã liên kết tài khoản Google Fit thành công.' 
                  : 'Liên kết Google Fit để tự động đồng bộ số bước chân của anh Phi.'}
              </p>
            </div>
            
            {googleFitConnected ? (
              <span className="pill safe" style={{ display: 'flex', alignItems: 'center', gap: '4px', padding: '8px 16px', fontSize: '15px' }}>
                ✓ ĐÃ LIÊN KẾT
              </span>
            ) : (
              <button
                type="button"
                className="btn"
                style={{ width: 'auto', padding: '10px 20px', fontSize: '15px' }}
                onClick={handleConnectGoogleFit}
              >
                KẾT NỐI
              </button>
            )}
          </div>
        </div>

        <button 
          type="submit" 
          className="btn" 
          disabled={loading}
          style={{ display: 'inline-flex', gap: '8px' }}
        >
          <Save size={20} />
          <span>{loading ? 'Đang lưu...' : 'Lưu thông tin'}</span>
        </button>
      </form>
    </div>
  );
}
