import re

with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

new_speak = '''  const speakText = (text, idx) => {
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
  };'''

text = re.sub(r'  const speakText = \(text, idx\) => \{.*?  \};', new_speak, text, flags=re.DOTALL)

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
