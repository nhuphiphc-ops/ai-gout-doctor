import React, { useState, useEffect } from 'react';
import { 
  HeartPulse, 
  Home, 
  TrendingUp, 
  Compass, 
  Calendar, 
  User, 
  LogOut, 
  Sun, 
  Moon, 
  Menu, 
  X,
  FileSpreadsheet
} from 'lucide-react';

import apiService from './services/api';
import Dashboard from './components/Dashboard';
import MorningForm from './components/MorningForm';
import AfternoonForm from './components/AfternoonForm';
import ChartsView from './components/ChartsView';
import CorrelationReport from './components/CorrelationReport';
import HistoryTable from './components/HistoryTable';
import ProfileView from './components/ProfileView';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  // Dashboard & History data states
  const [dashboardData, setDashboardData] = useState(null);
  const [historyLogs, setHistoryLogs] = useState([]);
  const [chartView, setChartView] = useState('week'); // week, month, year
  const [loading, setLoading] = useState(true);

  // Auto login or fetch current session
  useEffect(() => {
    const initSession = async () => {
      let user = apiService.getCurrentUser();
      if (!user) {
        // Automatically perform mock login for frictionless local PC/phone experience
        try {
          const res = await apiService.loginMock();
          user = res.user;
        } catch (err) {
          console.error('Failed to perform local mock login:', err);
        }
      }
      
      // Fetch fresh profile from backend DB to sync state (e.g. Google Fit connection status)
      if (user) {
        try {
          const freshProfile = await apiService.getProfile();
          user = freshProfile;
          localStorage.setItem('user', JSON.stringify(freshProfile));
        } catch (err) {
          console.error('Failed to fetch fresh user profile:', err);
        }
      }
      
      setCurrentUser(user);
      setLoading(false);

      // Clean up google_fit success parameters from URL
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('google_fit') === 'success') {
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    };
    initSession();
  }, []);

  // Fetch data whenever user session is ready or view changes
  const loadData = async () => {
    if (!currentUser) return;
    try {
      const dbData = await apiService.getDashboardData(chartView);
      setDashboardData(dbData);
      
      const logs = await apiService.getHistoryLogs(100);
      setHistoryLogs(logs);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  useEffect(() => {
    if (currentUser) {
      loadData();
    }
  }, [currentUser, chartView, currentView]);

  const handleLogout = () => {
    apiService.logout();
    setCurrentUser(null);
    setCurrentView('dashboard');
  };

  const handleExport = (format) => {
    const url = apiService.getExportUrl(format);
    window.open(url, '_blank');
  };

  const handleSaveLog = (updatedLog) => {
    // Refresh dashboard data
    loadData();
    setCurrentView('dashboard');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-primary)', color: 'var(--text-secondary)' }}>
        Đang khởi động Bác sĩ gia đình AI...
      </div>
    );
  }

  return (
    <div className="app-wrapper">
      
      {/* Navbar Header */}
      <nav className="navbar">
        <div className="container navbar-inner">
          <div className="brand" style={{ cursor: 'pointer' }} onClick={() => setCurrentView('dashboard')}>
            <HeartPulse size={30} style={{ color: 'var(--color-primary)' }} />
            <span>AI Gout Doctor</span>
          </div>

          {/* Desktop Navigation Links */}
          <ul className="nav-links">
            <li>
              <button 
                className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
                onClick={() => setCurrentView('dashboard')}
              >
                Dashboard
              </button>
            </li>
            <li>
              <button 
                className={`nav-btn ${currentView === 'charts' ? 'active' : ''}`}
                onClick={() => setCurrentView('charts')}
              >
                Biểu đồ xu hướng
              </button>
            </li>
            <li>
              <button 
                className={`nav-btn ${currentView === 'correlation' ? 'active' : ''}`}
                onClick={() => setCurrentView('correlation')}
              >
                Mối tương quan thực phẩm
              </button>
            </li>
            <li>
              <button 
                className={`nav-btn ${currentView === 'history' ? 'active' : ''}`}
                onClick={() => setCurrentView('history')}
              >
                Nhật ký cũ
              </button>
            </li>
            <li>
              <button 
                className={`nav-btn ${currentView === 'profile' ? 'active' : ''}`}
                onClick={() => setCurrentView('profile')}
              >
                Cá nhân
              </button>
            </li>
          </ul>

          {/* Desktop Right Side: User profile widget & logout */}
          {currentUser && (
            <div className="user-profile-widget" style={{ display: 'flex' }}>
              <div className="user-avatar">
                {currentUser.avatar_url ? (
                  <img src={currentUser.avatar_url} alt="Avatar" />
                ) : (
                  currentUser.name ? currentUser.name.charAt(0) : 'P'
                )}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '2px' }}>
                <span style={{ fontSize: '15px', fontWeight: '600' }}>{currentUser.name || 'Anh Phi'}</span>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>47 tuổi / Gout 11 năm</span>
              </div>
              <button 
                onClick={handleLogout} 
                title="Đăng xuất"
                style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', marginLeft: '12px' }}
              >
                <LogOut size={18} />
              </button>
            </div>
          )}

          {/* Mobile hamburger button */}
          <button 
            className="mobile-toggle"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </nav>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="mobile-menu-overlay" onClick={() => setMobileMenuOpen(false)}>
          <div className="mobile-menu-drawer" onClick={(e) => e.stopPropagation()}>
            <div className="mobile-menu-header">
              <div className="brand" style={{ cursor: 'pointer' }} onClick={() => { setCurrentView('dashboard'); setMobileMenuOpen(false); }}>
                <HeartPulse size={28} style={{ color: 'var(--color-primary)' }} />
                <span>AI Gout Doctor</span>
              </div>
              <button className="mobile-menu-close" onClick={() => setMobileMenuOpen(false)}>
                <X size={24} />
              </button>
            </div>
            
            {currentUser && (
              <div className="mobile-user-widget">
                <div className="user-avatar">
                  {currentUser.avatar_url ? (
                    <img src={currentUser.avatar_url} alt="Avatar" />
                  ) : (
                    currentUser.name ? currentUser.name.charAt(0) : 'P'
                  )}
                </div>
                <div>
                  <div style={{ fontWeight: '600' }}>{currentUser.name || 'Anh Phi'}</div>
                  <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>47 tuổi / Gout 11 năm</div>
                </div>
              </div>
            )}

            <ul className="mobile-nav-links">
              <li>
                <button 
                  className={`mobile-nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
                  onClick={() => { setCurrentView('dashboard'); setMobileMenuOpen(false); }}
                >
                  Dashboard
                </button>
              </li>
              <li>
                <button 
                  className={`mobile-nav-btn ${currentView === 'charts' ? 'active' : ''}`}
                  onClick={() => { setCurrentView('charts'); setMobileMenuOpen(false); }}
                >
                  Biểu đồ xu hướng
                </button>
              </li>
              <li>
                <button 
                  className={`mobile-nav-btn ${currentView === 'correlation' ? 'active' : ''}`}
                  onClick={() => { setCurrentView('correlation'); setMobileMenuOpen(false); }}
                >
                  Mối tương quan thực phẩm
                </button>
              </li>
              <li>
                <button 
                  className={`mobile-nav-btn ${currentView === 'history' ? 'active' : ''}`}
                  onClick={() => { setCurrentView('history'); setMobileMenuOpen(false); }}
                >
                  Nhật ký cũ
                </button>
              </li>
              <li>
                <button 
                  className={`mobile-nav-btn ${currentView === 'profile' ? 'active' : ''}`}
                  onClick={() => { setCurrentView('profile'); setMobileMenuOpen(false); }}
                >
                  Cá nhân
                </button>
              </li>
              {currentUser && (
                <li style={{ marginTop: 'auto', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
                  <button 
                    className="mobile-nav-btn" 
                    onClick={() => { handleLogout(); setMobileMenuOpen(false); }}
                    style={{ color: 'var(--color-danger)', display: 'flex', alignItems: 'center', gap: '8px', background: 'transparent', border: 'none', width: '100%', padding: '12px 16px', fontWeight: '500' }}
                  >
                    <LogOut size={18} />
                    <span>Đăng xuất</span>
                  </button>
                </li>
              )}
            </ul>
          </div>
        </div>
      )}

      {/* Render Main Content */}
      <main className="main-content container">
        {currentView === 'dashboard' && (
          <Dashboard 
            data={dashboardData} 
            currentUser={currentUser}
            onNavigate={(view) => setCurrentView(view)} 
            onExport={handleExport}
            onRefresh={loadData}
          />
        )}
        
        {currentView === 'morning' && (
          <MorningForm 
            todayLog={dashboardData?.today_log} 
            onSave={handleSaveLog}
            onCancel={() => setCurrentView('dashboard')}
          />
        )}

        {currentView === 'afternoon' && (
          <AfternoonForm 
            todayLog={dashboardData?.today_log} 
            onSave={handleSaveLog}
            onCancel={() => setCurrentView('dashboard')}
          />
        )}

        {currentView === 'charts' && (
          <ChartsView 
            trendsData={dashboardData?.trends || []}
            activeView={chartView}
            onViewChange={(view) => setChartView(view)}
          />
        )}

        {currentView === 'correlation' && (
          <CorrelationReport />
        )}

        {currentView === 'history' && (
          <HistoryTable logs={historyLogs} />
        )}

        {currentView === 'profile' && (
          <ProfileView onProfileUpdate={(user) => setCurrentUser(user)} />
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <p style={{ marginBottom: '8px' }}>
            Hệ thống Quản lý sức khỏe cá nhân & Cảnh báo tái phát Gout cấp nội bộ v1.0.0
          </p>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
            ⚠️ Tuyên bố: Mọi thông tin tư vấn và cảnh báo được đề xuất bởi thuật toán học máy / luật AI mang tính chất tham khảo. Không thay thế các chỉ định điều trị và chẩn đoán của Bác sĩ chuyên khoa cơ xương khớp.
          </p>
        </div>
      </footer>
      {/* Bottom Navigation Bar for Mobile */}
      <div className="mobile-bottom-nav">
        <button 
          className={`mobile-bottom-nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentView('dashboard')}
        >
          <Home size={20} />
          <span>Trang chủ</span>
        </button>
        <button 
          className={`mobile-bottom-nav-btn ${currentView === 'charts' ? 'active' : ''}`}
          onClick={() => setCurrentView('charts')}
        >
          <TrendingUp size={20} />
          <span>Biểu đồ</span>
        </button>
        <button 
          className={`mobile-bottom-nav-btn ${currentView === 'correlation' ? 'active' : ''}`}
          onClick={() => setCurrentView('correlation')}
        >
          <Compass size={20} />
          <span>Tương quan</span>
        </button>
        <button 
          className={`mobile-bottom-nav-btn ${currentView === 'history' ? 'active' : ''}`}
          onClick={() => setCurrentView('history')}
        >
          <Calendar size={20} />
          <span>Nhật ký</span>
        </button>
        <button 
          className={`mobile-bottom-nav-btn ${currentView === 'profile' ? 'active' : ''}`}
          onClick={() => setCurrentView('profile')}
        >
          <User size={20} />
          <span>Cá nhân</span>
        </button>
      </div>
    </div>
  );
}
