import re
with open('frontend/src/services/api.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('sendChatMessage: async (message) => {', 'sendChatMessage: async (message, apiKey) => {')
text = text.replace('const response = await axios.post(${API_URL}/api/chat, { message });', 'const response = await axios.post(${API_URL}/api/chat, { message }, { headers: { "X-Gemini-Key": apiKey } });')

with open('frontend/src/services/api.js', 'w', encoding='utf-8') as f:
    f.write(text)
