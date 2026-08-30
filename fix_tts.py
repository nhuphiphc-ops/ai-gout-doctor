import re

with open('frontend/src/components/RecoveryGuideView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

new_speak_text = '''  const speakText = () => {
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
  };'''

text = re.sub(r'  const speakText = \(\) => \{.*?(?=  return \()', new_speak_text + '\n\n', text, flags=re.DOTALL)

with open('frontend/src/components/RecoveryGuideView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
