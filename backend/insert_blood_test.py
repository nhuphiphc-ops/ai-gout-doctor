import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, MedicalCheckup

def insert_record():
    db = SessionLocal()
    user = db.query(User).first()
    
    if not user:
        print("No user found")
        return
        
    checkup = MedicalCheckup(
        user_id=user.id,
        checkup_date=datetime.date(2026, 7, 31),
        uric_acid=505.54,  # umol/L
        fasting_glucose=5.49,
        cholesterol_total=5.52,
        triglyceride=1.39,
        ast=25.0,
        alt=22.5,
        creatinine=109.87,
        notes="KẾT QUẢ XÉT NGHIỆM MÁU (31/07/2026):\n- Axit Uric: Tăng RẤT CAO (505.54 µmol/L, ngưỡng < 420). Đây là nguyên nhân cốt lõi gây Gout.\n- Cholesterol toàn phần: Tăng nhẹ (5.52 mmol/L, ngưỡng < 5.2).\n- Creatinine: Hơi cao (109.87 µmol/L), cho thấy thận đang lọc kém đi một chút so với bình thường."
    )
    db.add(checkup)
    db.commit()
    print("Successfully added blood test record to database.")
    db.close()

if __name__ == '__main__':
    insert_record()
