import React, { useState, useEffect } from 'react';
import { 
  HeartPulse, 
  Home, 
  TrendingUp, 
  User, 
  LogOut, 
  Menu, 
  X,
  MessageCircle,
  FileText
} from 'lucide-react';

import apiService from './services/api';
import Dashboard from './components/Dashboard';
import MorningForm from './components/MorningForm';
import AfternoonForm from './components/AfternoonForm';
import ChartsView from './components/ChartsView';
import ProfileView from './components/ProfileView';
import ChatView from './components/ChatView';
import MedicalRecordsView from './components/MedicalRecordsView';

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [currentView, setCurrentView] = useState('chat');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  // Dashboard & History data states
  const [dashboardData, setDashboardData] = useState(null);
  const [chartView, setChartView] = useState('week'); // week, month, year
  const [loading, setLoading] = useState(true);

  // Auto login or fetch current session
  useEffect(() => {
    const initSession = async () => {
      let user = apiService.getCurrentUser();
      if (!user) {
        try {
          const res = await apiService.loginMock();
          user = res.user;
        } catch (err) {
          console.error('Failed to perform local mock login:', err);
        }
      }
      
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
    };
    initSession();
  }, []);

  const loadData = async () => {
    if (!currentUser) return;
    try {
      const dbData = await apiService.getDashboardData(chartView);
      setDashboardData(dbData);
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
    setCurrentView('chat');
  };

  const handleSaveLog = (updatedLog) => {
    loadData();
    setCurrentView('dashboard');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: 'var(--bg-primary)', color: 'var(--text-secondary)' }}>
        Đang khởi động Trợ lý tư vấn AI...
      </div>
    );
  }

  return (
    <div className="app-wrapper">
      
      {/* Navbar Header */}
      <nav className="navbar">
        <div className="container navbar-inner">
          <div className="brand" style={{ cursor: 'pointer' }} onClick={() => setCurrentView('chat')}>
            <HeartPulse size={30} style={{ color: 'var(--color-primary)' }} />
            <span>AI Health Assistant</span>
          </div>

          {/* Desktop Navigation Links */}
          <ul className="nav-links">
            <li>
              <button className={`nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('chat')}>
                Tư vấn AI
              </button>
            </li>
            <li>
              <button className={`nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('medical')}>
                Hồ sơ y tế
              </button>
            </li>
            <li>
              <button className={`nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('dashboard')}>
                Nhật ký
              </button>
            </li>
            <li>
              <button className={`nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('charts')}>
                Biểu đồ
              </button>
            </li>
            <li>
              <button className={`nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('profile')}>
                Cá nhân
              </button>
            </li>
          </ul>

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
                <span style={{ fontSize: '15px', fontWeight: '600' }}>{currentUser.name || 'Bệnh nhân'}</span>
              </div>
              <button onClick={handleLogout} style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', marginLeft: '12px' }}>
                <LogOut size={18} />
              </button>
            </div>
          )}

          <button className="mobile-toggle" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </nav>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="mobile-menu-overlay" onClick={() => setMobileMenuOpen(false)}>
          <div className="mobile-menu-drawer" onClick={(e) => e.stopPropagation()}>
            <div className="mobile-menu-header">
              <div className="brand" onClick={() => { setCurrentView('chat'); setMobileMenuOpen(false); }}>
                <HeartPulse size={28} style={{ color: 'var(--color-primary)' }} />
                <span>AI Assistant</span>
              </div>
              <button className="mobile-menu-close" onClick={() => setMobileMenuOpen(false)}>
                <X size={24} />
              </button>
            </div>
            
            <ul className="mobile-nav-links">
              <li>
                <button className={`mobile-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => { setCurrentView('chat'); setMobileMenuOpen(false); }}>
                  Tư vấn AI
                </button>
              </li>
              <li>
                <button className={`mobile-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => { setCurrentView('medical'); setMobileMenuOpen(false); }}>
                  Hồ sơ y tế
                </button>
              </li>
              <li>
                <button className={`mobile-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => { setCurrentView('dashboard'); setMobileMenuOpen(false); }}>
                  Nhật ký sinh hoạt
                </button>
              </li>
              <li>
                <button className={`mobile-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => { setCurrentView('charts'); setMobileMenuOpen(false); }}>
                  Biểu đồ
                </button>
              </li>
              <li>
                <button className={`mobile-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => { setCurrentView('profile'); setMobileMenuOpen(false); }}>
                  Cá nhân
                </button>
              </li>
            </ul>
          </div>
        </div>
      )}

      {/* Render Main Content */}
      <main className={`main-content ${currentView === "chat" ? "" : "container"}`}>
        {currentView === 'chat' && (
          <ChatView userProfile={currentUser} />
        )}

        {currentView === 'medical' && (
          <MedicalRecordsView />
        )}

        {currentView === 'dashboard' && (
          <Dashboard 
            data={dashboardData} 
            currentUser={currentUser}
            onNavigate={(view) => setCurrentView(view)} 
            onExport={() => {}}
            onRefresh={loadData}
          />
        )}
        
        {currentView === 'morning' && (
          <MorningForm todayLog={dashboardData?.today_log} onSave={handleSaveLog} onCancel={() => setCurrentView('dashboard')} />
        )}

        {currentView === 'afternoon' && (
          <AfternoonForm todayLog={dashboardData?.today_log} onSave={handleSaveLog} onCancel={() => setCurrentView('dashboard')} />
        )}

        {currentView === 'charts' && (
          <ChartsView trendsData={dashboardData?.trends || []} activeView={chartView} onViewChange={(view) => setChartView(view)} />
        )}

        {currentView === 'profile' && (
          <ProfileView onProfileUpdate={(user) => setCurrentUser(user)} />
        )}
      </main>

      {/* Bottom Navigation Bar for Mobile */}
      <div className="mobile-bottom-nav">
        <button className={`mobile-bottom-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('chat')}>
          <MessageCircle size={20} />
          <span>Tư vấn</span>
        </button>
        <button className={`mobile-bottom-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('medical')}>
          <FileText size={20} />
          <span>Hồ sơ</span>
        </button>
        <button className={`mobile-bottom-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('dashboard')}>
          <Home size={20} />
          <span>Nhật ký</span>
        </button>
        <button className={`mobile-bottom-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('charts')}>
          <TrendingUp size={20} />
          <span>Biểu đồ</span>
        </button>
        <button className={`mobile-bottom-nav-btn ${currentView === "foo" ? "active" : ""}`} onClick={() => setCurrentView('profile')}>
          <User size={20} />
          <span>Cá nhân</span>
        </button>
      </div>
    </div>
  );
}
