import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "        <main className=\"flex-1 w-full flex flex-col pt-24\">"
end_marker = "          {/* Stats Section */}"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

new_hero = """        <main className="flex-1 w-full flex flex-col pt-16 md:pt-20">
          {/* Hero Section */}
          <div className="max-w-7xl mx-auto w-full px-6 lg:px-8 py-10 lg:py-16 flex flex-col lg:flex-row items-center justify-between min-h-[75vh]">
            
            {/* Left Side: Content */}
            <div className="w-full lg:w-1/2 flex flex-col items-start text-left relative z-10 lg:pr-8 xl:pr-12">
              <div className="border border-slate-900 text-[#1e1b4b] text-[10px] sm:text-xs font-bold tracking-[0.15em] uppercase px-3 py-1.5 sm:px-4 sm:py-2 mb-6 sm:mb-8 shadow-[2px_2px_0px_0px_rgba(30,27,75,0.1)] bg-white">
                Application Drafting, Automated
              </div>
              
              <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-slate-900 leading-[1.1] mb-5">
                Claim your <br className="hidden sm:block"/> rights in <span className="text-[#3b36e8]">plain <br className="hidden sm:block"/> language.</span>
              </h1>
              
              <p className="text-lg sm:text-xl text-slate-600 mb-8 max-w-md leading-relaxed">
                No legal jargon. No expensive lawyers. Describe your civic issue like you're talking to a friend — our AI drafts a legally sound RTI application.
              </p>
              
              <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="bg-[#1e1b4b] hover:bg-[#2e2b5e] text-white font-semibold text-base sm:text-lg py-3 sm:py-4 px-6 sm:px-8 rounded-xl transition-all flex items-center gap-2 shadow-[0_8px_30px_rgb(0,0,0,0.12)] active:scale-95">
                Start Drafting Now <ArrowRight size={18} />
              </button>
              <div className="mt-4 text-xs sm:text-sm text-slate-500 font-medium">
                Free to use · Takes about 2 minutes
              </div>
            </div>
            
            {/* Right Side: Graphic */}
            <div className="w-full lg:w-1/2 relative mt-16 lg:mt-0 flex justify-center lg:justify-end">
              {/* Added scale down on medium/small screens to prevent overflow */}
              <div className="relative w-full max-w-[450px] h-[350px] sm:h-[400px] scale-90 sm:scale-100 origin-center lg:origin-right">
                {/* Yellow Card (You Type) */}
                <div className="absolute top-0 left-0 w-4/5 bg-[#fffdf0] border border-[#fde68a] rounded-xl p-5 sm:p-6 shadow-sm rotate-[-3deg] z-10">
                  <div className="text-[#b45309] text-[10px] sm:text-[11px] font-bold uppercase tracking-widest mb-3">You Type</div>
                  <div className="text-[#334155] font-medium text-base sm:text-lg leading-relaxed">
                    "My road hasn't been repaired even though funds were sanctioned last year — why?"
                  </div>
                </div>
                
                {/* White Card (Drafted) */}
                <div className="absolute top-28 sm:top-32 right-0 w-[90%] bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-2xl z-20">
                  <div className="absolute -top-8 -right-4 sm:-right-8 w-[75px] h-[75px] sm:w-[90px] sm:h-[90px] rounded-full border-[3px] border-[#dc2626] text-[#dc2626] flex flex-col items-center justify-center rotate-[15deg] bg-white shadow-sm z-30">
                    <span className="text-[7px] sm:text-[9px] font-extrabold tracking-widest uppercase mb-0.5">Drafted</span>
                    <span className="text-[10px] sm:text-xs font-bold font-mono">RTI-01</span>
                  </div>
                  <div className="font-mono text-xs sm:text-[13px] text-slate-700 space-y-4 sm:space-y-5 leading-relaxed">
                    <div>
                      <span className="font-bold text-slate-900">To:</span> The Public Information Officer<br/>
                      Municipal Corporation
                    </div>
                    <div>
                      <span className="font-bold text-slate-900">Subject:</span> Information regarding sanctioned road repair funds.
                    </div>
                    <div>
                      1. Details of funds sanctioned for [Road Name], FY 2025-26.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>\n\n"""

text = text[:start_idx] + new_hero + text[end_idx:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Hero layout patched for responsiveness.")
