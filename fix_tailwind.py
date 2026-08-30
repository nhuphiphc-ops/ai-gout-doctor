with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

tailwind_script = '''    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        corePlugins: {
          preflight: false
        }
      }
    </script>
    <title>'''

text = text.replace('    <title>', tailwind_script)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
