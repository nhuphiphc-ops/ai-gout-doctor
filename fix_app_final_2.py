import re

with open('frontend/src/App.jsx', 'rb') as f:
    text = f.read()

# Replace any occurrence of the form feed and the word lex
text = text.replace(b'\x0clex', b'lex')

with open('frontend/src/App.jsx', 'wb') as f:
    f.write(text)
