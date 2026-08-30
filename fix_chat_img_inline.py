import re
with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace any existing width/height classes with explicit style
text = re.sub(
    r'<img src=\{userProfile\.avatar_url\} alt="User" className="w-[0-9]+ h-[0-9]+',
    r'<img src={userProfile.avatar_url} alt="User" style={{ width: \'20px\', height: \'20px\' }} className="',
    text
)

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
