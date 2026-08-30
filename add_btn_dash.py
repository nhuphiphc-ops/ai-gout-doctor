import re
with open('frontend/src/components/Dashboard.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

dash_btn = '''            <button onClick={() => onNavigate('guide')} className="btn" style={{ background: 'linear-gradient(135deg, #2563eb 0%, #3b82f6 100%)', color: '#fff', width: '100%', justifyContent: 'center', marginTop: '16px', fontWeight: 'bold' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              Xem Cẩm nang Khắc phục
            </button>'''

text = text.replace('dấu hiệu nằm rải rác ở nhiều phân hệ thành một nhận định, việc mà bảng biểu rời rạc không làm được.\n            </p>', 'dấu hiệu nằm rải rác ở nhiều phân hệ thành một nhận định, việc mà bảng biểu rời rạc không làm được.\n            </p>\n' + dash_btn)

with open('frontend/src/components/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
