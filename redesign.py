import os
import re

def replace_colors_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tailwind classes replacements
    content = content.replace('bg-blue-600', 'bg-green-600')
    content = content.replace('bg-blue-500', 'bg-green-500')
    content = content.replace('bg-blue-700', 'bg-green-700')
    
    content = content.replace('text-blue-400', 'text-green-400')
    content = content.replace('text-blue-500', 'text-green-500')
    content = content.replace('text-blue-600', 'text-green-600')
    
    content = content.replace('border-blue-500', 'border-green-500')
    content = content.replace('border-blue-400', 'border-green-400')
    
    content = content.replace('from-blue-600', 'from-green-600')
    content = content.replace('to-indigo-600', 'to-yellow-500')
    content = content.replace('to-indigo-500', 'to-yellow-400')
    content = content.replace('hover:from-blue-500', 'hover:from-green-500')
    
    content = content.replace('text-indigo-400', 'text-yellow-400')
    content = content.replace('text-purple-400', 'text-green-400')
    content = content.replace('text-pink-400', 'text-yellow-400')
    content = content.replace('text-orange-400', 'text-green-400')
    
    # CSS hex replacements (for inline styles)
    content = content.replace('#3b82f6', '#22c55e') # blue-500 to green-500
    content = content.replace('#2563eb', '#16a34a') # blue-600 to green-600
    content = content.replace('#8b5cf6', '#eab308') # violet-500 to yellow-500
    content = content.replace('#a855f7', '#facc15') # purple-500 to yellow-400
    
    # rgba replacements for drop-shadow
    content = content.replace('129,140,248', '234,179,8') # indigo to yellow
    content = content.replace('192,132,252', '34,197,94') # purple to green
    content = content.replace('244,114,182', '234,179,8') # pink to yellow
    content = content.replace('251,146,60', '34,197,94')  # orange to green

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

src_dir = 'frontend/src'
for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.jsx', '.js')):
            replace_colors_in_file(os.path.join(root, file))

# Update index.css
css_path = 'frontend/src/index.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('--bg-primary: radial-gradient(circle at 50% -20%, #1e3a8a 0%, #0b0f19 80%);', '--bg-primary: radial-gradient(circle at 50% -20%, #064e3b 0%, #0f172a 80%);')
css = css.replace('--color-accent: #6366f1;', '--color-accent: #eab308;')
css = css.replace('background: linear-gradient(135deg, var(--color-primary) 0%, #2563eb 100%);', 'background: linear-gradient(135deg, var(--color-primary) 0%, #eab308 100%);')
css = css.replace('border-left: 4px solid #3b82f6;', 'border-left: 4px solid #eab308;')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Redesign applied.")
