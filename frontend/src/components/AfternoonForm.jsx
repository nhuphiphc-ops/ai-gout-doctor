import React, { useState, useEffect } from 'react';
import { Moon, ArrowLeft, Footprints, Droplet, Plus, X, Pill } from 'lucide-react';
import apiService from '../services/api';

export default function AfternoonForm({ todayLog, onSave, onCancel }) {
  const [steps, setSteps] = useState(6000);
  const [walkingDuration, setWalkingDuration] = useState(30);
  const [exerciseDuration, setExerciseDuration] = useState(0);
  const [waterIntake, setWaterIntake] = useState(2.0);

  // Diet checklist
  const [hadAlcohol, setHadAlcohol] = useState(false);
  const [hadBeer, setHadBeer] = useState(false);
  const [hadSeafood, setHadSeafood] = useState(false);
  const [hadOrganMeat, setHadOrganMeat] = useState(false);
  const [hadRedMeat, setHadRedMeat] = useState(false);
  const [hadSweets, setHadSweets] = useState(false);

  // Tag inputs
  const [foodsConsumed, setFoodsConsumed] = useState([]);
  const [foodInput, setFoodInput] = useState('');
  const [medications, setMedications] = useState([]);
  const [medInput, setMedInput] = useState('');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Populate data if already exists
  useEffect(() => {
    if (todayLog && todayLog.afternoon_completed) {
      setSteps(todayLog.steps || 0);
      setWalkingDuration(todayLog.walking_duration || 0);
      setExerciseDuration(todayLog.exercise_duration || 0);
      setWaterIntake(todayLog.water_intake || 0.0);
      
      setHadAlcohol(todayLog.had_alcohol || false);
      setHadBeer(todayLog.had_beer || false);
      setHadSeafood(todayLog.had_seafood || false);
      setHadOrganMeat(todayLog.had_organ_meat || false);
      setHadRedMeat(todayLog.had_red_meat || false);
      setHadSweets(todayLog.had_sweets || false);

      setFoodsConsumed(todayLog.foods.map(f => f.food_name) || []);
      setMedications(todayLog.medications.map(m => m.med_name) || []);
    }
  }, [todayLog]);

  // Handle adding custom food tag
  const handleAddFood = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const val = foodInput.trim().replace(',', '');
      if (val && !foodsConsumed.includes(val)) {
        setFoodsConsumed([...foodsConsumed, val]);
      }
      setFoodInput('');
    }
  };

  const removeFood = (index) => {
    setFoodsConsumed(foodsConsumed.filter((_, i) => i !== index));
  };

  // Handle adding medication tag
  const handleAddMed = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      const val = medInput.trim().replace(',', '');
      if (val && !medications.includes(val)) {
        setMedications([...medications, val]);
      }
      setMedInput('');
    }
  };

  const removeMed = (index) => {
    setMedications(medications.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const payload = {
      steps: parseInt(steps),
      walking_duration: parseInt(walkingDuration),
      exercise_duration: parseInt(exerciseDuration),
      water_intake: parseFloat(waterIntake),
      foods_consumed: foodsConsumed,
      had_alcohol: hadAlcohol || hadBeer, // beer is alcohol
      had_beer: hadBeer,
      had_seafood: hadSeafood,
      had_organ_meat: hadOrganMeat,
      had_red_meat: hadRedMeat,
      had_sweets: hadSweets,
      medications: medications,
    };

    try {
      const response = await apiService.submitAfternoonLog(payload);
      onSave(response);
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra khi gửi dữ liệu.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <button 
        onClick={onCancel}
        className="nav-btn" 
        style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', marginBottom: '20px', padding: '6px 12px' }}
      >
        <ArrowLeft size={16} />
        <span>Quay lại Dashboard</span>
      </button>

      <h2 className="form-title">
        <Moon size={28} color="var(--color-accent)" />
        <span>Cập nhật hoạt động Buổi Chiều (17:00)</span>
      </h2>

      {error && (
        <div style={{ background: 'var(--color-danger-light)', border: '1px solid var(--color-danger)', color: 'var(--color-danger)', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '16px' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>

        {/* Row 1: Steps & Water */}
        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="steps">
              Số bước chân đi bộ <Footprints size={14} style={{ display: 'inline', color: 'var(--color-primary)' }} />
            </label>
            <input 
              type="number" 
              id="steps"
              className="form-input"
              value={steps}
              onChange={(e) => setSteps(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="water">
              Lượng nước đã uống (Lít) <Droplet size={14} style={{ display: 'inline', color: 'var(--color-accent)' }} />
            </label>
            <input 
              type="number" 
              step="0.1"
              id="water"
              className="form-input"
              value={waterIntake}
              onChange={(e) => setWaterIntake(e.target.value)}
              required
            />
            <span style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
              Mục tiêu khuyến nghị để đào thải tốt Uric: <strong>2.5 Lít/ngày</strong>
            </span>
          </div>
        </div>

        {/* Row 2: Walking & Workout times */}
        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="walking">Thời gian đi bộ (phút)</label>
            <input 
              type="number" 
              id="walking"
              className="form-input"
              value={walkingDuration}
              onChange={(e) => setWalkingDuration(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="exercise">Vận động khác / Tập thể thao (phút)</label>
            <input 
              type="number" 
              id="exercise"
              className="form-input"
              value={exerciseDuration}
              onChange={(e) => setExerciseDuration(e.target.value)}
              required
            />
          </div>
        </div>

        {/* Gout Risk Food checklist */}
        <div className="form-group">
          <label className="form-label">
            Hôm nay anh có sử dụng các nhóm thực phẩm sau không?
          </label>
          <div className="food-checkboxes-grid">
            <div 
              className={`food-checkbox-card danger-food ${hadBeer ? 'selected' : ''}`}
              onClick={() => setHadBeer(!hadBeer)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Bia (Cồn cao)</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Nguy cơ cực cao kích thích gout</div>
              </div>
            </div>

            <div 
              className={`food-checkbox-card danger-food ${hadAlcohol && !hadBeer ? 'selected' : ''}`}
              onClick={() => setHadAlcohol(!hadAlcohol)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Rượu mạnh / Vang</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Giảm khả năng lọc uric qua thận</div>
              </div>
            </div>

            <div 
              className={`food-checkbox-card danger-food ${hadOrganMeat ? 'selected' : ''}`}
              onClick={() => setHadOrganMeat(!hadOrganMeat)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Nội tạng động vật</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Lòng mề, gan, cật chứa purin cao</div>
              </div>
            </div>

            <div 
              className={`food-checkbox-card danger-food ${hadSeafood ? 'selected' : ''}`}
              onClick={() => setHadSeafood(!hadSeafood)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Hải sản (Tôm, tôm hùm, cua...)</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Giàu dinh dưỡng & purin vỏ</div>
              </div>
            </div>

            <div 
              className={`food-checkbox-card danger-food ${hadRedMeat ? 'selected' : ''}`}
              onClick={() => setHadRedMeat(!hadRedMeat)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Thịt đỏ (Bò, trâu, bê...)</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Hạn chế ở mức vừa phải</div>
              </div>
            </div>

            <div 
              className={`food-checkbox-card warning-food ${hadSweets ? 'selected' : ''}`}
              onClick={() => setHadSweets(!hadSweets)}
            >
              <div className="checkbox-dot" />
              <div>
                <strong>Đồ ngọt / Nước ngọt có ga</strong>
                <div style={{ fontSize: '12px', opacity: 0.8 }}>Fructose tăng tổng hợp uric acid</div>
              </div>
            </div>
          </div>
        </div>

        {/* Custom food items tag inputs */}
        <div className="form-group">
          <label className="form-label" htmlFor="food-input">
            Các món ăn cụ thể đã ăn hôm nay (Gõ tên món rồi ấn <strong>Enter</strong> hoặc dấu phẩy)
          </label>
          <div className="tag-input-container">
            {foodsConsumed.map((food, i) => (
              <span key={i} className="tag-badge">
                {food}
                <X size={14} className="tag-close" onClick={() => removeFood(i)} />
              </span>
            ))}
            <input
              type="text"
              id="food-input"
              className="tag-input-field"
              placeholder={foodsConsumed.length === 0 ? "Ví dụ: canh bầu nấu cá, cải bắp luộc, rau cần..." : "Thêm món khác..."}
              value={foodInput}
              onChange={(e) => setFoodInput(e.target.value)}
              onKeyDown={handleAddFood}
            />
          </div>
        </div>

        {/* Medications list */}
        <div className="form-group">
          <label className="form-label" htmlFor="med-input">
            Các thuốc điều trị/Thực phẩm chức năng đã uống (nếu có)
          </label>
          <div className="tag-input-container" style={{ borderColor: 'rgba(99, 102, 241, 0.2)' }}>
            {medications.map((med, i) => (
              <span key={i} className="tag-badge" style={{ background: 'rgba(99, 102, 241, 0.25)', border: '1px solid rgba(99, 102, 241, 0.4)' }}>
                <Pill size={14} style={{ marginRight: '4px', color: 'var(--color-accent)' }} />
                {med}
                <X size={14} className="tag-close" onClick={() => removeMed(i)} />
              </span>
            ))}
            <input
              type="text"
              id="med-input"
              className="tag-input-field"
              placeholder={medications.length === 0 ? "Ví dụ: Febuxostat 40mg, Colchicine..." : "Thêm thuốc khác..."}
              value={medInput}
              onChange={(e) => setMedInput(e.target.value)}
              onKeyDown={handleAddMed}
            />
          </div>
        </div>

        <div style={{ marginTop: '30px' }}>
          <button 
            type="submit" 
            className="btn" 
            disabled={loading}
          >
            {loading ? 'Đang lưu...' : 'Lưu hoạt động Buổi Chiều'}
          </button>
        </div>

      </form>
    </div>
  );
}
