import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# I will replace the entire `if (currentView === 'landing')` block up to `// --- VIEW 2`
start_marker = "if (currentView === 'landing') {"
end_marker = "  // --- VIEW 2: APPLICATION INTERFACE ---"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

new_landing = """if (currentView === 'landing') {
    return (
      <div className="min-h-screen w-full bg-slate-50 text-slate-900 font-sans flex flex-col selection:bg-indigo-100 selection:text-indigo-900">
        <nav className="w-full flex items-center justify-between px-8 py-4 bg-white/80 backdrop-blur-md border-b border-slate-200/50 fixed top-0 z-50 transition-all">
          <div className="flex items-center gap-3 font-bold text-xl tracking-tight text-slate-900 cursor-pointer">
            <div className="w-10 h-10 bg-indigo-600 text-white rounded-xl flex items-center justify-center shadow-sm"><Scale size={20} /></div>
            <div className="flex flex-col justify-center leading-tight"><span>Civic<span className="text-indigo-600">Action</span></span></div>
          </div>
          <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="bg-slate-900 hover:bg-indigo-600 text-white font-semibold py-2.5 px-6 rounded-full transition-all duration-300 shadow-md">
            {isAuthenticated ? 'Go to Dashboard' : 'Sign In'}
          </button>
        </nav>
        
        <main className="flex-1 w-full flex flex-col pt-16">
          {/* Hero Section */}
          <div className="relative w-full flex flex-col items-center justify-center min-h-[85vh] py-20 px-4 overflow-hidden">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-100 via-slate-50 to-slate-50 opacity-70 pointer-events-none"></div>
            <div className="text-center px-6 max-w-5xl mx-auto relative z-10">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-indigo-100 shadow-sm text-indigo-700 font-bold text-xs uppercase tracking-widest mb-8">
                <Sparkles size={14} className="text-indigo-500" /> AI-Powered Legal Drafting
              </div>
              <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 leading-[1.1] text-slate-900">
                Claim your rights in <br className="hidden md:block" />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-500">Plain Language.</span>
              </h1>
              <p className="text-lg md:text-xl text-slate-600 mb-12 max-w-2xl mx-auto leading-relaxed">
                No legal jargon. No expensive lawyers. Describe your civic issue like you're talking to a friend, and our AI instantly formats a legally sound RTI application.
              </p>
              <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="group text-lg bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-10 rounded-full transition-all flex items-center gap-2 mx-auto shadow-xl hover:shadow-indigo-300 active:scale-95">
                Start Drafting Now <ArrowRight size={20} />
              </button>
            </div>
          </div>

          {/* Reviews Section */}
          <div className="w-full bg-zinc-950 py-24">
            <div className="max-w-6xl mx-auto px-6">
              <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Trusted by Citizens Across India</h2>
                <p className="text-zinc-400 font-medium text-lg max-w-2xl mx-auto">See how CivicAction is helping ordinary people cut through red tape and demand accountability.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {[
                  {name: "Priya S.", loc: "Bangalore", review: "I spent 6 months trying to get my streetlights fixed. I drafted one RTI using CivicAction and they were repaired in 14 days. Absolutely incredible tool."},
                  {name: "Rajesh K.", loc: "Delhi", review: "The Rights Navigator is a gamechanger. When my landlord tried to evict me illegally, I showed him the exact legal clauses the AI gave me. He backed down immediately."},
                  {name: "Anil M.", loc: "Mumbai", review: "I had no idea I was eligible for the housing scheme until I used this app. It guided me step-by-step and even drafted the application for me. Highly recommended!"}
                ].map((r, i) => (
                  <div key={i} className="bg-zinc-900/80 p-8 rounded-2xl border border-white/10 backdrop-blur-sm flex flex-col justify-between hover:border-indigo-500/30 transition-all hover:-translate-y-1 shadow-lg">
                    <div className="text-zinc-300 font-medium leading-relaxed mb-8">"{r.review}"</div>
                    <div className="flex items-center gap-4 border-t border-white/10 pt-6">
                      <div className="w-12 h-12 rounded-full bg-indigo-900/30 border border-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold text-lg">{r.name[0]}</div>
                      <div>
                        <div className="font-bold text-white text-base">{r.name}</div>
                        <div className="text-xs font-semibold text-zinc-500 tracking-wide uppercase mt-0.5">{r.loc}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <footer className="w-full bg-black py-8 border-t border-zinc-900">
            <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
              <div className="flex items-center gap-2 font-bold text-lg tracking-tight text-white mb-4 md:mb-0">
                <Scale size={18} className="text-indigo-500"/> CivicAction
              </div>
              <div className="text-zinc-600 text-sm font-medium">
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

print("Redesigned landing page installed.")
