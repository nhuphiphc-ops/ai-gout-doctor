import React, { useState, useEffect } from 'react';
import { AlertTriangle, Compass, RefreshCw, BarChart2 } from 'lucide-react';
import apiService from '../services/api';

export default function CorrelationReport() {
  const [data, setData] = useState(null);
  const [days, setDays] = useState(30);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadCorrelations = async (daysVal) => {
    setLoading(true);
    try {
      const res = await apiService.getCorrelations(daysVal);
      setData(res);
    } catch (err) {
      setError('Lỗi khi tải báo cáo tương quan thực phẩm.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCorrelations(days);
  }, [days]);

  const getBarColorClass = (percentage) => {
    if (percentage >= 60.0) return 'danger';
    if (percentage >= 30.0) return 'warning';
    return 'safe';
  };

  return (
    <div className="card">
      <div className="dashboard-header" style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '16px', marginBottom: '20px' }}>
        <h2 className="form-title" style={{ borderBottom: 'none', marginBottom: '0', paddingBottom: '0' }}>
          <Compass size={28} />
          <span>Bản đồ tương quan Dinh dưỡng & Cơn đau khớp</span>
        </h2>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ fontSize: '15px', color: 'var(--text-secondary)' }}>Khoảng thời gian:</span>
          <select 
            value={days} 
            onChange={(e) => setDays(parseInt(e.target.value))}
            style={{ background: '#1e293b', border: '1px solid var(--border-color)', color: '#fff', padding: '6px 12px', borderRadius: '8px', fontSize: '15px' }}
          >
            <option value={30}>30 ngày gần nhất</option>
            <option value={60}>60 ngày gần nhất</option>
            <option value={90}>90 ngày gần nhất</option>
          </select>
          <button 
            onClick={() => loadCorrelations(days)} 
            style={{ background: 'transparent', border: 'none', color: 'var(--color-primary)', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
          >
            <RefreshCw size={16} />
          </button>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
          Đang tính toán ma trận tương quan thống kê...
        </div>
      ) : error ? (
        <div style={{ color: 'var(--color-danger)', textAlign: 'center', padding: '20px 0' }}>
          {error}
        </div>
      ) : !data || data.correlations.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-secondary)' }}>
          <p style={{ marginBottom: '10px' }}>Chưa ghi nhận đủ dữ liệu cơn đau khớp chân trong vòng {days} ngày qua.</p>
          <p style={{ fontSize: '15px', color: 'var(--text-muted)' }}>
            Hệ thống cần ghi nhận ít nhất một đợt đau/nhức khớp chân và lịch sử thực phẩm trước đó để bắt đầu tính toán tương quan.
          </p>
        </div>
      ) : (
        <div>
          {/* Summary Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', marginBottom: '24px', border: '1px solid var(--border-color)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Số ngày phân tích</div>
              <div style={{ fontSize: '32px', fontWeight: '800', color: 'var(--color-primary)' }}>{data.days_analyzed}</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Số ngày đau nhức chân</div>
              <div style={{ fontSize: '32px', fontWeight: '800', color: 'var(--color-danger)' }}>{data.pain_days_count}</div>
            </div>
          </div>

          <p style={{ fontSize: '16px', color: 'var(--text-secondary)', marginBottom: '20px' }}>
            Tỷ lệ tương quan dưới đây hiển thị <strong>xác suất xảy ra nhức mỏi/đau khớp chân trong vòng 48h</strong> sau khi anh Phi ăn thực phẩm hoặc thực hiện thói quen này:
          </p>

          {/* Correlation Bars List */}
          <div className="correlation-list">
            {data.correlations.map((item, index) => {
              const colorClass = getBarColorClass(item.correlation_percentage);
              return (
                <div key={index} className="correlation-item">
                  <div className="correlation-header">
                    <span style={{ fontSize: '17px', fontWeight: '600' }}>{item.food_name}</span>
                    <span style={{ color: `var(--color-${colorClass})`, fontWeight: '700' }}>
                      {item.correlation_percentage}%
                    </span>
                  </div>
                  
                  <div className="correlation-bar-bg">
                    <div 
                      className={`correlation-bar-fill ${colorClass}`}
                      style={{ width: `${item.correlation_percentage}%` }}
                    />
                  </div>
                  
                  <div style={{ fontSize: '13px', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between' }}>
                    <span>Ăn trước khi đau: {item.pain_incidents_with_food} lần</span>
                    <span>Tổng số ngày ăn: {item.total_consumption} ngày</span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Scientific Disclaimer */}
          <div style={{ marginTop: '30px', padding: '16px', background: 'rgba(245, 158, 11, 0.05)', borderLeft: '4px solid var(--color-warning)', borderRadius: '0 8px 8px 0', display: 'flex', gap: '12px' }}>
            <AlertTriangle size={20} style={{ color: 'var(--color-warning)', flexShrink: 0 }} />
            <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              <strong>Hướng dẫn diễn giải chỉ số:</strong> Các món ăn có tỷ lệ tương quan &gt; 50% được coi là tác nhân nghi ngờ cao gây bùng phát cơn gout cấp của riêng cơ địa anh Phi. Anh nên lưu lại danh sách này và chủ động tránh ăn các món này liên tục nhiều ngày hoặc ăn kèm với bia rượu.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
