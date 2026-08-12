# AI Health Assistant - Bác Sĩ Gia Đình AI Quản Lý Gout & Sức Khỏe Cá Nhân

Hệ thống quản lý sức khỏe cá nhân lâu dài được xây dựng riêng cho nam giới 47 tuổi có tiền sử bệnh gout 11 năm. Ứng dụng chạy nội bộ trên máy tính (PC) và có thể truy cập mượt mà từ điện thoại di động thông qua mạng Wifi gia đình.

## Các tính năng chính
1. **Theo dõi sức khỏe hàng ngày (Morning & Afternoon)**:
   - **Sáng (07:00)**: Cập nhật cân nặng, huyết áp, nhịp tim, giấc ngủ, tình trạng đau khớp chân (ngón cái, mắt cá, đầu gối, bàn chân), mệt mỏi, stress và tâm trạng.
   - **Chiều (17:00)**: Ghi nhận số bước chân, thời gian đi bộ/tập luyện, lượng nước uống (mục tiêu 2.5L), thuốc đã sử dụng và checklist thực phẩm giàu purin (bia rượu, hải sản, nội tạng, thịt đỏ, đồ ngọt).
2. **Cố vấn sức khỏe AI**:
   - Tự động đánh giá điểm **Nguy cơ Gout**, **Điểm Tim mạch**, **Điểm Chuyển hóa** và chỉ số **Chất lượng sống (QoL)**.
   - Đưa ra lời khuyên dinh dưỡng, chế độ vận động và nhắc nhở uống nước theo chỉ số thực tế.
3. **Cảnh báo Gout cấp (Red Alert)**:
   - Kích hoạt cảnh báo đỏ nổi bật khi phát hiện triệu chứng đau nhức hoặc sưng tấy khớp kèm hướng dẫn giảm đau cấp tốc (uống nước, gác chân cao, chườm lạnh).
4. **Phân tích nâng cao (Correlation Report)**:
   - Tự động phân tích tương quan thống kê sau 30 ngày để lập bảng **Top 20 thực phẩm liên đới cao nhất tới các cơn đau khớp chân** của riêng cơ địa người dùng.
5. **Xuất báo cáo**:
   - Hỗ trợ xuất dữ liệu sức khỏe ra file **Excel (.xlsx)**, **Word (.docx)** và **PDF (.pdf)** chất lượng cao.

---

## Kiến trúc hệ thống
* **Frontend**: React + Vite (Vanilla CSS theme tối, glassmorphism, chữ lớn cho tuổi trung niên).
* **Backend**: Python FastAPI (SQLAlchemy, Pandas, ReportLab, python-docx).
* **Database**: PostgreSQL.
* **Đóng gói**: Docker & Docker Compose.

---

## Hướng dẫn cài đặt và chạy ứng dụng

### Yêu cầu hệ thống
* Đã cài đặt **Docker** và **Docker Compose** trên PC. (Tải tại [Docker Desktop](https://www.docker.com/products/docker-desktop/)).

### Khởi động ứng dụng
1. Mở PowerShell hoặc Command Prompt tại thư mục dự án:
   ```powershell
   cd "c:\Users\Admin\Desktop\DU AN SUC KHOE MR PHI"
   ```
2. Khởi chạy toàn bộ hệ thống bằng Docker Compose:
   ```powershell
   docker-compose up -d --build
   ```
3. Sau khi khởi động thành công:
   - **Frontend** chạy tại: `http://localhost:3000`
   - **Backend API** chạy tại: `http://localhost:8000` (Tài liệu API Swagger tại `http://localhost:8000/docs`)

---

## Hướng dẫn truy cập từ Điện thoại (LAN Wifi)

Để sử dụng ứng dụng trên điện thoại di động:
1. Đảm bảo cả PC và điện thoại của anh đang kết nối vào **cùng một mạng Wifi gia đình**.
2. Tìm địa chỉ IP nội bộ của PC:
   - Mở CMD trên PC và gõ: `ipconfig`
   - Tìm dòng `IPv4 Address` thuộc card mạng Wifi (Ví dụ: `192.168.1.15`).
3. Trên điện thoại, mở trình duyệt và truy cập:
   ```
   http://[IP_CỦA_PC]:3000
   ```
   *(Ví dụ: `http://192.168.1.15:3000`)*
4. Hệ thống đã được lập trình để tự động nhận dạng IP của PC và điều hướng API về đúng cổng `8000` trên PC của anh mà không bị lỗi kết nối!

---

## Hướng dẫn sao lưu dữ liệu sức khỏe (Backup & Restore)

Vì dữ liệu sức khỏe tích lũy theo năm là tài sản vô cùng quan trọng, anh nên thực hiện sao lưu định kỳ.

### 1. Sao lưu dữ liệu (Backup)
Anh có thể chạy lệnh sau trong PowerShell của PC để xuất toàn bộ cơ sở dữ liệu ra một file SQL dự phòng:
```powershell
docker exec -t health_postgres_db pg_dumpall -c -U postgres > "c:\Users\Admin\Desktop\DU AN SUC KHOE MR PHI\backup_health_db.sql"
```
*Lời khuyên: Nên lưu trữ file `backup_health_db.sql` này lên Google Drive hoặc USB định kỳ mỗi tháng.*

### 2. Phục hồi dữ liệu (Restore)
Nếu chuyển sang máy tính mới hoặc cài lại hệ thống, anh có thể phục hồi dữ liệu từ file sao lưu bằng cách:
1. Chạy `docker-compose up -d` để khởi động cơ sở dữ liệu mới.
2. Chạy lệnh phục hồi:
```powershell
cat "c:\Users\Admin\Desktop\DU AN SUC KHOE MR PHI\backup_health_db.sql" | docker exec -i health_postgres_db psql -U postgres
```

---

## Tuyên bố miễn trừ trách nhiệm (Medical Disclaimer)
Hệ thống này được thiết kế để hỗ trợ cá nhân tự theo dõi và điều chỉnh thói quen sinh hoạt. Các cảnh báo gout cấp hay tim mạch không cấu thành chẩn đoán y khoa chính thức. Trong trường hợp đau khớp dữ dội hoặc huyết áp cao vượt ngưỡng cảnh báo đỏ liên tục, người dùng cần lập tức thăm khám tại cơ sở y tế uy tín.
