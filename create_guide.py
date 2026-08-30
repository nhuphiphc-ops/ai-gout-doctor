import re

code = '''import React, { useState, useEffect } from 'react';
import apiService from '../services/api';

function RecoveryGuideView() {
  const [guide, setGuide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [speaking, setSpeaking] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGuide();
    return () => {
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    }
  }, []);

  const fetchGuide = async () => {
    try {
      const apiKey = localStorage.getItem('gemini_api_key') || '';
      const prompt = "Hãy đóng vai một chuyên gia y tế. Kiểm tra toàn bộ hồ sơ y tế (xét nghiệm, siêu âm) của tôi. Phân tích CHỈ những chỉ số đang vượt ngưỡng hoặc bất thường (ví dụ axit uric, eGFR, nang thận, TSH...). Viết thành một TÀI LIỆU KHẮC PHỤC BỆNH ngắn gọn, chia làm 2 phần: 1. Chỉ số cảnh báo, 2. Hành động cần làm ngay. Viết ngắn gọn, súc tích để tôi dễ nghe trên điện thoại.";
      const res = await apiService.sendChatMessage(prompt, apiKey);
      setGuide(res.response);
    } catch (err) {
      setError("Không thể tải tài liệu. Vui lòng kiểm tra lại API Key hoặc mạng.");
    } finally {
      setLoading(false);
    }
  };

  const speakText = () => {
    if (!('speechSynthesis' in window)) {
      alert("Trình duyệt không hỗ trợ đọc văn bản.");
      return;
    }
    window.speechSynthesis.cancel();
    if (speaking) {
      setSpeaking(false);
      return;
    }
    
    // Clean markdown before speaking
    const cleanText = guide.replace(/\\*\\*/g, '').replace(/\\*/g, '').replace(/#/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'vi-VN';
    utterance.rate = 1.1;
    
    const voices = window.speechSynthesis.getVoices();
    const viVoice = voices.find(v => v.lang.includes('vi') || v.lang.includes('VI'));
    if (viVoice) utterance.voice = viVoice;
    
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    
    setSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] bg-[#0b0f19] text-gray-100 p-4 overflow-y-auto">
      <div className="bg-[#1e293b]/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-white/10 mb-6 mt-4">
        <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span className="text-blue-400">🧠</span> Tài Liệu Khắc Phục Bệnh
        </h2>
        <p className="text-sm text-gray-400 mb-6">Tài liệu phân tích chuyên sâu các chỉ số vượt ngưỡng của bạn do AI tổng hợp.</p>
        
        {loading ? (
          <div className="flex flex-col items-center justify-center py-10 space-y-4">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-gray-400 font-medium animate-pulse">AI đang phân tích số liệu...</p>
          </div>
        ) : error ? (
          <div className="text-red-400 bg-red-900/30 p-4 rounded-xl border border-red-500/30">
            {error}
            <button onClick={fetchGuide} className="block mt-4 bg-red-500 text-white px-4 py-2 rounded-lg text-sm">Thử lại</button>
          </div>
        ) : (
          <div className="animate-fade-in">
            <button 
              onClick={speakText}
              className={w-full py-4 rounded-xl font-bold flex items-center justify-center gap-3 mb-6 transition-all shadow-lg \}
            >
              {speaking ? (
                <><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg> TẠM DỪNG ĐỌC</>
              ) : (
                <><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg> 🔊 NGHE AI ĐỌC TÀI LIỆU</>
              )}
            </button>
            
            <div className="whitespace-pre-wrap leading-relaxed text-[15px] text-gray-200 p-5 bg-white/5 rounded-xl border border-white/5 font-sans">
              {guide}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RecoveryGuideView;
'''

with open('frontend/src/components/RecoveryGuideView.jsx', 'w', encoding='utf-8') as f:
    f.write(code)

# Add to App.jsx
with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app_text = f.read()

if 'import RecoveryGuideView from' not in app_text:
    app_text = app_text.replace("import ChatView from './components/ChatView';", "import ChatView from './components/ChatView';\nimport RecoveryGuideView from './components/RecoveryGuideView';")

if 'currentView === \\'guide\\'' not in app_text:
    guide_block = '''          {currentView === 'guide' && (
            <RecoveryGuideView />
          )}'''
    app_text = app_text.replace("          {currentView === 'chat' && (", guide_block + "\n          {currentView === 'chat' && (")

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app_text)

# Add button to Dashboard.jsx
with open('frontend/src/components/Dashboard.jsx', 'r', encoding='utf-8') as f:
    dash_text = f.read()

dash_btn = '''            <button onClick={() => onNavigate('guide')} className="btn" style={{ background: 'linear-gradient(135deg, #2563eb 0%, #3b82f6 100%)', color: '#fff', width: '100%', justifyContent: 'center', marginTop: '16px', fontWeight: 'bold' }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
              Xem Cẩm nang Khắc phục
            </button>'''

dash_text = dash_text.replace('các dấu hiệu nằm rải rác ở nhiều phân hệ thành một nhận định, việc mà bảng biểu rời rạc không làm được.\n            </p>', 'các dấu hiệu nằm rải rác ở nhiều phân hệ thành một nhận định, việc mà bảng biểu rời rạc không làm được.\n            </p>\n' + dash_btn)

with open('frontend/src/components/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(dash_text)
