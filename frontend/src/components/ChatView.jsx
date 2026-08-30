import React, { useState, useRef, useEffect } from 'react';
import { apiService } from '../services/api';

function ChatView({ userProfile }) {
  const [messages, setMessages] = useState([
    { role: 'ai', content: Chào anh , tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không? }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input.trim() };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      // Send chat history (excluding the first greeting to save context, or send all)
      const data = await apiService.sendChatMessage(userMsg.content, messages.slice(1));
      setMessages([...newMessages, { role: 'ai', content: data.response }]);
    } catch (error) {
      setMessages([...newMessages, { role: 'ai', content: 'Xin lỗi, đã có lỗi kết nối tới máy chủ AI. Vui lòng thử lại sau.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-80px)] bg-gray-50">
      <div className="bg-white p-4 shadow-sm z-10 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">Bác sĩ AI của bạn</h1>
          <p className="text-xs text-green-500 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span> Đang trực tuyến
          </p>
        </div>
        {userProfile?.avatar_url && (
          <img src={userProfile.avatar_url} alt="User" className="w-10 h-10 rounded-full border-2 border-blue-100 object-cover" />
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={\lex \\}>
            <div className={\max-w-[85%] rounded-2xl p-3 shadow-sm \\}>
              <div className="whitespace-pre-wrap text-[15px] leading-relaxed">
                {msg.content}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-100 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center gap-2">
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
              <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 bg-white border-t border-gray-100">
        <form onSubmit={handleSend} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Hỏi AI về sức khỏe của bạn..."
            className="flex-1 bg-gray-100 border-none rounded-full px-5 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={!input.trim() || loading}
            className="bg-blue-600 text-white w-12 h-12 rounded-full flex items-center justify-center shadow-md disabled:bg-gray-300"
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
