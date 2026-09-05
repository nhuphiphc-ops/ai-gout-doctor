import re

with open('backend/schemas.py', 'r', encoding='utf-8') as f:
    schemas_content = f.read()

if 'class VideoScriptRequest' not in schemas_content:
    schemas_content += '''\n
class VideoScriptRequest(BaseModel):
    topic: str
    format: str
    tone: str
    audience: str
'''
    with open('backend/schemas.py', 'w', encoding='utf-8') as f:
        f.write(schemas_content)

with open('backend/ai_engine.py', 'r', encoding='utf-8') as f:
    ai_content = f.read()

if 'def generate_video_script' not in ai_content:
    ai_content += '''\n
def generate_video_script(topic: str, format: str, tone: str, audience: str, api_key: str = None) -> str:
    import os
    import google.generativeai as genai
    
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        return "Lỗi: Không tìm thấy API Key. Hãy cấu hình API Key trong trang Cài đặt (Nhật ký)."
        
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
Bạn là một chuyên gia sáng tạo nội dung đa nền tảng cho kênh "Sức khỏe Mr. Phi".
Hãy viết một kịch bản video y tế / sức khỏe.
Chủ đề: {topic}
Định dạng: {format}
Tông giọng: {tone}
Đối tượng mục tiêu: {audience}

Yêu cầu xuất đầu ra CHÍNH XÁC theo chuẩn Markdown để dễ đọc:
# Kịch bản Video: [Tên chủ đề]

**Thông tin chung:**
- **Định dạng:** {format}
- **Tông giọng:** {tone}
- **Đối tượng:** {audience}

---

## 1. Mở bài (Hook - 3-5 giây đầu)
[Viết câu giật tít, nêu vấn đề chạm nỗi đau hoặc phản trực giác]

## 2. Thân bài (Nội dung chính)
| Cảnh / Thời gian | Lời thoại (Voice-over / Host) | Hình ảnh mô tả (Visual/B-roll/Text) |
|---|---|---|
| [0:05 - 0:10] | [Lời thoại] | [Mô tả hình ảnh] |
| [0:10 - 0:20] | [Lời thoại] | [Mô tả hình ảnh] |
(Tiếp tục các dòng tùy theo độ dài video)

## 3. Kêu gọi hành động (Call-to-Action)
[Viết lời kêu gọi tương tác, theo dõi kênh Sức khỏe Mr. Phi]

## 4. Miễn trừ trách nhiệm y tế
*Lưu ý: Nội dung video này chỉ mang tính chất tham khảo, không thay thế chẩn đoán và điều trị y khoa. Vui lòng tham khảo ý kiến Bác sĩ trước khi áp dụng.*
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi khi tạo kịch bản AI: {str(e)}"
'''
    with open('backend/ai_engine.py', 'w', encoding='utf-8') as f:
        f.write(ai_content)

with open('backend/main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

if '@app.post("/api/video-script/generate")' not in main_content:
    route_code = '''\n
@app.post("/api/video-script/generate")
def generate_video_script(
    query: schemas.VideoScriptRequest,
    current_user: models.User = Depends(auth.get_current_user)
):
    import ai_engine
    import os
    api_key = os.getenv("GEMINI_API_KEY")
    script = ai_engine.generate_video_script(
        topic=query.topic,
        format=query.format,
        tone=query.tone,
        audience=query.audience,
        api_key=api_key
    )
    return {"script": script}
'''
    main_content += route_code
    with open('backend/main.py', 'w', encoding='utf-8') as f:
        f.write(main_content)
