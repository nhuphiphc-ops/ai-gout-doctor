import re

with open('frontend/src/components/Dashboard.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

btn_pattern = r'          \{\/\* Video Script Module Button \*\/\}.*?Tạo Kịch Bản Mới\n            </button>\n          </div>'
match = re.search(btn_pattern, text, flags=re.DOTALL)
if match:
    btn_html = match.group(0)
    text = text.replace(btn_html + '\n\n', '') # remove from bottom
    
    # insert above scores-container
    insert_point = '      {/* Scores Grid */}'
    text = text.replace(insert_point, btn_html + '\n\n' + insert_point)
    
    with open('frontend/src/components/Dashboard.jsx', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Moved successfully.")
else:
    print("Button not found!")
