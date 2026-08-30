import re
with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'className=\{.lex \}', r'className="flex"', text)

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
