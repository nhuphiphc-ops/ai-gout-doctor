import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

if 'import VideoScriptView' not in text:
    text = text.replace('import RecoveryGuideView from \'./components/RecoveryGuideView\';', 'import RecoveryGuideView from \'./components/RecoveryGuideView\';\nimport VideoScriptView from \'./components/VideoScriptView\';')

if 'currentView === \'video_script\'' not in text:
    render_logic = '''      {currentView === 'guide' && <RecoveryGuideView />}
      {currentView === 'video_script' && <VideoScriptView />}'''
    text = text.replace('{currentView === \'guide\' && <RecoveryGuideView />}', render_logic)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
