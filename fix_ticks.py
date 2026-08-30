import re

with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    chat = f.read()
chat = re.sub(r'className=\{mt-2.*?\}', 'className={mt-2 p-1.5 rounded-full flex items-center justify-center gap-1 text-xs font-medium transition-colors }', chat)
with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(chat)

with open('frontend/src/components/MedicalRecordsView.jsx', 'r', encoding='utf-8') as f:
    med = f.read()
# fix the template literals in med
med = re.sub(r'let text = Hồ sơ khám ngày \. ;', 'let text = Hồ sơ khám ngày . ;', med)
med = re.sub(r'Axit Uric:  miligam trên đê xi lít\. ', 'Axit Uric:  miligam trên đê xi lít. ', med)
med = re.sub(r'Đường huyết:  mi li mon trên lít\. ', 'Đường huyết:  mi li mon trên lít. ', med)
med = re.sub(r'Cholesterol:  mi li mon trên lít\. ', 'Cholesterol:  mi li mon trên lít. ', med)
med = re.sub(r'Huyết áp:  trên \. ', 'Huyết áp:  trên . ', med)
med = re.sub(r'Mức lọc cầu thận eGFR: \. ', 'Mức lọc cầu thận eGFR: . ', med)
med = re.sub(r'Kích thước nang thận: \. ', 'Kích thước nang thận: . ', med)
med = re.sub(r'Ghi chú chuyên khoa: \.', 'Ghi chú chuyên khoa: .', med)

# Also fix the button class in MedicalRecordsView
med = re.sub(r'className=\{absolute top-4 right-4 p-2 rounded-full \}', 'className={bsolute top-4 right-4 p-2 rounded-full }', med)

with open('frontend/src/components/MedicalRecordsView.jsx', 'w', encoding='utf-8') as f:
    f.write(med)
