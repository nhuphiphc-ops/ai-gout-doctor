with open('frontend/src/App.jsx', 'rb') as f:
    text = f.read().decode('utf-8')

import re
text = re.sub(r'className=\{\x0clex.*?\s*\}', 'className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', text, count=1)
text = re.sub(r'className=\{\x0clex.*?\s*\}', 'className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', text, count=1)
text = re.sub(r'className=\{\x0clex.*?\s*\}', 'className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', text, count=1)
text = re.sub(r'className=\{\x0clex.*?\s*\}', 'className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', text, count=1)
text = re.sub(r'className=\{\x0clex.*?\s*\}', 'className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', text, count=1)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
