import React, { useState } from 'react';
import { 
  AlertTriangle, 
  Droplet, 
  Activity, 
  Moon, 
  TrendingUp, 
  Smile, 
  Utensils, 
  PlusCircle, 
  CheckCircle,
  FileText,
  Video,
  RefreshCw
} from 'lucide-react';
import apiService from '../services/api';

export default function Dashboard({ data, currentUser, onNavigate, onExport, onRefresh }) {
  const todayLog = data?.today_log;
  const recs = todayLog?.ai_recommendations;

  const [syncing, setSyncing] = useState(false);
  const [syncMessage, setSyncMessage] = useState('');
  const [syncError, setSyncError] = useState('');

  const handleSyncSteps = async () => {
    setSyncing(true);
    setSyncMessage('');
    setSyncError('');
    try {
      const response = await apiService.syncSteps();
      setSyncMessage(`Đồng bộ thành công! Số bước chân hôm nay: ${response.steps.toLocaleString()} bước.`);
      if (onRefresh) {
        onRefresh();
      }
    } catch (err) {
      console.error(err);
      setSyncError(err.response?.data?.detail || 'Lỗi khi đồng bộ dữ liệu bước chân từ Google Fit.');
    } finally {
      setSyncing(false);
    }
  };
  
  const getScoreClass = (status) => {
    if (status === 'Danger') return 'danger';
    if (status === 'Warning') return 'warning';
    return 'safe';
  };

  const getScoreLabel = (status) => {
    if (status === 'Danger') return 'Nguy hiểm';
    if (status === 'Warning') return 'Cảnh báo';
    return 'An toàn';
  };

  return (
    <div>
      {/* Gout Danger Red Alert */}
      {recs?.danger_alert && (
        <div className="danger-alert-box">
          <div className="danger-alert-title">
            <AlertTriangle size={32} />
            <span>{recs.danger_alert.title}</span>
          </div>
          <p style={{ fontSize: '18px', fontWeight: '500', marginBottom: '16px', color: '#fff' }}>
            {recs.danger_alert.message}
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
            <div style={{ background: 'rgba(239, 68, 68, 0.15)', padding: '16px', borderRadius: '12px', border: '1px solid rgba(239,68,68,0.3)' }}>
              <strong style={{ color: '#ef4444' }}>Biện pháp tức thời:</strong>
              <ul style={{ paddingLeft: '20px', marginTop: '8px', fontSize: '16px', color: '#fca5a5' }}>
                <li>Uống thêm 1-2 cốc nước ấm lớn ngay lập tức.</li>
                <li>Nằm nghỉ ngơi, kê cao chân bị đau bằng gối.</li>
                <li>Tránh cử động và giữ mát khớp bị sưng.</li>
              </ul>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <strong>Lưu ý:</strong>
              <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginTop: '8px' }}>
                Nếu khớp sưng tấy nóng đỏ dữ dội đi kèm sốt nhẹ, hãy liên hệ ngay với Bác sĩ cơ xương khớp để được kê đơn phù hợp. Tránh tự ý sử dụng thuốc nam không rõ nguồn gốc.
              </p>
            </div>
          </div>
        </div>
      )}

          {/* Video Script Module Button */}
          <div className="card glass-effect" style={{ marginBottom: '24px', padding: '16px' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontSize: '18px', color: '#fff' }}>
              <Video size={20} color="#eab308" />
              Viết Kịch Bản Video Sức Khỏe
            </h4>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              Module AI hỗ trợ sáng tạo kịch bản video đa nền tảng (TikTok, Shorts, YouTube) dành cho kênh Mr. Phi.
            </p>
            <button onClick={() => onNavigate('video_script')} className="btn" style={{ background: 'linear-gradient(135deg, #eab308 0%, #facc15 100%)', color: '#fff', width: '100%', justifyContent: 'center', fontWeight: 'bold' }}>
              <Video size={18} style={{ marginRight: '8px' }} />
              Tạo Kịch Bản Mới
            </button>
          </div>

      {/* Scores Grid */}
      <div className="scores-container">
        {/* QoL Index */}
        <div className="card score-card safe">
          <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>Chỉ Số Sức Khỏe QoL</h3>
          <div className="score-value" style={{ color: 'var(--color-safe)' }}>
            {todayLog ? todayLog.qol_score : '--'}
          </div>
          <span className="score-status" style={{ background: 'var(--color-safe-light)', color: 'var(--color-safe)' }}>
            {todayLog ? 'Chất lượng sống' : 'Chưa cập nhật'}
          </span>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '8px' }}>
            Đánh giá tổng quan giấc ngủ, dinh dưỡng & vận động
          </p>
        </div>

        {/* Gout Risk */}
        <div className={`card score-card ${getScoreClass(todayLog?.gout_score >= 60 ? 'Danger' : (todayLog?.gout_score >= 30 ? 'Warning' : 'Safe'))}`}>
          <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>Nguy Cơ Bùng Phát Gout</h3>
          <div className="score-value">
            {todayLog ? Math.round(todayLog.gout_score) : '--'}
          </div>
          <span className="score-status">
            {todayLog ? getScoreLabel(todayLog.gout_score >= 60 ? 'Danger' : (todayLog?.gout_score >= 30 ? 'Warning' : 'Safe')) : 'Chưa cập nhật'}
          </span>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '8px' }}>
            Tính theo chỉ số purin ăn vào, lượng nước và vận động
          </p>
        </div>

        {/* Cardio Risk */}
        <div className={`card score-card ${getScoreClass(todayLog?.cardio_score >= 60 ? 'Danger' : (todayLog?.cardio_score >= 25 ? 'Warning' : 'Safe'))}`}>
          <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>Chỉ Số Tim Mạch</h3>
          <div className="score-value">
            {todayLog ? Math.round(todayLog.cardio_score) : '--'}
          </div>
          <span className="score-status">
            {todayLog ? getScoreLabel(todayLog.cardio_score >= 60 ? 'Danger' : (todayLog?.cardio_score >= 25 ? 'Warning' : 'Safe')) : 'Chưa cập nhật'}
          </span>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '8px' }}>
            Đánh giá theo Huyết áp, Nhịp tim và chỉ số BMI
          </p>
        </div>

        {/* Metabolic Risk */}
        <div className={`card score-card ${getScoreClass(todayLog?.metabolic_score >= 60 ? 'Danger' : (todayLog?.metabolic_score >= 30 ? 'Warning' : 'Safe'))}`}>
          <h3 style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>Nguy Cơ Chuyển Hóa</h3>
          <div className="score-value">
            {todayLog ? Math.round(todayLog.metabolic_score) : '--'}
          </div>
          <span className="score-status">
            {todayLog ? getScoreLabel(todayLog.metabolic_score >= 60 ? 'Danger' : (todayLog?.metabolic_score >= 30 ? 'Warning' : 'Safe')) : 'Chưa cập nhật'}
          </span>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '8px' }}>
            Đánh giá nguy cơ mỡ máu và đái tháo đường
          </p>
        </div>
      </div>

      {/* Main Dashboard Panel */}
      <div className="dashboard-grid">
        
        {/* Left Side: Daily Recommendations & Status */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          
          {/* AI Daily Advice */}
          <div className="card">
            <h2 className="form-title" style={{ borderBottom: 'none', marginBottom: '16px' }}>
              <Smile size={28} />
              <span>Bác sĩ gia đình AI tư vấn hôm nay</span>
            </h2>
            
            {!todayLog ? (
              <div style={{ textAlign: 'center', padding: '30px 0' }}>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '16px' }}>
                  Chào anh Phi! Hãy cập nhật nhật ký sức khỏe hôm nay để AI phân tích và đưa ra tư vấn.
                </p>
                <div style={{ display: 'flex', gap: '16px', justifyContent: 'center' }}>
                  <button className="btn" style={{ width: 'auto' }} onClick={() => onNavigate('morning')}>
                    Cập nhật Buổi Sáng
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                
                {/* Diet recommendation */}
                <div className="rec-section">
                  <div className="rec-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Utensils size={18} color="var(--color-primary)" />
                    <span>Chế độ dinh dưỡng khuyên dùng:</span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginTop: '8px' }}>
                    <div style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(16, 185, 129, 0.1)' }}>
                      <strong style={{ color: 'var(--color-safe)', fontSize: '16px' }}>Nên dùng:</strong>
                      <ul className="rec-list" style={{ marginTop: '8px' }}>
                        {recs?.diet?.eat?.map((item, i) => <li key={i}>{item}</li>)}
                      </ul>
                    </div>
                    <div style={{ background: 'rgba(239, 68, 68, 0.05)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(239, 68, 68, 0.1)' }}>
                      <strong style={{ color: 'var(--color-danger)', fontSize: '16px' }}>Hạn chế:</strong>
                      <ul className="rec-list limit" style={{ marginTop: '8px' }}>
                        {recs?.diet?.limit?.map((item, i) => <li key={i}>{item}</li>)}
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Water recommendation */}
                <div className="rec-section">
                  <div className="rec-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Droplet size={18} color="var(--color-accent)" />
                    <span>Lượng nước cần bù:</span>
                  </div>
                  <p style={{ fontSize: '16px', background: 'rgba(99, 102, 241, 0.05)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(99, 102, 241, 0.1)', marginTop: '8px' }}>
                    {recs?.water}
                  </p>
                </div>

                {/* Exercise recommendation */}
                <div className="rec-section">
                  <div className="rec-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Activity size={18} color="var(--color-warning)" />
                    <span>Vận động và Phục hồi:</span>
                  </div>
                  <ul className="rec-list" style={{ marginTop: '8px' }}>
                    {recs?.activity?.map((item, i) => <li key={i}>{item}</li>)}
                  </ul>
                </div>

                {/* Specific warnings */}
                {recs?.warnings?.length > 0 && (
                  <div className="rec-section">
                    <div className="rec-title" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-warning)' }}>
                      <AlertTriangle size={18} />
                      <span>Các yếu tố rủi ro ghi nhận:</span>
                    </div>
                    <ul className="rec-list limit" style={{ marginTop: '8px', color: '#fbcfe8' }}>
                      {recs?.warnings?.map((item, i) => <li key={i}>{item}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Today's Log Card */}
          {todayLog && (
            <div className="card">
              <h2 className="form-title" style={{ borderBottom: 'none', marginBottom: '16px' }}>
                <CheckCircle size={28} color="var(--color-safe)" />
                <span>Nhật ký chỉ số hôm nay</span>
              </h2>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
                <div>
                  <h4 style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Nhật Ký Buổi Sáng</h4>
                  <ul style={{ listStyle: 'none', fontSize: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <li>Cân nặng: <strong>{todayLog.weight || '--'} kg</strong></li>
                    <li>Huyết áp: <strong>{todayLog.bp_systolic ? `${todayLog.bp_systolic}/${todayLog.bp_diastolic}` : '--'} mmHg</strong></li>
                    <li>Nhịp tim: <strong>{todayLog.heart_rate || '--'} bpm</strong></li>
                    <li>Giấc ngủ: <strong>{todayLog.sleep_duration || '--'}h</strong> (Chất lượng: <strong>{todayLog.sleep_quality || '--'}/10</strong>)</li>
                    <li>Đau khớp chân: <span className={todayLog.joint_pain ? 'pill danger' : 'pill safe'}>{todayLog.joint_pain ? 'Có đau' : 'Bình thường'}</span></li>
                  </ul>
                </div>

                <div>
                  <h4 style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '8px' }}>Nhật Ký Buổi Chiều</h4>
                  {todayLog.afternoon_completed ? (
                    <ul style={{ listStyle: 'none', fontSize: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                      <li>Vận động: <strong>{todayLog.steps.toLocaleString()} bước</strong> ({todayLog.walking_duration + todayLog.exercise_duration} phút)</li>
                      <li>Nước uống: <strong>{todayLog.water_intake} lít</strong> / 2.5L</li>
                      <li>
                        Thực phẩm: 
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginTop: '6px' }}>
                          {todayLog.had_beer && <span className="pill danger">Bia</span>}
                          {todayLog.had_alcohol && !todayLog.had_beer && <span className="pill danger">Rượu</span>}
                          {todayLog.had_seafood && <span className="pill danger">Hải sản</span>}
                          {todayLog.had_organ_meat && <span className="pill danger">Nội tạng</span>}
                          {todayLog.had_red_meat && <span className="pill danger">Thịt đỏ</span>}
                          {todayLog.had_sweets && <span className="pill warning">Đồ ngọt</span>}
                          {(!todayLog.had_beer && !todayLog.had_alcohol && !todayLog.had_seafood && !todayLog.had_organ_meat && !todayLog.had_red_meat && !todayLog.had_sweets) && <span className="pill safe">Không chất kích thích</span>}
                        </div>
                      </li>
                      {todayLog.foods.length > 0 && (
                        <li>Món ăn khác: {todayLog.foods.map(f => f.food_name).join(', ')}</li>
                      )}
                      {todayLog.medications.length > 0 && (
                        <li>Thuốc dùng: <strong>{todayLog.medications.map(m => m.med_name).join(', ')}</strong></li>
                      )}
                    </ul>
                  ) : (
                    <div style={{ padding: '12px', background: 'rgba(255,255,255,0.02)', borderRadius: '10px', border: '1px dashed var(--border-color)', textAlign: 'center' }}>
                      <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '10px' }}>
                        Chưa cập nhật hoạt động buổi chiều.
                      </p>
                      <button className="btn btn-secondary" style={{ padding: '8px 16px', fontSize: '15px' }} onClick={() => onNavigate('afternoon')}>
                        Nhập hoạt động chiều
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

        </div>

        {/* Right Side: Quick Check-in Links & Report Exporter */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          
          {/* Quick Check-in Box */}
          <div className="card" style={{ background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(23, 32, 53, 0.7) 100%)' }}>
            <h3 style={{ fontSize: '20px', marginBottom: '12px', color: '#fff' }}>Cập nhật hôm nay</h3>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '20px' }}>
              Hãy duy trì ghi chép để AI hiểu rõ thói quen sinh hoạt và chỉ số cơ xương khớp của anh.
            </p>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <button 
                className={`btn ${todayLog?.morning_completed ? 'btn-secondary' : ''}`}
                onClick={() => onNavigate('morning')}
              >
                <PlusCircle size={20} />
                <span>{todayLog?.morning_completed ? 'Sửa chỉ số Buổi Sáng (07:00)' : 'Nhập chỉ số Buổi Sáng (07:00)'}</span>
              </button>
              
              <button 
                className={`btn ${todayLog?.afternoon_completed ? 'btn-secondary' : ''}`}
                onClick={() => onNavigate('afternoon')}
              >
                <PlusCircle size={20} />
                <span>{todayLog?.afternoon_completed ? 'Sửa hoạt động Buổi Chiều (17:00)' : 'Nhập hoạt động Buổi Chiều (17:00)'}</span>
              </button>

              {currentUser?.google_fit_connected && (
                <div style={{ borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '12px', marginTop: '4px' }}>
                  <button 
                    className="btn" 
                    style={{ 
                      background: syncing ? 'rgba(99, 102, 241, 0.2)' : 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)', 
                      color: '#fff',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '8px',
                      cursor: syncing ? 'not-allowed' : 'pointer'
                    }}
                    onClick={handleSyncSteps}
                    disabled={syncing}
                  >
                    <RefreshCw size={20} className={syncing ? 'spin-animation' : ''} />
                    <span>{syncing ? 'Đang đồng bộ...' : 'Đồng bộ bước chân Google Fit'}</span>
                  </button>
                  {syncMessage && (
                    <p style={{ color: 'var(--color-safe)', fontSize: '13px', marginTop: '8px', textAlign: 'center', fontWeight: '500' }}>{syncMessage}</p>
                  )}
                  {syncError && (
                    <p style={{ color: 'var(--color-danger)', fontSize: '13px', marginTop: '8px', textAlign: 'center', fontWeight: '500' }}>{syncError}</p>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Export Center */}
          <div className="card">
            <h3 style={{ fontSize: '20px', marginBottom: '12px' }}>Xuất báo cáo sức khỏe</h3>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '20px' }}>
              Xuất dữ liệu lịch sử để gửi cho bác sĩ điều trị hoặc lưu trữ cá nhân.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <button className="export-btn" style={{ justifyContent: 'center' }} onClick={() => onExport('excel')}>
                <FileText size={18} color="#10b981" />
                <span>Tải Báo cáo Excel (.xlsx)</span>
              </button>
              <button className="export-btn" style={{ justifyContent: 'center' }} onClick={() => onExport('pdf')}>
                <FileText size={18} color="#ef4444" />
                <span>Tải Báo cáo PDF (.pdf)</span>
              </button>
              <button className="export-btn" style={{ justifyContent: 'center' }} onClick={() => onExport('word')}>
                <FileText size={18} color="#6366f1" />
                <span>Tải Báo cáo Word (.docx)</span>
              </button>
            </div>
          </div>

          {/* Recovery Guide Button */}
          <div className="card glass-effect" style={{ marginBottom: '24px', padding: '16px' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontSize: '18px', color: '#fff' }}>
              <Activity size={20} color="#22c55e" />
              Tài Liệu Khắc Phục Bệnh
            </h4>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              Phân tích tổng hợp các chỉ số y tế đang cảnh báo (axit uric, thận, tuyến giáp...) và lập kế hoạch phục hồi có giọng đọc AI.
            </p>
            <button onClick={() => onNavigate('guide')} className="btn" style={{ background: 'linear-gradient(135deg, #16a34a 0%, #22c55e 100%)', color: '#fff', width: '100%', justifyContent: 'center', fontWeight: 'bold' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ marginRight: '8px' }}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              Xem Cẩm nang Khắc phục
            </button>
          </div>

          {/* Tips Box */}
          <div className="card" style={{ borderLeft: '4px solid var(--color-primary)' }}>
            <h4 style={{ color: 'var(--color-primary)', marginBottom: '8px', fontSize: '17px' }}>Lời khuyên của chuyên gia</h4>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)' }}>
              "Với người bị gout lâu năm, cơ thể tích lũy các hạt tophi vi mô ở các khớp. Đi bộ nhẹ giúp lưu thông dịch khớp, giảm lắng đọng muối urat cực tốt."
            </p>
          </div>

        </div>

      </div>
    </div>
  );
}
