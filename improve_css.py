import re

with open('frontend/src/index.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Make background more premium (dark blue gradient)
text = re.sub(
    r'--bg-primary: #0b0f19;',
    r'--bg-primary: radial-gradient(circle at 50% -20%, #1e3a8a 0%, #0b0f19 80%);\n  --bg-color-fallback: #0b0f19;',
    text
)

# Apply fallback background to body
text = re.sub(
    r'background: var\(--bg-primary\);',
    r'background-color: var(--bg-color-fallback);\n  background-image: var(--bg-primary);\n  background-attachment: fixed;',
    text
)

# Make cards glassmorphic
text = re.sub(
    r'--bg-card: rgba\(23, 32, 53, 0\.7\);',
    r'--bg-card: rgba(15, 23, 42, 0.6);\n  backdrop-filter: blur(16px);\n  -webkit-backdrop-filter: blur(16px);',
    text
)

# Give cards a subtle border to match glassmorphism
text = re.sub(
    r'--border-color: rgba\(255, 255, 255, 0\.08\);',
    r'--border-color: rgba(255, 255, 255, 0.12);\n  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);',
    text
)

with open('frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(text)
