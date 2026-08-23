import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace from `if (currentView === 'landing') {` up to `// --- VIEW 2: APPLICATION INTERFACE ---`

start_marker = "if (currentView === 'landing') {"
end_marker = "  // --- VIEW 2: APPLICATION INTERFACE ---"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

new_landing = """if (currentView === 'landing') {
    return (
      <div className="min-h-screen w-full bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">
        <nav className="w-full flex items-center justify-between px-8 py-6 bg-transparent absolute top-0 z-50">
          <div className="flex items-center gap-3 font-bold text-2xl tracking-tight text-slate-900 cursor-pointer">
            <div className="w-10 h-10 bg-[#1e1b4b] text-white rounded-lg flex items-center justify-center shadow-sm"><Scale size={20} /></div>
            <div className="flex flex-col justify-center leading-tight"><span>Civic<span className="text-[#3b36e8] font-normal">Action</span></span></div>
          </div>
          <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="bg-transparent hover:bg-slate-100 text-slate-800 font-semibold py-2 px-6 rounded-lg border border-slate-300 transition-all shadow-sm">
            {isAuthenticated ? 'Go to Dashboard' : 'Sign In'}
          </button>
        </nav>
        
        <main className="flex-1 w-full flex flex-col pt-24">
          {/* Hero Section */}
          <div className="max-w-7xl mx-auto w-full px-8 py-20 flex flex-col lg:flex-row items-center justify-between min-h-[85vh]">
            
            {/* Left Side: Content */}
            <div className="w-full lg:w-1/2 flex flex-col items-start text-left relative z-10 lg:pr-12">
              <div className="border border-slate-900 text-[#1e1b4b] text-xs font-bold tracking-[0.15em] uppercase px-4 py-2 mb-10 shadow-[2px_2px_0px_0px_rgba(30,27,75,0.1)] bg-white">
                Application Drafting, Automated
              </div>
              
              <h1 className="text-6xl md:text-7xl font-bold tracking-tight text-slate-900 leading-[1.1] mb-6">
                Claim your <br/> rights in <span className="text-[#3b36e8]">plain <br/> language.</span>
              </h1>
              
              <p className="text-xl text-slate-600 mb-10 max-w-md leading-relaxed">
                No legal jargon. No expensive lawyers. Describe your civic issue like you're talking to a friend — our AI drafts a legally sound RTI application.
              </p>
              
              <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="bg-[#1e1b4b] hover:bg-[#2e2b5e] text-white font-semibold text-lg py-4 px-8 rounded-xl transition-all flex items-center gap-2 shadow-[0_8px_30px_rgb(0,0,0,0.12)] active:scale-95">
                Start Drafting Now <ArrowRight size={20} />
              </button>
              <div className="mt-6 text-sm text-slate-500 font-medium">
                Free to use · Takes about 2 minutes
              </div>
            </div>
            
            {/* Right Side: Graphic */}
            <div className="w-full lg:w-1/2 relative mt-20 lg:mt-0 flex justify-center lg:justify-end">
              <div className="relative w-full max-w-lg h-[450px]">
                {/* Yellow Card (You Type) */}
                <div className="absolute top-10 left-0 lg:left-4 w-4/5 bg-[#fffdf0] border border-[#fde68a] rounded-xl p-6 shadow-sm rotate-[-3deg] z-10">
                  <div className="text-[#b45309] text-[11px] font-bold uppercase tracking-widest mb-4">You Type</div>
                  <div className="text-[#334155] font-medium text-lg leading-relaxed">
                    "My road hasn't been repaired even though funds were sanctioned last year — why?"
                  </div>
                </div>
                
                {/* White Card (Drafted) */}
                <div className="absolute top-44 right-0 lg:-right-8 w-[95%] bg-white border border-slate-200 rounded-xl p-8 shadow-2xl z-20">
                  <div className="absolute -top-10 -right-10 w-[90px] h-[90px] rounded-full border-[3px] border-[#dc2626] text-[#dc2626] flex flex-col items-center justify-center rotate-[15deg] bg-white shadow-sm z-30">
                    <span className="text-[9px] font-extrabold tracking-widest uppercase mb-0.5">Drafted</span>
                    <span className="text-xs font-bold font-mono">RTI-01</span>
                  </div>
                  <div className="font-mono text-[13px] text-slate-700 space-y-5 leading-relaxed">
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
          </div>

          {/* Stats Section */}
          <div className="w-full bg-white border-y border-slate-200 py-16 relative z-10">
            <div className="max-w-5xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12 text-center divide-y md:divide-y-0 md:divide-x divide-slate-200">
              <div className="flex flex-col items-center justify-center pt-6 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="text-[#3b36e8]" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">42,500<span className="text-[#3b36e8]">+</span></span>
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Cases Drafted & Solved</div>
              </div>
              
              <div className="flex flex-col items-center justify-center pt-8 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="text-[#3b36e8]" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">94<span className="text-[#3b36e8]">%</span></span>
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Resolution Success Rate</div>
              </div>
              
              <div className="flex flex-col items-center justify-center pt-8 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="text-[#3b36e8]" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">4.9<span className="text-[#3b36e8]">/5</span></span>
                </div>
                <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mt-1">Citizen Satisfaction Rating</div>
              </div>
            </div>
          </div>

          {/* Reviews Section */}
          <div className="w-full bg-[#1e1b4b] py-24">
            <div className="max-w-6xl mx-auto px-6">
              <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Trusted by Citizens Across India</h2>
                <p className="text-indigo-200 font-medium text-lg max-w-2xl mx-auto">See how CivicAction is helping ordinary people cut through red tape and demand accountability.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {name: "Priya S.", loc: "Bangalore", review: "I spent 6 months trying to get my streetlights fixed. I drafted one RTI using CivicAction and they were repaired in 14 days. Absolutely incredible tool."},
                  {name: "Rajesh K.", loc: "Delhi", review: "The Rights Navigator is a gamechanger. When my landlord tried to evict me illegally, I showed him the exact legal clauses the AI gave me. He backed down immediately."},
                  {name: "Anil M.", loc: "Mumbai", review: "I had no idea I was eligible for the housing scheme until I used this app. It guided me step-by-step and even drafted the application for me. Highly recommended!"}
                ].map((r, i) => (
                  <div key={i} className="bg-white/5 p-8 rounded-2xl border border-white/10 backdrop-blur-sm flex flex-col justify-between hover:border-[#3b36e8] transition-all hover:-translate-y-1 shadow-lg">
                    <div className="text-indigo-100 font-medium leading-relaxed mb-8">"{r.review}"</div>
                    <div className="flex items-center gap-4 border-t border-white/10 pt-6">
                      <div className="w-12 h-12 rounded-full bg-indigo-900 border border-[#3b36e8] flex items-center justify-center text-white font-bold text-lg">{r.name[0]}</div>
                      <div>
                        <div className="font-bold text-white text-base">{r.name}</div>
                        <div className="text-xs font-semibold text-indigo-300 tracking-wide uppercase mt-0.5">{r.loc}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <footer className="w-full bg-[#0f0e26] py-12 border-t border-[#1e1b4b]">
            <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
              <div className="flex items-center gap-2 font-bold text-xl tracking-tight text-white mb-4 md:mb-0">
                <Scale size={20} className="text-[#3b36e8]"/> CivicAction
              </div>
              <div className="text-indigo-200/50 text-sm font-medium">
                &copy; {new Date().getFullYear()} CivicAction. Empowering Citizens.
              </div>
            </div>
          </footer>
        </main>
      </div>
    );
  }

"""

text = text[:start_idx] + new_landing + text[end_idx:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("UI Redesign complete!")
