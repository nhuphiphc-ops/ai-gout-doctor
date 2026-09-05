import re

with open('frontend/src/services/api.js', 'r', encoding='utf-8') as f:
    text = f.read()

if 'generateVideoScript' not in text:
    api_method = '''
  // Video Script Generator
  generateVideoScript: async (data) => {
    const response = await api.post('/api/video-script/generate', data);
    return response.data;
  },
  
  // AI Chat'''
    text = text.replace('  // AI Chat', api_method)
    with open('frontend/src/services/api.js', 'w', encoding='utf-8') as f:
        f.write(text)
