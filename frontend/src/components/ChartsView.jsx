import React from 'react';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend 
} from 'recharts';
import { TrendingUp, Activity, BarChart2 } from 'lucide-react';

export default function ChartsView({ trendsData, activeView, onViewChange }) {
  
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ background: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', padding: '12px', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}>
          <p style={{ fontWeight: '600', marginBottom: '8px', color: '#fff' }}>{label}</p>
          {payload.map((item, index) => (
            <p key={index} style={{ color: item.color, fontSize: '14px', margin: '4px 0' }}>
              {item.name}: <strong>{typeof item.value === 'number' ? item.value.toFixed(1) : item.value}</strong>
              {item.name.includes('nước') ? ' L' : (item.name.includes('bước') ? ' bước' : (item.name.includes('áp') ? ' mmHg' : (item.name.includes('nặng') ? ' kg' : '')))}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card">
      <div className="dashboard-header">
        <h2 className="form-title" style={{ borderBottom: 'none', marginBottom: '0' }}>
          <TrendingUp size={28} />
          <span>Biểu đồ xu hướng sức khỏe</span>
        </h2>
        
        {/* View selection tabs */}
        <div className="view-controls">
          <button 
            className={`view-btn ${activeView === 'day' ? 'active' : ''}`}
            onClick={() => onViewChange('day')}
          >
            Theo Ngày
          </button>
          <button 
            className={`view-btn ${activeView === 'week' ? 'active' : ''}`}
            onClick={() => onViewChange('week')}
          >
            Theo Tuần
          </button>
          <button 
            className={`view-btn ${activeView === 'month' ? 'active' : ''}`}
            onClick={() => onViewChange('month')}
          >
            Theo Tháng
          </button>
          <button 
            className={`view-btn ${activeView === 'year' ? 'active' : ''}`}
            onClick={() => onViewChange('year')}
          >
            Theo Năm
          </button>
        </div>
      </div>

      {trendsData.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-secondary)' }}>
          Chưa có đủ dữ liệu lịch sử để vẽ biểu đồ. Hãy cập nhật chỉ số thường xuyên hàng ngày.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '40px', marginTop: '24px' }}>
          
          {/* Chart 1: Score trends */}
          <div>
            <h4 style={{ fontSize: '18px', marginBottom: '16px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Activity size={18} color="var(--color-primary)" />
              <span>Chỉ số điểm sức khỏe (Gout, Tim mạch, Chất lượng QoL)</span>
            </h4>
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <LineChart data={trendsData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="date" stroke="var(--text-muted)" style={{ fontSize: '13px' }} />
                  <YAxis domain={[0, 100]} stroke="var(--text-muted)" style={{ fontSize: '13px' }} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '10px' }} />
                  <Line 
                    type="monotone" 
                    dataKey="qol_score" 
                    name="Chất lượng sống (QoL)" 
                    stroke="var(--color-safe)" 
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="gout_score" 
                    name="Nguy cơ Gout" 
                    stroke="var(--color-danger)" 
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="cardio_score" 
                    name="Rủi ro Tim mạch" 
                    stroke="var(--color-warning)" 
                    strokeWidth={2}
                    dot={{ r: 3 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Row for Weight/BP & Steps/Water */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
            
            {/* Chart 2: Blood Pressure & Weight */}
            <div style={{ minWidth: 0 }}>
              <h4 style={{ fontSize: '18px', marginBottom: '16px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <TrendingUp size={18} color="var(--color-accent)" />
                <span>Huyết áp & Cân nặng</span>
              </h4>
              <div style={{ width: '100%', height: 250 }}>
                <ResponsiveContainer>
                  <LineChart data={trendsData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="date" stroke="var(--text-muted)" style={{ fontSize: '12px' }} />
                    <YAxis yAxisId="left" stroke="var(--color-accent)" domain={['dataMin - 5', 'dataMax + 10']} style={{ fontSize: '12px' }} />
                    <YAxis yAxisId="right" orientation="right" stroke="var(--color-safe)" domain={['dataMin - 1', 'dataMax + 1']} style={{ fontSize: '12px' }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '13px' }} />
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="bp_systolic" 
                      name="HA tâm thu" 
                      stroke="var(--color-danger)" 
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      yAxisId="left"
                      type="monotone" 
                      dataKey="bp_diastolic" 
                      name="HA tâm trương" 
                      stroke="var(--color-warning)" 
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      yAxisId="right"
                      type="monotone" 
                      dataKey="weight" 
                      name="Cân nặng (kg)" 
                      stroke="var(--color-safe)" 
                      strokeWidth={2.5}
                      dot={{ r: 3 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Chart 3: Steps & Water */}
            <div style={{ minWidth: 0 }}>
              <h4 style={{ fontSize: '18px', marginBottom: '16px', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BarChart2 size={18} color="var(--color-primary)" />
                <span>Số bước chân & Nước uống</span>
              </h4>
              <div style={{ width: '100%', height: 250 }}>
                <ResponsiveContainer>
                  <BarChart data={trendsData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                    <XAxis dataKey="date" stroke="var(--text-muted)" style={{ fontSize: '12px' }} />
                    <YAxis yAxisId="left" stroke="var(--text-muted)" style={{ fontSize: '12px' }} />
                    <YAxis yAxisId="right" orientation="right" stroke="var(--color-accent)" domain={[0, 4]} style={{ fontSize: '12px' }} />
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '13px' }} />
                    <Bar 
                      yAxisId="left"
                      dataKey="steps" 
                      name="Số bước chân" 
                      fill="rgba(16, 185, 129, 0.4)" 
                      radius={[4, 4, 0, 0]}
                    />
                    <Line 
                      yAxisId="right"
                      type="monotone" 
                      dataKey="water_intake" 
                      name="Nước uống (L)" 
                      stroke="var(--color-accent)" 
                      strokeWidth={2.5}
                      dot={{ r: 3 }}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
