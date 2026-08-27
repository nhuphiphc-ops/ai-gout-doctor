# 🩺 HỆ THỐNG TỔNG HỢP & PHÂN TÍCH TÀI LIỆU – DỰ ÁN SỨC KHỎE MR PHI

Hệ thống module tự động hóa xử lý hồ sơ tài liệu đa định dạng (PDF Text/Scan OCR, Word `.docx`, Excel `.xlsx`), trích xuất thông tin then chốt và xuất báo cáo đa tầng.

---

## 📁 Cấu Trúc Module trong Dự Án

```text
E:\DU AN SUC KHOE MR PHI\
├── document_aggregator.py    # Module xử lý lõi: Đọc file, OCR scan, bóc tách thực thể, xuất Excel
├── webapp.py                 # Giao diện WebApp Streamlit trực quan 4 Tab
├── run_webapp.bat            # Tệp nhấp đúp (1-click) để mở nhanh WebApp
└── README.md                 # Tài liệu hướng dẫn sử dụng
```

---

## 🚀 Cách Sử Dụng

### Cách 1: Sử dụng Giao diện WebApp (Khuyến nghị)
- **Cách mở nhanh:** Nhấp đúp chuột vào tệp `run_webapp.bat`.
- **Hoặc chạy lệnh qua Terminal / PowerShell:**
  ```powershell
  cd "E:\DU AN SUC KHOE MR PHI"
  python -m streamlit run webapp.py --server.port 8502
  ```
- Mở trình duyệt tại: **`http://localhost:8502`**

### Cách 2: Sử dụng Module Python trong Code / Script khác
```python
from document_aggregator import DocumentAggregator

# 1. Khởi tạo công cụ
agg = DocumentAggregator(project_name="Dự Án Sức Khỏe Mr Phi")

# 2. Quét cả thư mục hồ sơ (tự động OCR các file PDF scan)
agg.read_folder(r"E:\DU AN SUC KHOE MR PHI", recursive=True)

# 3. Xuất file báo cáo Excel nhiều sheet hoàn chỉnh
agg.export_excel("Bao_cao_tong_hop.xlsx")
```

---

## 🌟 Các Tính Năng Chính
1. **OCR Siêu Tốc & Tự Động Lưu Cache:** Tự nhận diện các trang scan hình ảnh trong file PDF để bóc tách toàn văn sang dạng text rõ ràng.
2. **Trích Xuất Thông Tin Then Chốt (Key Entities):** Tự động lọc ra các mốc số tiền, ngày tháng, số văn bản, cơ quan/đơn vị/nhân sự liên quan.
3. **Smart Document Reader:** Trình đọc văn bản trực tiếp trên giao diện web, chọn trang và tra cứu nhanh chóng.
4. **Bảng Tính & Tìm Kiếm:** Lọc và tra cứu tức thì trên các bảng dữ liệu Excel.
5. **Xuất Excel 6 Sheet:** Chuẩn định dạng báo cáo quản trị.
