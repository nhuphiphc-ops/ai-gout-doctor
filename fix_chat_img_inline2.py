import re
with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r"\'", "'")
text = text.replace(r'\"', '"')

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
