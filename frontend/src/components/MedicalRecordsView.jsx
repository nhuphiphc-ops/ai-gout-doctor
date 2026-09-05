import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

function MedicalRecordsView() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [speakingId, setSpeakingId] = useState(null);
  
  const [formData, setFormData] = useState({
    checkup_date: new Date().toISOString().split('T')[0],
    uric_acid: '',
    fasting_glucose: '',
    cholesterol_total: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    weight: '',
    egfr: '',
    kidney_cyst_size: '',
    tsh: '',
    ft3: '',
    ft4: '',
    notes: ''
  });

  useEffect(() => {
    loadRecords();
    return () => {
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    }
  }, []);

  const loadRecords = async () => {
    try {
      const data = await apiService.getMedicalCheckups();
      setRecords(data);
    } catch (error) {
      console.error("Lỗi tải hồ sơ xét nghiệm", error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Clean up empty strings
      const payload = { ...formData };
      Object.keys(payload).forEach(key => {
        if (payload[key] === '') payload[key] = null;
      });
      
      await apiService.createMedicalCheckup(payload);
      setIsAdding(false);
      loadRecords();
    } catch (error) {
      console.error("Lỗi lưu hồ sơ", error);
      alert("Có lỗi xảy ra khi lưu!");
    }
  };
  
  const readRecord = (record) => {
    if (!('speechSynthesis' in window)) {
        alert("Trình duyệt không hỗ trợ đọc văn bản.");
        return;
    }
    
    window.speechSynthesis.cancel();
    if (speakingId === record.id) {
        setSpeakingId(null);
        return;
    }
    
    const dateStr = new Date(record.checkup_date).toLocaleDateString('vi-VN');
    let text = `Hồ sơ khám ngày ${dateStr}. `;
    if (record.uric_acid) text += `Axit Uric: ${record.uric_acid} miligam trên đê xi lít. `;
    if (record.fasting_glucose) text += `Đường huyết: ${record.fasting_glucose} mi li mon trên lít. `;
    if (record.cholesterol_total) text += `Cholesterol: ${record.cholesterol_total} mi li mon trên lít. `;
    if (record.blood_pressure_systolic) text += `Huyết áp: ${record.blood_pressure_systolic} trên ${record.blood_pressure_diastolic}. `;
    if (record.egfr) text += `Mức lọc cầu thận eGFR: ${record.egfr}. `;
    if (record.kidney_cyst_size) text += `Kích thước nang thận: ${record.kidney_cyst_size}. `;
    if (record.notes) text += `Ghi chú chuyên khoa: ${record.notes}.`;
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'vi-VN';
    utterance.rate = 1.1;
    
    const voices = window.speechSynthesis.getVoices();
    const viVoice = voices.find(v => v.lang.includes('vi') || v.lang.includes('VI'));
    if (viVoice) utterance.voice = viVoice;
    
    utterance.onend = () => setSpeakingId(null);
    utterance.onerror = () => setSpeakingId(null);
    
    setSpeakingId(record.id);
    window.speechSynthesis.speak(utterance);
  };

  if (loading) return <div className="p-8 text-center text-gray-400">Đang tải dữ liệu...</div>;

  return (
    <div className="p-4 bg-transparent text-gray-100 min-h-[calc(100vh-80px)] overflow-y-auto pb-20">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white">Hồ sơ Sinh hóa & Hình ảnh</h2>
        <button 
          onClick={() => setIsAdding(!isAdding)}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-full text-sm font-semibold shadow-sm transition-colors"
        >
          {isAdding ? 'Hủy' : '+ Thêm kết quả'}
        </button>
      </div>

      {isAdding && (
        <div className="bg-[#1e293b]/80 backdrop-blur-md border-white/10 rounded-2xl p-5 mb-6 shadow-md border border-green-500/30 animate-fade-in">
          <h3 className="font-bold text-white mb-4 border-b pb-2">Nhập kết quả xét nghiệm / Siêu âm mới</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Ngày khám</label>
              <input type="date" name="checkup_date" value={formData.checkup_date} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" required />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Axit Uric (mg/dL)</label>
                <input type="number" step="0.01" name="uric_acid" value={formData.uric_acid} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="vd: 7.2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Glucose (mmol/L)</label>
                <input type="number" step="0.01" name="fasting_glucose" value={formData.fasting_glucose} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="vd: 5.5" />
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Cholesterol (mmol/L)</label>
                <input type="number" step="0.01" name="cholesterol_total" value={formData.cholesterol_total} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="vd: 5.2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">eGFR (Độ lọc thận)</label>
                <input type="number" step="0.1" name="egfr" value={formData.egfr} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="vd: 90" />
              </div>
            </div>
            
            <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">Kích thước nang thận (mm)</label>
                <input type="text" name="kidney_cyst_size" value={formData.kidney_cyst_size} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="vd: 11.7 x 10" />
            </div>
            
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-300 mb-1">TSH</label>
                <input type="number" step="0.01" name="tsh" value={formData.tsh} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="TSH" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-300 mb-1">FT3</label>
                <input type="number" step="0.01" name="ft3" value={formData.ft3} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="FT3" />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-300 mb-1">FT4</label>
                <input type="number" step="0.01" name="ft4" value={formData.ft4} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="FT4" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">HA tâm thu</label>
                <input type="number" name="blood_pressure_systolic" value={formData.blood_pressure_systolic} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="120" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">HA tâm trương</label>
                <input type="number" name="blood_pressure_diastolic" value={formData.blood_pressure_diastolic} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl" placeholder="80" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">Ghi chú chuyên khoa / Siêu âm</label>
              <textarea name="notes" value={formData.notes} onChange={handleInputChange} className="w-full p-3 bg-transparent text-gray-100 border border-white/20 rounded-xl h-24" placeholder="Nhập kết luận siêu âm..."></textarea>
            </div>

            <button type="submit" className="w-full bg-green-600 text-white font-bold py-3 rounded-xl shadow-md">
              Lưu kết quả khám
            </button>
          </form>
        </div>
      )}

      <div className="space-y-4">
        {records.length === 0 ? (
          <div className="text-center p-8 bg-[#1e293b]/80 backdrop-blur-md border-white/10 rounded-2xl border border-white/10">
            <p className="text-gray-400">Chưa có hồ sơ y tế nào.</p>
          </div>
        ) : (
          records.map((record) => (
            <div key={record.id} className="bg-[#1e293b]/80 backdrop-blur-md border-white/10 rounded-2xl p-5 shadow-sm border border-white/10 relative">
              <button 
                onClick={() => readRecord(record)}
                className={`absolute top-4 right-4 p-2 rounded-full ${speakingId === record.id ? 'bg-blue-900/50 text-blue-300' : 'bg-white/10 text-gray-400'}`}
              >
                {speakingId === record.id ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
                )}
              </button>
              
              <div className="font-bold text-lg text-blue-300 mb-3 border-b pb-2 pr-10">
                Ngày {new Date(record.checkup_date).toLocaleDateString('vi-VN')}
              </div>
              <div className="grid grid-cols-2 gap-y-3 gap-x-4 text-sm">
                {record.uric_acid && (
                  <div><span className="text-gray-400 block">Axit Uric</span><span className="font-semibold text-red-600">{record.uric_acid} mg/dL</span></div>
                )}
                {record.fasting_glucose && (
                  <div><span className="text-gray-400 block">Đường huyết</span><span className="font-semibold">{record.fasting_glucose} mmol/L</span></div>
                )}
                {record.cholesterol_total && (
                  <div><span className="text-gray-400 block">Cholesterol</span><span className="font-semibold">{record.cholesterol_total} mmol/L</span></div>
                )}
                {record.blood_pressure_systolic && (
                  <div><span className="text-gray-400 block">Huyết áp</span><span className="font-semibold">{record.blood_pressure_systolic}/{record.blood_pressure_diastolic}</span></div>
                )}
                {record.egfr && (
                  <div><span className="text-gray-400 block">Độ lọc thận eGFR</span><span className="font-semibold text-green-600">{record.egfr}</span></div>
                )}
                {record.kidney_cyst_size && (
                  <div><span className="text-gray-400 block">Nang thận</span><span className="font-semibold">{record.kidney_cyst_size}</span></div>
                )}
              </div>
              
              {(record.tsh || record.ft3 || record.ft4) && (
                <div className="mt-3 pt-3 border-t border-white/5 grid grid-cols-3 gap-2 text-xs">
                  {record.tsh && <div><span className="text-gray-400 block">TSH</span><span className="font-medium">{record.tsh}</span></div>}
                  {record.ft3 && <div><span className="text-gray-400 block">FT3</span><span className="font-medium">{record.ft3}</span></div>}
                  {record.ft4 && <div><span className="text-gray-400 block">FT4</span><span className="font-medium">{record.ft4}</span></div>}
                </div>
              )}
              
              {record.notes && (
                <div className="mt-3 pt-3 border-t border-white/10 bg-transparent text-gray-100 p-3 rounded-lg">
                  <span className="text-gray-400 block text-xs font-bold mb-1 uppercase">Kết luận siêu âm / Chuyên khoa:</span>
                  <p className="text-sm text-white whitespace-pre-wrap">{record.notes}</p>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default MedicalRecordsView;
