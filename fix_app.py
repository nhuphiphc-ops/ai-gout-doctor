import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Desktop nav
text = re.sub(r'className=\{\\\n?av-btn \\\\\}', r'className={
av-btn }', text) # placeholder logic

# The easiest way is to just replace the whole nav-links block
desktop_nav_bad = '''          <ul className="nav-links">
            <li>
              <button className={\\
av-btn \\\\} onClick={() => setCurrentView('chat')}>
                Tư vấn AI
              </button>
            </li>
            <li>
              <button className={\\
av-btn \\\\} onClick={() => setCurrentView('medical')}>
                Hồ sơ y tế
              </button>
            </li>
            <li>
              <button className={\\
av-btn \\\\} onClick={() => setCurrentView('dashboard')}>
                Nhật ký
              </button>
            </li>
            <li>
              <button className={\\
av-btn \\\\} onClick={() => setCurrentView('charts')}>
                Biểu đồ
              </button>
            </li>
            <li>
              <button className={\\
av-btn \\\\} onClick={() => setCurrentView('profile')}>
                Cá nhân
              </button>
            </li>
          </ul>'''

desktop_nav_good = '''          <ul className="nav-links">
            <li><button className={
av-btn } onClick={() => setCurrentView('chat')}>Tư vấn AI</button></li>
            <li><button className={
av-btn } onClick={() => setCurrentView('medical')}>Hồ sơ y tế</button></li>
            <li><button className={
av-btn } onClick={() => setCurrentView('dashboard')}>Nhật ký</button></li>
            <li><button className={
av-btn } onClick={() => setCurrentView('charts')}>Biểu đồ</button></li>
            <li><button className={
av-btn } onClick={() => setCurrentView('profile')}>Cá nhân</button></li>
          </ul>'''
          
text = text.replace(desktop_nav_bad, desktop_nav_good)

mobile_nav_bad = '''            <ul className="mobile-nav-links">
              <li>
                <button className={\\mobile-nav-btn \\\\} onClick={() => { setCurrentView('chat'); setMobileMenuOpen(false); }}>
                  Tư vấn AI
                </button>
              </li>
              <li>
                <button className={\\mobile-nav-btn \\\\} onClick={() => { setCurrentView('medical'); setMobileMenuOpen(false); }}>
                  Hồ sơ y tế
                </button>
              </li>
              <li>
                <button className={\\mobile-nav-btn \\\\} onClick={() => { setCurrentView('dashboard'); setMobileMenuOpen(false); }}>
                  Nhật ký sinh hoạt
                </button>
              </li>
              <li>
                <button className={\\mobile-nav-btn \\\\} onClick={() => { setCurrentView('charts'); setMobileMenuOpen(false); }}>
                  Biểu đồ
                </button>
              </li>
              <li>
                <button className={\\mobile-nav-btn \\\\} onClick={() => { setCurrentView('profile'); setMobileMenuOpen(false); }}>
                  Cá nhân
                </button>
              </li>
            </ul>'''

mobile_nav_good = '''            <ul className="mobile-nav-links">
              <li><button className={mobile-nav-btn } onClick={() => { setCurrentView('chat'); setMobileMenuOpen(false); }}>Tư vấn AI</button></li>
              <li><button className={mobile-nav-btn } onClick={() => { setCurrentView('medical'); setMobileMenuOpen(false); }}>Hồ sơ y tế</button></li>
              <li><button className={mobile-nav-btn } onClick={() => { setCurrentView('dashboard'); setMobileMenuOpen(false); }}>Nhật ký</button></li>
              <li><button className={mobile-nav-btn } onClick={() => { setCurrentView('charts'); setMobileMenuOpen(false); }}>Biểu đồ</button></li>
              <li><button className={mobile-nav-btn } onClick={() => { setCurrentView('profile'); setMobileMenuOpen(false); }}>Cá nhân</button></li>
            </ul>'''

text = text.replace(mobile_nav_bad, mobile_nav_good)

main_content_bad = "      <main className={\\main-content \\\\}>"
main_content_good = "      <main className={main-content }>"
text = text.replace(main_content_bad, main_content_good)

mobile_bottom_bad = '''      <div className="mobile-bottom-nav">
        <button className={\\mobile-bottom-nav-btn \\\\} onClick={() => setCurrentView('chat')}>
          <MessageCircle size={20} />
          <span>Tư vấn</span>
        </button>
        <button className={\\mobile-bottom-nav-btn \\\\} onClick={() => setCurrentView('medical')}>
          <FileText size={20} />
          <span>Hồ sơ</span>
        </button>
        <button className={\\mobile-bottom-nav-btn \\\\} onClick={() => setCurrentView('dashboard')}>
          <Home size={20} />
          <span>Nhật ký</span>
        </button>
        <button className={\\mobile-bottom-nav-btn \\\\} onClick={() => setCurrentView('charts')}>
          <TrendingUp size={20} />
          <span>Biểu đồ</span>
        </button>
        <button className={\\mobile-bottom-nav-btn \\\\} onClick={() => setCurrentView('profile')}>
          <User size={20} />
          <span>Cá nhân</span>
        </button>
      </div>'''

mobile_bottom_good = '''      <div className="mobile-bottom-nav">
        <button className={mobile-bottom-nav-btn } onClick={() => setCurrentView('chat')}><MessageCircle size={20} /><span>Tư vấn</span></button>
        <button className={mobile-bottom-nav-btn } onClick={() => setCurrentView('medical')}><FileText size={20} /><span>Hồ sơ</span></button>
        <button className={mobile-bottom-nav-btn } onClick={() => setCurrentView('dashboard')}><Home size={20} /><span>Nhật ký</span></button>
        <button className={mobile-bottom-nav-btn } onClick={() => setCurrentView('charts')}><TrendingUp size={20} /><span>Biểu đồ</span></button>
        <button className={mobile-bottom-nav-btn } onClick={() => setCurrentView('profile')}><User size={20} /><span>Cá nhân</span></button>
      </div>'''
      
text = text.replace(mobile_bottom_bad, mobile_bottom_good)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
