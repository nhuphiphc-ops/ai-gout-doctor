import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app_text = f.read()

if 'import RecoveryGuideView from' not in app_text:
    app_text = app_text.replace("import ChatView from './components/ChatView';", "import ChatView from './components/ChatView';\nimport RecoveryGuideView from './components/RecoveryGuideView';")

if 'currentView === \\'guide\\'' not in app_text:
    guide_block = '''          {currentView === 'guide' && (
            <RecoveryGuideView />
          )}'''
    app_text = app_text.replace("          {currentView === 'chat' && (", guide_block + "\n          {currentView === 'chat' && (")

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app_text)
