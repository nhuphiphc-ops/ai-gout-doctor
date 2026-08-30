import re

with open('backend/ai_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

system_prompt_addition = '''\n\nNguồn cơ sở dữ liệu tích hợp:
- Nếu eGFR < 60: Thận đang suy giảm chức năng độ 3, cảnh báo cực kỳ nguy hiểm nếu bệnh nhân lạm dụng thuốc giảm đau NSAIDs (Colchicine, Ibuprofen).
- Siêu âm Thận: Nếu có nang (Cyst), dặn dò uống đủ 2-2.5L nước, tránh nhịn tiểu.
- Siêu âm Tuyến giáp (TIRADS 3): Nguy cơ ác tính thấp (<5%), không cần phẫu thuật ngay nhưng phải theo dõi 6-12 tháng. Nếu TSH/FT3/FT4 bất thường, cần điều chỉnh nội tiết.
- Bảng Tra cứu Purine Thực Phẩm:
  + Cực cao (>150mg/100g): Nội tạng động vật, cá mòi, cá trích, bia, rượu mạnh, nước cốt thịt. TUYỆT ĐỐI TRÁNH.
  + Cao trung bình (50-150mg/100g): Hải sản có vỏ (tôm, cua), thịt đỏ (bò, cừu), măng tây, súp lơ. HẠN CHẾ.
  + Thấp (<50mg/100g): Rau xanh, hoa quả, trứng, sữa tươi, phô mai. AN TOÀN.
Bạn phải dựa vào cơ sở dữ liệu trên để chấm điểm và phát hiện rủi ro. Khuyến nghị phải cực kỳ cá nhân hóa theo các chỉ số Thận và Tuyến Giáp của bệnh nhân Nguyễn Như Phi.'''

text = text.replace('Bạn là Bác sĩ chuyên khoa nội tiết và cơ xương khớp (AI Gout Doctor), hỗ trợ bệnh nhân Nguyễn Như Phi (sinh năm 1980).', 
                    'Bạn là Bác sĩ chuyên khoa nội tiết, thận học và cơ xương khớp (AI Gout Doctor), hỗ trợ bệnh nhân Nguyễn Như Phi (sinh năm 1980).' + system_prompt_addition)

with open('backend/ai_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)
