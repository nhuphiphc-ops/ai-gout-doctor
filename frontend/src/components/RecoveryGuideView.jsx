import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

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
      const res = await apiService.sendChatMessage(prompt, []);
      setGuide(res.response);
    } catch (err) {
      setError("Không thể tải tài liệu. Vui lòng kiểm tra lại API Key hoặc mạng.");
    } finally {
      setLoading(false);
    }
  };

  const speakText = () => {
    if (!('speechSynthesis' in window)) {
      alert("Trình duyệt không hỗ trợ đọc văn bản. Vui lòng mở bằng Chrome hoặc Safari.");
      return;
    }
    
    window.speechSynthesis.cancel();
    if (speaking) {
      setSpeaking(false);
      return;
    }
    
    // Clean markdown before speaking
    const cleanText = guide.replace(/\*\*/g, '').replace(/\*/g, '').replace(/#/g, '');
    
    // Split into sentences for Android/Samsung compatibility (long text bug)
    const sentences = cleanText.match(/[^.!?]+[.!?]+/g) || [cleanText];
    let currentIdx = 0;
    
    setSpeaking(true);
    
    const speakNext = () => {
      if (currentIdx >= sentences.length) {
        setSpeaking(false);
        return;
      }
      
      const utterance = new SpeechSynthesisUtterance(sentences[currentIdx].trim());
      utterance.lang = 'vi-VN';
      utterance.rate = 1.0;
      
      const voices = window.speechSynthesis.getVoices();
      const viVoice = voices.find(v => v.lang.includes('vi') || v.lang.includes('VI'));
      if (viVoice) utterance.voice = viVoice;
      
      utterance.onend = () => {
        currentIdx++;
        speakNext();
      };
      
      utterance.onerror = (e) => {
        console.error("TTS Error:", e);
        // Fallback: just stop on error, sometimes Android throws error randomly
        setSpeaking(false);
      };
      
      window.speechSynthesis.speak(utterance);
    };
    
    speakNext();
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] bg-transparent text-gray-100 p-4 overflow-y-auto">
      <div className="bg-[#1e293b]/80 backdrop-blur-md rounded-2xl p-6 shadow-lg border border-white/10 mb-6 mt-4">
        <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
          <span className="text-green-400">🧠</span> Tài Liệu Khắc Phục
        </h2>
        <p className="text-sm text-gray-400 mb-6">Tài liệu phân tích chuyên sâu các chỉ số vượt ngưỡng của bạn do AI tổng hợp.</p>
        
        {loading ? (
          <div className="flex flex-col items-center justify-center py-10 space-y-4">
            <div className="w-8 h-8 border-4 border-green-500 border-t-transparent rounded-full animate-spin"></div>
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
              className={`w-full py-4 rounded-xl font-bold flex items-center justify-center gap-3 mb-6 transition-all shadow-lg ${speaking ? 'bg-green-600 text-white shadow-green-500/30' : 'bg-green-600 hover:bg-green-500 text-white shadow-blue-500/30'}`}
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
