import React, { useState, useEffect } from 'react';
import { Sun, ArrowLeft, Info, Heart, Moon } from 'lucide-react';
import apiService from '../services/api';

export default function MorningForm({ todayLog, onSave, onCancel }) {
  const [weight, setWeight] = useState(62.5);
  const [bpSystolic, setBpSystolic] = useState(120);
  const [bpDiastolic, setBpDiastolic] = useState(80);
  const [heartRate, setHeartRate] = useState(70);
  const [sleepQuality, setSleepQuality] = useState(8);
  const [sleepDuration, setSleepDuration] = useState(7.5);
  
  const [jointPain, setJointPain] = useState(false);
  const [painBigToe, setPainBigToe] = useState(false);
  const [painAnkle, setPainAnkle] = useState(false);
  const [painKnee, setPainKnee] = useState(false);
  const [painFoot, setPainFoot] = useState(false);
  const [painSeverity, setPainSeverity] = useState(0);
  
  const [fatigueLevel, setFatigueLevel] = useState(3);
  const [stressLevel, setStressLevel] = useState(3);
  const [moodLevel, setMoodLevel] = useState(8);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Populate data if already exists
  useEffect(() => {
    if (todayLog && todayLog.morning_completed) {
      setWeight(todayLog.weight || 62.5);
      setBpSystolic(todayLog.bp_systolic || 120);
      setBpDiastolic(todayLog.bp_diastolic || 80);
      setHeartRate(todayLog.heart_rate || 70);
      setSleepQuality(todayLog.sleep_quality || 8);
      setSleepDuration(todayLog.sleep_duration || 7.5);
      setJointPain(todayLog.joint_pain || false);
      setPainBigToe(todayLog.pain_big_toe || false);
      setPainAnkle(todayLog.pain_ankle || false);
      setPainKnee(todayLog.pain_knee || false);
      setPainFoot(todayLog.pain_foot || false);
      setPainSeverity(todayLog.pain_severity || 0);
      setFatigueLevel(todayLog.fatigue_level || 3);
      setStressLevel(todayLog.stress_level || 3);
      setMoodLevel(todayLog.mood_level || 8);
    }
  }, [todayLog]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const payload = {
      weight: parseFloat(weight),
      bp_systolic: parseInt(bpSystolic),
      bp_diastolic: parseInt(bpDiastolic),
      heart_rate: parseInt(heartRate),
      sleep_quality: parseInt(sleepQuality),
      sleep_duration: parseFloat(sleepDuration),
      joint_pain: jointPain,
      pain_big_toe: jointPain ? painBigToe : false,
      pain_ankle: jointPain ? painAnkle : false,
      pain_knee: jointPain ? painKnee : false,
      pain_foot: jointPain ? painFoot : false,
      pain_severity: jointPain ? parseInt(painSeverity) : 0,
      fatigue_level: parseInt(fatigueLevel),
      stress_level: parseInt(stressLevel),
      mood_level: parseInt(moodLevel),
    };

    try {
      const response = await apiService.submitMorningLog(payload);
      onSave(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra khi gửi dữ liệu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <button 
        onClick={onCancel}
        className="nav-btn" 
        style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '20px', padding: '6px 12px' }}
      >
        <ArrowLeft size={16} />
        <span>Quay lại Dashboard</span>
      </button>

      <h2 className="form-title">
        <Sun size={28} color="var(--color-warning)" />
        <span>Cập nhật sức khỏe Buổi Sáng (07:00)</span>
      </h2>

      {error && (
        <div style={{ background: 'var(--color-danger-light)', border: '1px solid var(--color-danger)', color: 'var(--color-danger)', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '16px' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        
        {/* Row 1: Weight & BP */}
        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="weight">Cân nặng hiện tại (kg)</label>
            <input 
              type="number" 
              step="0.1"
              id="weight"
              className="form-input"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              required
            />
          </div>
          
          <div className="form-row" style={{ gap: '10px' }}>
            <div className="form-group">
              <label className="form-label" htmlFor="bp_sys">HA tâm thu (Max)</label>
              <input 
                type="number" 
                id="bp_sys"
                className="form-input"
                value={bpSystolic}
                onChange={(e) => setBpSystolic(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="bp_dia">HA tâm trương (Min)</label>
              <input 
                type="number" 
                id="bp_dia"
                className="form-input"
                value={bpDiastolic}
                onChange={(e) => setBpDiastolic(e.target.value)}
                required
              />
            </div>
          </div>
        </div>

        {/* Row 2: Heart Rate & Sleep duration */}
        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="heart_rate">
              Nhịp tim tĩnh (bpm) <Heart size={14} style={{ display: 'inline', color: 'var(--color-danger)' }} />
            </label>
            <input 
              type="number" 
              id="heart_rate"
              className="form-input"
              value={heartRate}
              onChange={(e) => setHeartRate(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="sleep_duration">
              Thời gian ngủ (giờ) <Moon size={14} style={{ display: 'inline', color: 'var(--color-accent)' }} />
            </label>
            <input 
              type="number" 
              step="0.5"
              id="sleep_duration"
              className="form-input"
              value={sleepDuration}
              onChange={(e) => setSleepDuration(e.target.value)}
              required
            />
          </div>
        </div>

        {/* Sleep Quality */}
        <div className="form-group">
          <label className="form-label">Chất lượng giấc ngủ: <strong>{sleepQuality}/10</strong></label>
          <input 
            type="range" 
            min="1" 
            max="10" 
            className="form-input" 
            style={{ padding: '0' }}
            value={sleepQuality}
            onChange={(e) => setSleepQuality(parseInt(e.target.value))}
          />
          <div style={{ display: 'flex', justifyContent: 'between', fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
            <span>Rất trằn trọc / Mất ngủ</span>
            <span style={{ marginLeft: 'auto' }}>Ngủ sâu / Sảng khoái</span>
          </div>
        </div>

        {/* Joint Pain switch */}
        <div className="form-group" style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <strong style={{ fontSize: '18px' }}>Tình trạng đau tức / Nhức mỏi khớp chân</strong>
              <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
                Tích chọn nếu anh cảm thấy bất kỳ dấu hiệu nhức mỏi, đau châm chích vùng chân sáng nay.
              </p>
            </div>
            <button
              type="button"
              className={`btn ${jointPain ? 'btn-danger' : 'btn-secondary'}`}
              style={{ width: 'auto', padding: '10px 24px', fontSize: '16px' }}
              onClick={() => setJointPain(!jointPain)}
            >
              {jointPain ? 'CÓ ĐAU' : 'BÌNH THƯỜNG'}
            </button>
          </div>

          {/* Conditional Joint Pain Sub-form */}
          {jointPain && (
            <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid var(--border-color)' }}>
              <label className="form-label">Chọn cụ thể vị trí đau (Chọn nhiều vị trí nếu có):</label>
              
              <div className="pain-areas-grid">
                <div 
                  className={`pain-checkbox-card ${painBigToe ? 'selected' : ''}`}
                  onClick={() => setPainBigToe(!painBigToe)}
                >
                  <div style={{ fontSize: '15px' }}>Khớp Ngón Cái</div>
                  <div style={{ fontSize: '12px', opacity: 0.7 }}>(Hay gặp nhất)</div>
                </div>
                
                <div 
                  className={`pain-checkbox-card ${painAnkle ? 'selected' : ''}`}
                  onClick={() => setPainAnkle(!painAnkle)}
                >
                  <div style={{ fontSize: '15px' }}>Khớp Mắt Cá</div>
                </div>
                
                <div 
                  className={`pain-checkbox-card ${painKnee ? 'selected' : ''}`}
                  onClick={() => setPainKnee(!painKnee)}
                >
                  <div style={{ fontSize: '15px' }}>Khớp Đầu Gối</div>
                </div>

                <div 
                  className={`pain-checkbox-card ${painFoot ? 'selected' : ''}`}
                  onClick={() => setPainFoot(!painFoot)}
                >
                  <div style={{ fontSize: '15px' }}>Bàn chân / Gót</div>
                </div>
              </div>

              <div className="form-group" style={{ marginTop: '20px' }}>
                <label className="form-label">Mức độ đau khớp chân hiện tại: <strong>{painSeverity}/10</strong></label>
                <input 
                  type="range" 
                  min="1" 
                  max="10" 
                  className="form-input" 
                  style={{ padding: '0' }}
                  value={painSeverity}
                  onChange={(e) => setPainSeverity(parseInt(e.target.value))}
                />
                <div style={{ display: 'flex', justifyContent: 'between', fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
                  <span>Nhói nhẹ / Thỉnh thoảng nhức</span>
                  <span style={{ marginLeft: 'auto' }}>Đau dữ dội / Sưng tấy đỏ / Không đi lại được</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Mood and Stress Levels */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginTop: '20px' }}>
          
          <div className="form-group">
            <label className="form-label">Mức độ mệt mỏi cơ thể: <strong>{fatigueLevel}/10</strong></label>
            <input 
              type="range" 
              min="1" 
              max="10" 
              className="form-input" 
              style={{ padding: '0' }}
              value={fatigueLevel}
              onChange={(e) => setFatigueLevel(parseInt(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Mức độ stress tinh thần: <strong>{stressLevel}/10</strong></label>
            <input 
              type="range" 
              min="1" 
              max="10" 
              className="form-input" 
              style={{ padding: '0' }}
              value={stressLevel}
              onChange={(e) => setStressLevel(parseInt(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Tâm trạng sáng nay: <strong>{moodLevel}/10</strong></label>
            <input 
              type="range" 
              min="1" 
              max="10" 
              className="form-input" 
              style={{ padding: '0' }}
              value={moodLevel}
              onChange={(e) => setMoodLevel(parseInt(e.target.value))}
            />
          </div>

        </div>

        <div style={{ marginTop: '30px' }}>
          <button 
            type="submit" 
            className="btn" 
            disabled={loading}
          >
            {loading ? 'Đang lưu...' : 'Lưu chỉ số Buổi Sáng'}
          </button>
        </div>

      </form>
    </div>
  );
}
