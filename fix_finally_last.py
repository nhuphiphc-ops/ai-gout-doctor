import sys

with open('frontend/src/App.jsx', 'rb') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if b'\x0clex' in line:
        line = line.replace(b'\x0clex', b'lex')
    new_lines.append(line)

with open('frontend/src/App.jsx', 'wb') as f:
    f.writelines(new_lines)
