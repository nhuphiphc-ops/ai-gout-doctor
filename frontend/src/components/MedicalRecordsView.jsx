import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

function MedicalRecordsView() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState({
    checkup_date: new Date().toISOString().split('T')[0],
    uric_acid: '',
    fasting_glucose: '',
    cholesterol_total: '',
    blood_pressure_systolic: '',
    blood_pressure_diastolic: '',
    weight: '',
    notes: ''
  });

  useEffect(() => {
    loadRecords();
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
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        checkup_date: formData.checkup_date,
        uric_acid: formData.uric_acid ? parseFloat(formData.uric_acid) : null,
        fasting_glucose: formData.fasting_glucose ? parseFloat(formData.fasting_glucose) : null,
        cholesterol_total: formData.cholesterol_total ? parseFloat(formData.cholesterol_total) : null,
        blood_pressure_systolic: formData.blood_pressure_systolic ? parseInt(formData.blood_pressure_systolic) : null,
        blood_pressure_diastolic: formData.blood_pressure_diastolic ? parseInt(formData.blood_pressure_diastolic) : null,
        weight: formData.weight ? parseFloat(formData.weight) : null,
        notes: formData.notes
      };
      await apiService.createMedicalCheckup(payload);
      setIsAdding(false);
      setFormData({
        checkup_date: new Date().toISOString().split('T')[0],
        uric_acid: '',
        fasting_glucose: '',
        cholesterol_total: '',
        blood_pressure_systolic: '',
        blood_pressure_diastolic: '',
        weight: '',
        notes: ''
      });
      loadRecords();
    } catch (error) {
      alert("Lỗi khi lưu hồ sơ: " + error.message);
    }
  };

  if (loading) return <div className="p-4 text-center">Đang tải dữ liệu...</div>;

  return (
    <div className="p-4 mb-20">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Hồ sơ xét nghiệm</h1>
        <button 
          onClick={() => setIsAdding(!isAdding)}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl text-sm font-medium shadow-sm"
        >
          {isAdding ? "Hủy" : "+ Thêm mới"}
        </button>
      </div>

      {isAdding && (
        <div className="bg-white rounded-2xl p-5 shadow-sm mb-6 border border-gray-100">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ngày xét nghiệm</label>
              <input type="date" name="checkup_date" value={formData.checkup_date} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" required />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Axit Uric (mg/dL)</label>
                <input type="number" step="0.1" name="uric_acid" value={formData.uric_acid} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="VD: 7.2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Đường huyết (mmol/L)</label>
                <input type="number" step="0.1" name="fasting_glucose" value={formData.fasting_glucose} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="VD: 5.5" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cholesterol (mmol/L)</label>
                <input type="number" step="0.1" name="cholesterol_total" value={formData.cholesterol_total} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="VD: 5.2" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Cân nặng (kg)</label>
                <input type="number" step="0.1" name="weight" value={formData.weight} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="VD: 70" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">HA tâm thu</label>
                <input type="number" name="blood_pressure_systolic" value={formData.blood_pressure_systolic} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="120" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">HA tâm trương</label>
                <input type="number" name="blood_pressure_diastolic" value={formData.blood_pressure_diastolic} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl" placeholder="80" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ghi chú thêm</label>
              <textarea name="notes" value={formData.notes} onChange={handleInputChange} className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl h-24" placeholder="Ghi chú..."></textarea>
            </div>

            <button type="submit" className="w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md">
              Lưu kết quả xét nghiệm
            </button>
          </form>
        </div>
      )}

      <div className="space-y-4">
        {records.length === 0 ? (
          <div className="text-center p-8 bg-white rounded-2xl border border-gray-100">
            <p className="text-gray-500">Chưa có hồ sơ xét nghiệm nào.</p>
            <p className="text-sm text-gray-400 mt-2">Hãy thêm kết quả xét nghiệm để AI tư vấn chính xác hơn.</p>
          </div>
        ) : (
          records.map((record) => (
            <div key={record.id} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
              <div className="font-bold text-lg text-blue-800 mb-3 border-b pb-2">
                Ngày {new Date(record.checkup_date).toLocaleDateString('vi-VN')}
              </div>
              <div className="grid grid-cols-2 gap-y-3 gap-x-4 text-sm">
                {record.uric_acid && (
                  <div><span className="text-gray-500 block">Axit Uric</span><span className="font-semibold text-red-600">{record.uric_acid} mg/dL</span></div>
                )}
                {record.fasting_glucose && (
                  <div><span className="text-gray-500 block">Đường huyết</span><span className="font-semibold">{record.fasting_glucose} mmol/L</span></div>
                )}
                {record.cholesterol_total && (
                  <div><span className="text-gray-500 block">Cholesterol</span><span className="font-semibold">{record.cholesterol_total} mmol/L</span></div>
                )}
                {record.blood_pressure_systolic && (
                  <div><span className="text-gray-500 block">Huyết áp</span><span className="font-semibold">{record.blood_pressure_systolic}/{record.blood_pressure_diastolic}</span></div>
                )}
              </div>
              {record.notes && (
                <div className="mt-4 pt-3 border-t border-gray-100">
                  <span className="text-gray-500 block text-xs font-semibold mb-1">KẾT LUẬN / GHI CHÚ CHUYÊN KHOA:</span>
                  <p className="text-sm text-gray-700 whitespace-pre-wrap">{record.notes}</p>
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
