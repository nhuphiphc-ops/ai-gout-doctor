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
        checkup_date=datetime.date(2026, 8, 8),
        notes="KẾT QUẢ SIÊU ÂM (08/08/2026):\n1. Ổ bụng: Thận phải có nang đơn thuần có nốt vôi hóa (~11.7x10mm). Các tạng khác (gan, túi mật, lách, thận trái...) bình thường.\n2. Tuyến giáp: TIRADS 3, cả 2 thùy có nhân hỗn hợp kích thước nhỏ (Thùy phải 10.3x4.3mm, Thùy trái 7.2x3.6mm), không tăng sinh mạch, nguy cơ ác tính thấp.\nKết luận chung: Uống đủ nước (1.5 - 2.5L/ngày), theo dõi định kỳ 6-12 tháng/lần."
    )
    db.add(checkup)
    db.commit()
    print("Successfully added ultrasound record to database.")
    db.close()

if __name__ == '__main__':
    insert_record()
