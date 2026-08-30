with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('className={\n', 'className={')
text = text.replace('av-btn \\}', 'nav-btn  }') # This is getting complicated
