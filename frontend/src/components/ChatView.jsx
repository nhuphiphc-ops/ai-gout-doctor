import React, { useState, useEffect, useRef } from 'react';
import apiService from '../services/api';

function ChatView({ userProfile }) {
  const [messages, setMessages] = useState([
    { role: 'ai', content: "Chào anh, tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  const [showApiPrompt, setShowApiPrompt] = useState(!localStorage.getItem('gemini_api_key'));
  const endRef = useRef(null);
  const [speakingIdx, setSpeakingIdx] = useState(null);

  const speakText = (text, idx) => {
    if (!('speechSynthesis' in window)) return;
    
    window.speechSynthesis.cancel();
    if (speakingIdx === idx) {
      setSpeakingIdx(null);
      return;
    }
    
    const cleanText = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/#/g, '');
    const sentences = cleanText.match(/[^.!?]+[.!?]+/g) || [cleanText];
    let currentIdx = 0;
    
    setSpeakingIdx(idx);
    
    const speakNext = () => {
      if (currentIdx >= sentences.length) {
        setSpeakingIdx(null);
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
      
      utterance.onerror = () => setSpeakingIdx(null);
      
      window.speechSynthesis.speak(utterance);
    };
    
    speakNext();
  };

  const saveApiKey = (e) => {
    e.preventDefault();
    if (apiKey.trim()) {
      localStorage.setItem('gemini_api_key', apiKey.trim());
      setShowApiPrompt(false);
    }
  };

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMsgs = [...messages, { role: 'user', content: input }];
    setMessages(newMsgs);
    setInput('');
    setLoading(true);

    try {
      const res = await apiService.sendChatMessage(input, apiKey);
      setMessages([...newMsgs, { role: 'ai', content: res.response }]);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) {
         setShowApiPrompt(true);
         localStorage.removeItem('gemini_api_key');
      }
      setMessages([...newMsgs, { role: 'ai', content: 'Xin lỗi, hệ thống bị lỗi hoặc API Key không hợp lệ. Vui lòng kiểm tra lại.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] bg-transparent text-gray-100">
      <div className="bg-[#1e293b]/80 backdrop-blur-md border-white/10 p-4 shadow-sm z-10 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white">Bác sĩ AI của bạn</h1>
          <p className="text-xs text-green-500 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span> Đang trực tuyến
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => setShowApiPrompt(!showApiPrompt)} className="text-xs bg-white/10 px-3 py-1.5 rounded-full text-gray-300 font-medium hover:bg-gray-200">
            🔑 API Key
          </button>
          {userProfile?.avatar_url && (
            <img src={userProfile.avatar_url} alt="User" style={{ width: '20px', height: '20px' }} className="rounded-full border-2 border-green-500/30 object-cover" />
          )}
        </div>
      </div>

      {showApiPrompt && (
        <div className="bg-blue-900/40 p-4 border-b border-green-500/30 flex flex-col gap-2">
          <p className="text-sm text-blue-200 font-medium">Vui lòng nhập Google Gemini API Key để chat:</p>
          <form onSubmit={saveApiKey} className="flex gap-2">
            <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="AIzaSy..." className="flex-1 px-3 py-2 border border-green-500/50 rounded-lg text-sm focus:outline-none focus:border-green-400" />
            <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">Lưu Key</button>
          </form>
          <p className="text-xs text-blue-300 mt-1">Lưu ý: Key sẽ chỉ được lưu an toàn trên trình duyệt của bạn.</p>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] rounded-2xl p-3 shadow-sm ${msg.role === 'user' ? 'bg-green-600 text-white rounded-br-none' : 'bg-[#1e293b]/80 backdrop-blur-md border-white/10 border border-white/10 rounded-bl-none text-white'}`}>
              <div className="whitespace-pre-wrap text-[15px] leading-relaxed">
                {msg.content}
              </div>
              {msg.role === 'ai' && (
                <button 
                  onClick={() => speakText(msg.content, idx)}
                  className={`mt-2 p-1.5 rounded-full flex items-center justify-center gap-1 text-xs font-medium transition-colors ${speakingIdx === idx ? 'bg-green-900/50 text-green-300' : 'bg-white/10 hover:bg-gray-200 text-gray-300'}`}
                >
                  {speakingIdx === idx ? (
                    <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg> Đang đọc...</>
                  ) : (
                    <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg> Nghe AI đọc</>
                  )}
                </button>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-[#1e293b]/80 backdrop-blur-md border-white/10 border border-white/10 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center gap-2">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <div className="p-3 bg-[#1e293b]/80 backdrop-blur-md border-white/10 border-t border-white/10">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Hỏi AI về sức khỏe của bạn..."
            className="flex-1 bg-white/10 border-none rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={!input.trim() || loading}
            className="bg-green-600 text-white w-12 h-12 rounded-full flex items-center justify-center shadow-md disabled:bg-gray-500"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatView;
