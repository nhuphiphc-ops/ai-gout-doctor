import re
with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''  const [messages, setMessages] = useState([
    { role: 'ai', content: "Chào anh, tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiKey, setApiKey] = useState(localStorage.getItem('gemini_api_key') || '');
  const [showApiPrompt, setShowApiPrompt] = useState(!localStorage.getItem('gemini_api_key'));
  const endRef = useRef(null);

  const saveApiKey = (e) => {
    e.preventDefault();
    if (apiKey.trim()) {
      localStorage.setItem('gemini_api_key', apiKey.trim());
      setShowApiPrompt(false);
    }
  };'''

text = re.sub(r'  const \[messages, setMessages\].*?const endRef = useRef\(null\);', replacement, text, flags=re.DOTALL)

send_replace = '''    try {
      // Modify apiService to accept apiKey in header or body
      const res = await apiService.sendChatMessage(input, apiKey);
      setMessages([...newMsgs, { role: 'ai', content: res.response }]);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) {
         setShowApiPrompt(true);
         localStorage.removeItem('gemini_api_key');
      }
      setMessages([...newMsgs, { role: 'ai', content: 'Xin lỗi, hệ thống bị lỗi hoặc API Key không hợp lệ. Vui lòng kiểm tra lại.' }]);
    }'''

text = re.sub(r'    try \{.*?    \} catch \(err\) \{.*?    \}', send_replace, text, flags=re.DOTALL)

ui_replace = '''      <div className="bg-white p-4 shadow-sm z-10 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-800">Bác sĩ AI của bạn</h1>
          <p className="text-xs text-green-500 font-medium flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-green-500 inline-block"></span> Đang trực tuyến
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button onClick={() => setShowApiPrompt(!showApiPrompt)} className="text-xs bg-gray-100 px-3 py-1.5 rounded-full text-gray-600 font-medium hover:bg-gray-200">
            🔑 API Key
          </button>
          {userProfile?.avatar_url && (
            <img src={userProfile.avatar_url} alt="User" className="w-8 h-8 rounded-full border-2 border-blue-100 object-cover" />
          )}
        </div>
      </div>

      {showApiPrompt && (
        <div className="bg-blue-50 p-4 border-b border-blue-100 flex flex-col gap-2">
          <p className="text-sm text-blue-800 font-medium">Vui lòng nhập Google Gemini API Key để chat:</p>
          <form onSubmit={saveApiKey} className="flex gap-2">
            <input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="AIzaSy..." className="flex-1 px-3 py-2 border border-blue-200 rounded-lg text-sm focus:outline-none focus:border-blue-400" />
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">Lưu Key</button>
          </form>
          <p className="text-xs text-blue-600 mt-1">Lưu ý: Key sẽ chỉ được lưu an toàn trên trình duyệt của bạn.</p>
        </div>
      )}'''

text = re.sub(r'      <div className="bg-white p-4 shadow-sm z-10 flex items-center justify-between">.*?      </div>', ui_replace, text, flags=re.DOTALL)

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
