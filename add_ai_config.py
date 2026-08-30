import re

with open('frontend/src/components/Dashboard.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

ai_card = '''
          {/* AI Config Center */}
          <div className="card" style={{ marginTop: '20px' }}>
            <button 
              onClick={() => onNavigate('chat')}
              className="btn" 
              style={{ background: 'rgba(255,255,255,0.05)', width: '100%', justifyContent: 'center', marginBottom: '24px' }}
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{marginRight: '8px'}}><path d="m3 21 1.9-5.7a8.5 8.5 0 1 1 3.8 3.8z"/></svg>
              <span>Mở khung Trợ lý AI Q&A</span>
            </button>
            
            <div style={{ borderBottom: '1px solid var(--border-color)', marginBottom: '24px' }}></div>

            <h3 style={{ fontSize: '16px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              🔑 CẤU HÌNH AI
            </h3>
            
            {localStorage.getItem('gemini_api_key') ? (
              <p style={{ color: 'var(--color-safe)', fontSize: '14px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '500' }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                Đã lưu key trên máy này <span style={{ color: 'var(--text-muted)', fontWeight: 'normal' }}>— model gemini-2.5-flash</span>
              </p>
            ) : (
              <p style={{ color: 'var(--color-warning)', fontSize: '14px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '500' }}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                Chưa có API Key
              </p>
            )}

            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '20px', lineHeight: '1.6' }}>
              Khi triển khai trên Vercel, hãy đặt biến môi trường GEMINI_API_KEY (Settings &rarr; Environment Variables) — đó là cách an toàn nhất vì key không bao giờ rời server. Ô dưới đây chỉ dùng khi chạy thử cục bộ: key được lưu trong trình duyệt của riêng máy này.
            </p>

            <form onSubmit={(e) => {
              e.preventDefault();
              const key = e.target.elements.apikey.value.trim();
              if (key) {
                localStorage.setItem('gemini_api_key', key);
                window.dispatchEvent(new Event('storage'));
                e.target.reset();
              }
            }}>
              <input 
                name="apikey"
                type="password" 
                placeholder="Dán Gemini API key (AIza...)" 
                style={{ 
                  width: '100%', 
                  padding: '12px 16px', 
                  borderRadius: '8px', 
                  background: 'rgba(255,255,255,0.03)', 
                  border: '1px solid var(--border-color)',
                  color: 'white',
                  marginBottom: '16px',
                  fontSize: '14px'
                }} 
              />
              <div style={{ display: 'flex', gap: '12px' }}>
                <button type="submit" className="btn" style={{ background: '#38bdf8', color: '#000', fontWeight: '600', padding: '8px 24px', flex: 1, justifyContent: 'center' }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
                  Lưu
                </button>
                <button type="button" onClick={() => { localStorage.removeItem('gemini_api_key'); window.dispatchEvent(new Event('storage')); }} className="btn" style={{ background: 'rgba(0,0,0,0.3)', border: '1px solid var(--border-color)', padding: '8px 24px', flex: 1, justifyContent: 'center' }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                  Xoá key
                </button>
              </div>
            </form>
          </div>

          <div className="card" style={{ marginTop: '20px' }}>
            <h3 style={{ fontSize: '18px', marginBottom: '12px', display: 'flex', gap: '10px' }}>
              <span style={{color: '#38bdf8'}}>🧠</span> Phân tích chuyên sâu — để AI tự đọc dữ liệu và nêu cảnh báo
            </h3>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '0', lineHeight: '1.6' }}>
              Khác với Báo cáo Sáng (dựng từ mẫu có sẵn), phần này gửi <b>toàn bộ số liệu 18 phân hệ</b> cho Gemini và yêu cầu tự rút ra kết luận — nối các dấu hiệu nằm rải rác ở nhiều phân hệ thành một nhận định, việc mà bảng biểu rời rạc không làm được.
            </p>
          </div>
'''

# Find the end of Export Center div to insert this
# Searching for:
#           {/* Lời khuyên của chuyên gia */}
#           <div className="card" style={{ borderLeft: '4px solid var(--color-primary)' }}>

text = text.replace('          {/* Lời khuyên của chuyên gia */}', ai_card + '\n          {/* Lời khuyên của chuyên gia */}')

# Add a state hook to force re-render when local storage changes
hooks = '''  const [storageUpdate, setStorageUpdate] = useState(0);
  
  useEffect(() => {
    const handleStorage = () => setStorageUpdate(prev => prev + 1);
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);'''

text = text.replace('const [syncMessage, setSyncMessage] = useState(null);', 'const [syncMessage, setSyncMessage] = useState(null);\n' + hooks)

with open('frontend/src/components/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
