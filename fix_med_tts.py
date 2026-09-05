import re

with open('frontend/src/components/MedicalRecordsView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

new_speak = '''  const speakText = (record) => {
    if (!('speechSynthesis' in window)) return;
    
    window.speechSynthesis.cancel();
    if (speakingId === record.id) {
        setSpeakingId(null);
        return;
    }
    
    const dateStr = new Date(record.checkup_date).toLocaleDateString('vi-VN');
    let textStr = Hồ sơ khám ngày . ;
    if (record.uric_acid) textStr += Axit Uric:  miligam trên đê xi lít. ;
    if (record.fasting_glucose) textStr += Đường huyết:  mi li mon trên lít. ;
    if (record.cholesterol_total) textStr += Cholesterol:  mi li mon trên lít. ;
    if (record.blood_pressure_systolic) textStr += Huyết áp:  trên . ;
    if (record.egfr) textStr += Mức lọc cầu thận: . ;
    if (record.kidney_cyst_size) textStr += Kích thước nang thận: . ;
    if (record.notes) textStr += Ghi chú chuyên khoa: .;
    
    const sentences = textStr.match(/[^.!?]+[.!?]+/g) || [textStr];
    let currentIdx = 0;
    
    setSpeakingId(record.id);
    
    const speakNext = () => {
      if (currentIdx >= sentences.length) {
        setSpeakingId(null);
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
      
      utterance.onerror = () => setSpeakingId(null);
      
      window.speechSynthesis.speak(utterance);
    };
    
    speakNext();
  };'''

text = re.sub(r'  const speakText = \(record\) => \{.*?  \};', new_speak, text, flags=re.DOTALL)

with open('frontend/src/components/MedicalRecordsView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
