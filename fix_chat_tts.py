import re

with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

hooks = '''  const [speakingIdx, setSpeakingIdx] = useState(null);

  const speakText = (text, idx) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      if (speakingIdx === idx) {
        setSpeakingIdx(null);
        return;
      }
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'vi-VN'; // Vietnamese language
      utterance.rate = 1.1; // Slightly faster for Samsung
      
      // Try to find a Vietnamese or Google voice if available
      const voices = window.speechSynthesis.getVoices();
      const viVoice = voices.find(v => v.lang.includes('vi') || v.lang.includes('VI'));
      if (viVoice) utterance.voice = viVoice;

      utterance.onend = () => setSpeakingIdx(null);
      utterance.onerror = () => setSpeakingIdx(null);
      
      setSpeakingIdx(idx);
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Trình duyệt của bạn không hỗ trợ tính năng đọc văn bản.");
    }
  };'''

text = text.replace('  const endRef = useRef(null);', '  const endRef = useRef(null);\n' + hooks)

# Now modify the message rendering to add a speaker icon
render_msg = '''              <div className="whitespace-pre-wrap text-[15px] leading-relaxed">
                {msg.content}
              </div>
              {msg.role === 'ai' && (
                <button 
                  onClick={() => speakText(msg.content, idx)}
                  className={mt-2 p-1.5 rounded-full flex items-center justify-center gap-1 text-xs font-medium transition-colors }
                >
                  {speakingIdx === idx ? (
                    <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg> Đang đọc...</>
                  ) : (
                    <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg> Nghe AI đọc</>
                  )}
                </button>
              )}'''

text = text.replace('''              <div className="whitespace-pre-wrap text-[15px] leading-relaxed">
                {msg.content}
              </div>''', render_msg)

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
