import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '''      <div className="fixed bottom-0 left-0 right-0 bg-[#0f172a]/90 backdrop-blur-xl border-t border-white/10 z-50 px-2 pb-safe pt-2">
        <div className="flex justify-around items-center h-16 max-w-md mx-auto">
          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('dashboard')}
          >
            <Home size={22} className={currentView === 'dashboard' ? 'drop-shadow-[0_0_8px_rgba(96,165,250,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">Nhật ký</span>
          </button>
          
          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('chat')}
          >
            <MessageCircle size={22} className={currentView === 'chat' ? 'drop-shadow-[0_0_8px_rgba(74,222,128,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">AI Bác sĩ</span>
          </button>
          
          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('medical')}
          >
            <FileText size={22} className={currentView === 'medical' ? 'drop-shadow-[0_0_8px_rgba(192,132,252,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">Hồ sơ</span>
          </button>
          
          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('charts')}
          >
            <TrendingUp size={22} className={currentView === 'charts' ? 'drop-shadow-[0_0_8px_rgba(251,146,60,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">Biểu đồ</span>
          </button>
          
          <button 
            className={lex flex-col items-center justify-center w-full h-full space-y-1 transition-all } 
            onClick={() => setCurrentView('profile')}
          >
            <User size={22} className={currentView === 'profile' ? 'drop-shadow-[0_0_8px_rgba(244,114,182,0.8)]' : ''} />
            <span className="text-[10px] font-medium tracking-wide">Cá nhân</span>
          </button>
        </div>
      </div>'''

text = re.sub(r'<div className="mobile-bottom-nav">.*</div>', replacement, text, flags=re.DOTALL)

with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)
