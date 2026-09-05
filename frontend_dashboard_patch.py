import re

with open('frontend/src/components/Dashboard.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add an icon import for Video
if 'Video' not in text:
    text = text.replace('FileText,', 'FileText,\n  Video,')

new_button = '''          {/* Video Script Module Button */}
          <div className="card glass-effect" style={{ marginBottom: '24px', padding: '16px' }}>
            <h4 style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', fontSize: '18px', color: '#fff' }}>
              <Video size={20} color="#8b5cf6" />
              Viết Kịch Bản Video Sức Khỏe
            </h4>
            <p style={{ fontSize: '15px', color: 'var(--text-secondary)', marginBottom: '16px' }}>
              Module AI hỗ trợ sáng tạo kịch bản video đa nền tảng (TikTok, Shorts, YouTube) dành cho kênh Mr. Phi.
            </p>
            <button onClick={() => onNavigate('video_script')} className="btn" style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #a855f7 100%)', color: '#fff', width: '100%', justifyContent: 'center', fontWeight: 'bold' }}>
              <Video size={18} style={{ marginRight: '8px' }} />
              Tạo Kịch Bản Mới
            </button>
          </div>

          {/* Recovery Guide Button */}'''

text = text.replace('          {/* Recovery Guide Button */}', new_button)

with open('frontend/src/components/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
