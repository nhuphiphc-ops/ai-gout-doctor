with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('content: Chào anh, tôi là', 'content: \"Chào anh, tôi là Trợ lý AI Gout Doctor. Hôm nay sức khỏe của anh thế nào? Anh có cần tôi phân tích chỉ số xét nghiệm hay tư vấn thực đơn không?\" //')
with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
