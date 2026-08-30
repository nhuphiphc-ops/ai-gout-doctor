import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('lex', 'lex')

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
