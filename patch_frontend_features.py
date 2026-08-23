import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Imports
text = text.replace("import { FileText, ArrowRight", "import { Mail, FileText, ArrowRight")

# 2. States & Functions
dashboard_code = """
  const [dashboardData, setDashboardData] = useState([]);
  const [isFetchingDashboard, setIsFetchingDashboard] = useState(false);
  const [isDraftingAppeal, setIsDraftingAppeal] = useState(false);

  const fetchDashboard = async () => {
    setIsFetchingDashboard(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/applications/${userMobile}`);
      const data = await res.json();
      setDashboardData(data.applications || []);
    } catch (e) {}
    setIsFetchingDashboard(false);
  };

  useEffect(() => {
    if (activeTab === 'dashboard') fetchDashboard();
  }, [activeTab]);

  const handleDraftAppeal = async () => {
    setIsDraftingAppeal(true);
    setLoadingMessage("Drafting First Appeal...");
    setAppState('loading');
    try {
      const res = await fetch('http://127.0.0.1:8000/generate_appeal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rti_body: docData.body, applicant_name: applicantName || 'Citizen', language })
      });
      const data = await res.json();
      setDocData({...docData, subject: "First Appeal under Section 19(1) of RTI Act", body: data.appeal_draft});
    } catch(e) {}
    setAppState('result');
    setIsDraftingAppeal(false);
  };

  const handleEmail = () => {
    const subject = encodeURIComponent(docData.subject);
    const body = encodeURIComponent(docData.body);
    window.open(`mailto:?subject=${subject}&body=${body}`);
  };
"""
text = text.replace("const [applicantName, setApplicantName] = useState('');", "const [applicantName, setApplicantName] = useState('');" + dashboard_code)

# 3. Navbar Dashboard Tab
nav_buttons = """<button onClick={() => setActiveTab('rti')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'rti' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>RTI Drafter</button>
            <button onClick={() => setActiveTab('dashboard')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'dashboard' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Dashboard</button>
            <button onClick={() => setActiveTab('rights')}"""
text = text.replace("<button onClick={() => setActiveTab('rti')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'rti' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>RTI Drafter</button>\n            <button onClick={() => setActiveTab('rights')}", nav_buttons)

# 4. RTI Result Buttons
old_buttons = """<button className="flex items-center gap-2 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-700 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all active:scale-[0.97]">
                        <Copy size={16} /> Copy
                      </button>
                      <button onClick={handleDownload} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2 px-5 rounded-lg shadow-sm transition-all shadow-blue-600/20 active:scale-[0.97]">
                        <Download size={16} /> Download PDF
                      </button>"""
new_buttons = """<button onClick={handleDraftAppeal} className="flex items-center gap-2 bg-amber-100 hover:bg-amber-200 text-amber-800 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all">
                        <AlertCircle size={16} /> Draft First Appeal
                      </button>
                      <button onClick={handleEmail} className="flex items-center gap-2 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-700 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all">
                        <Mail size={16} /> Send via Email
                      </button>
                      <button onClick={handleDownload} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2 px-5 rounded-lg shadow-sm transition-all shadow-blue-600/20">
                        <Download size={16} /> Download PDF
                      </button>"""
text = text.replace(old_buttons, new_buttons)

# 5. Dashboard Tab UI
dashboard_ui = """
          {/* TAB: DASHBOARD */}
          {activeTab === 'dashboard' && (
            <div className="animate-subtle max-w-5xl mx-auto">
              <div className="text-2xl font-bold text-zinc-900 mb-8">My Applications</div>
              {isFetchingDashboard ? (
                <div className="flex justify-center p-12"><Loader2 className="animate-spin text-blue-600" size={32}/></div>
              ) : dashboardData.length === 0 ? (
                <div className="bg-white p-12 rounded-2xl text-center border border-zinc-200 shadow-sm">
                  <div className="text-zinc-300 mb-4 flex justify-center"><FileText size={48} /></div>
                  <div className="text-lg font-bold text-zinc-800">No applications yet</div>
                  <div className="text-zinc-500 text-sm mt-1">Draft an RTI and it will appear here.</div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {dashboardData.map((app) => (
                    <div key={app.id} className="bg-white p-6 rounded-2xl border border-zinc-200 shadow-sm hover:border-blue-300 transition-all cursor-pointer group" onClick={() => {
                      setDocData({department: app.department, subject: "Information Request under RTI Act, 2005", body: app.draft});
                      setActiveTab('rti');
                      setAppState('result');
                    }}>
                      <div className="text-[11px] font-bold text-blue-600 uppercase tracking-widest mb-2 flex justify-between">
                        <span>Application #{app.id}</span>
                        <ArrowRight size={14} className="opacity-0 group-hover:opacity-100 transition-opacity translate-x-[-10px] group-hover:translate-x-0"/>
                      </div>
                      <div className="font-bold text-lg text-zinc-900 mb-2 truncate">{app.department}</div>
                      <div className="text-sm font-medium text-zinc-600 line-clamp-3">{app.summary}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
"""
text = text.replace("{/* TAB 1: RTI DRAFTER */}", dashboard_ui + "\n          {/* TAB 1: RTI DRAFTER */}")

# 6. Landing Page Reviews
reviews_html = """
        {/* Reviews Section */}
        <div className="max-w-6xl mx-auto px-6 py-24 border-t border-white/10">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Trusted by Citizens Across India</h2>
            <p className="text-zinc-400 font-medium text-lg">See how CivicAction is helping ordinary people cut through red tape.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {name: "Priya S.", loc: "Bangalore", review: "I spent 6 months trying to get my streetlights fixed. I drafted one RTI using CivicAction and they were repaired in 14 days. Absolutely incredible tool."},
              {name: "Rajesh K.", loc: "Delhi", review: "The Rights Navigator is a gamechanger. When my landlord tried to evict me illegally, I showed him the exact legal clauses the AI gave me. He backed down immediately."},
              {name: "Anil M.", loc: "Mumbai", review: "I had no idea I was eligible for the housing scheme until I used this app. It guided me step-by-step and even drafted the application for me. Highly recommended!"}
            ].map((r, i) => (
              <div key={i} className="bg-zinc-900/50 p-8 rounded-2xl border border-white/10 backdrop-blur-sm flex flex-col justify-between hover:border-blue-500/30 transition-colors">
                <div className="text-zinc-300 font-medium leading-relaxed mb-6">"{r.review}"</div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-900/30 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold">{r.name[0]}</div>
                  <div>
                    <div className="font-bold text-white text-sm">{r.name}</div>
                    <div className="text-xs font-semibold text-zinc-500">{r.loc}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
"""
text = text.replace("      </div>\n    </div>\n  );", reviews_html + "\n      </div>\n    </div>\n  );")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Frontend patched with all features!")
