with open('frontend/src/App.jsx', 'rb') as f:
    data = f.read()

# \x0c is form feed
data = data.replace(b'\\x0clex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', b'lex flex-col items-center justify-center w-full h-full space-y-1 transition-all  ')
data = data.replace(b'\\x0clex flex-col items-center justify-center w-full h-full space-y-1 transition-all }', b'lex flex-col items-center justify-center w-full h-full space-y-1 transition-all  ')

with open('frontend/src/App.jsx', 'wb') as f:
    f.write(data)
