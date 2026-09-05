import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure Video icon is imported
if 'Video' not in text:
    text = text.replace('User \n} from', 'User,\n  Video\n} from')

nav_item = '''          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('video_script')}
          >
            <Video size={22} className={currentView === 'video_script' ? 'drop-shadow-[0_0_8px_rgba(129,140,248,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">Video AI</span>
          </button>
        </div>'''

text = text.replace('        </div>\n      </div>\n    </div>\n  );\n}', nav_item + '\n      </div>\n    </div>\n  );\n}')

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
