with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()
import re
text = re.sub(r'className=\{max-w-\[85\%\] rounded-2xl p-3 shadow-sm \}', r'className="max-w-[85%] rounded-2xl p-3 shadow-sm"', text)
with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
