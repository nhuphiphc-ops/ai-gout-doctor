import re

# Fix ChatView
with open('frontend/src/components/ChatView.jsx', 'r', encoding='utf-8') as f:
    chat = f.read()

chat = chat.replace('bg-gray-50', 'bg-transparent text-gray-100')
chat = chat.replace('bg-white', 'bg-[#1e293b]/80 backdrop-blur-md border-white/10')
chat = chat.replace('text-gray-800', 'text-white')
chat = chat.replace('text-gray-600', 'text-gray-300')
chat = chat.replace('bg-gray-100', 'bg-white/10')
chat = chat.replace('bg-blue-50', 'bg-blue-900/40')
chat = chat.replace('border-blue-100', 'border-blue-500/30')
chat = chat.replace('text-blue-800', 'text-blue-200')
chat = chat.replace('text-blue-600', 'text-blue-300')
chat = chat.replace('border-gray-100', 'border-white/10')
chat = chat.replace('bg-gray-300', 'bg-gray-500')
chat = chat.replace('border-blue-200', 'border-blue-500/50')
chat = chat.replace('text-green-700', 'text-green-300')
chat = chat.replace('bg-green-100', 'bg-green-900/50')

with open('frontend/src/components/ChatView.jsx', 'w', encoding='utf-8') as f:
    f.write(chat)

# Fix MedicalRecordsView
with open('frontend/src/components/MedicalRecordsView.jsx', 'r', encoding='utf-8') as f:
    med = f.read()

med = med.replace('bg-gray-50', 'bg-transparent text-gray-100')
med = med.replace('bg-white', 'bg-[#1e293b]/80 backdrop-blur-md border-white/10')
med = med.replace('text-gray-800', 'text-white')
med = med.replace('text-gray-700', 'text-gray-300')
med = med.replace('text-gray-600', 'text-gray-400')
med = med.replace('text-gray-500', 'text-gray-400')
med = med.replace('bg-gray-100', 'bg-white/10')
med = med.replace('border-blue-100', 'border-blue-500/30')
med = med.replace('text-blue-800', 'text-blue-300')
med = med.replace('text-blue-700', 'text-blue-200')
med = med.replace('border-gray-100', 'border-white/10')
med = med.replace('border-gray-200', 'border-white/20')
med = med.replace('border-gray-50', 'border-white/5')
med = med.replace('bg-blue-100', 'bg-blue-900/50')

with open('frontend/src/components/MedicalRecordsView.jsx', 'w', encoding='utf-8') as f:
    f.write(med)
