import React, { useState } from 'react';
import { Calendar, Eye, EyeOff } from 'lucide-react';

export default function HistoryTable({ logs }) {
  const [selectedLogId, setSelectedLogId] = useState(null);

  const getPainBadge = (log) => {
    if (log.joint_pain) {
      const parts = [];
      if (log.pain_big_toe) parts.push("Ngón cái");
      if (log.pain_ankle) parts.push("Mắt cá");
      if (log.pain_knee) parts.push("Gối");
      if (log.pain_foot) parts.push("Bàn chân");
      
      const loc = parts.length > 0 ? ` (${parts.join(', ')})` : '';
      return <span className="pill danger">Đau{loc} - Cấp độ {log.pain_severity}</span>;
    }
    return <span className="pill safe">Không đau</span>;
  };

  const getScorePill = (score) => {
    if (score >= 60) return <span className="pill danger">{Math.round(score)}</span>;
    if (score >= 30) return <span className="pill warning">{Math.round(score)}</span>;
    return <span className="pill safe">{Math.round(score)}</span>;
  };

  const toggleDetail = (id) => {
    if (selectedLogId === id) {
      setSelectedLogId(null);
    } else {
      setSelectedLogId(id);
    }
  };

  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
  };

  if (!logs || logs.length === 0) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
        Không có lịch sử nhật ký nào. Bắt đầu ghi chỉ số hôm nay để tạo lịch sử sức khỏe.
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="form-title" style={{ borderBottom: 'none', marginBottom: '16px' }}>
        <Calendar size={28} />
        <span>Lịch sử nhật ký sức khỏe</span>
      </h2>

      <div className="history-table-container">
        <table className="history-table">
          <thead>
            <tr>
              <th>Ngày</th>
              <th>Cân nặng</th>
              <th>Huyết áp</th>
              <th>Nhịp tim</th>
              <th>Giấc ngủ</th>
              <th>Số bước</th>
              <th>Nước uống</th>
              <th>Khớp chân</th>
              <th>Điểm Gout</th>
              <th>Điểm QoL</th>
              <th>Chi tiết</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <React.Fragment key={log.id}>
                <tr>
                  <td><strong>{formatDate(log.log_date)}</strong></td>
                  <td>{log.weight ? `${log.weight} kg` : '--'}</td>
                  <td>{log.bp_systolic ? `${log.bp_systolic}/${log.bp_diastolic}` : '--'}</td>
                  <td>{log.heart_rate ? `${log.heart_rate} bpm` : '--'}</td>
                  <td>{log.sleep_duration ? `${log.sleep_duration}h` : '--'}</td>
                  <td>{log.steps ? log.steps.toLocaleString() : '0'}</td>
                  <td>{log.water_intake ? `${log.water_intake} L` : '0 L'}</td>
                  <td>{getPainBadge(log)}</td>
                  <td>{getScorePill(log.gout_score)}</td>
                  <td><strong style={{ color: 'var(--color-safe)' }}>{log.qol_score}</strong></td>
                  <td>
                    <button 
                      onClick={() => toggleDetail(log.id)}
                      style={{ background: 'transparent', border: 'none', color: 'var(--color-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                    >
                      {selectedLogId === log.id ? <EyeOff size={18} /> : <Eye size={18} />}
                    </button>
                  </td>
                </tr>

                {/* Conditional detailed row */}
                {selectedLogId === log.id && (
                  <tr>
                    <td colSpan="11" style={{ background: 'rgba(255,255,255,0.01)', padding: '20px', borderTop: 'none' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', fontSize: '15px' }}>
                        <div>
                          <strong style={{ color: 'var(--color-primary)' }}>Chỉ số sức khỏe:</strong>
                          <ul style={{ listStyle: 'none', marginTop: '8px', paddingLeft: '0', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                            <li>Mệt mỏi: <strong>{log.fatigue_level || '--'}/10</strong></li>
                            <li>Căng thẳng: <strong>{log.stress_level || '--'}/10</strong></li>
                            <li>Tâm trạng: <strong>{log.mood_level || '--'}/10</strong></li>
                            <li>Học tập/Tập luyện: <strong>{log.exercise_duration || '0'} phút</strong></li>
                          </ul>
                        </div>

                        <div>
                          <strong style={{ color: 'var(--color-warning)' }}>Thực phẩm purin & rượu bia:</strong>
                          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginTop: '8px' }}>
                            {log.had_beer && <span className="pill danger">Bia</span>}
                            {log.had_alcohol && !log.had_beer && <span className="pill danger">Rượu</span>}
                            {log.had_seafood && <span className="pill danger">Hải sản</span>}
                            {log.had_organ_meat && <span className="pill danger">Nội tạng</span>}
                            {log.had_red_meat && <span className="pill danger">Thịt đỏ</span>}
                            {log.had_sweets && <span className="pill warning">Đồ ngọt</span>}
                            {(!log.had_beer && !log.had_alcohol && !log.had_seafood && !log.had_organ_meat && !log.had_red_meat && !log.had_sweets) && <span className="pill safe">Không ăn purin</span>}
                          </div>
                        </div>

                        <div>
                          <strong style={{ color: 'var(--color-accent)' }}>Món ăn & Thuốc trong ngày:</strong>
                          <p style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
                            <strong>Đã ăn:</strong> {log.foods.length > 0 ? log.foods.map(f => f.food_name).join(', ') : 'Không nhập món ăn cụ thể'}<br/>
                            <strong>Đã uống:</strong> {log.medications.length > 0 ? log.medications.map(m => m.med_name).join(', ') : 'Không dùng thuốc'}
                          </p>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
