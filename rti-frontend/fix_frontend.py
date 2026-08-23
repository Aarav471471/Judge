import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove any existing summarizer views. 
# They are enclosed in `{activeTab === 'summarizer' && (` and `)}`
# Wait, parsing this with regex is tricky. Let's just restore from my `retheme.py` baseline and apply the patch correctly.

with open(r'c:\oosc\Judge\rti-frontend\retheme.py', 'r', encoding='utf-8') as f:
    retheme_code = f.read()

# Run retheme to reset App.jsx
import subprocess
subprocess.run(['python', r'c:\oosc\Judge\rti-frontend\retheme.py'], check=True)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State Injection
states_injection = """  // --- Summarizer State ---
  const [summaryFile, setSummaryFile] = useState(null);
  const [summaryState, setSummaryState] = useState('empty');
  const [summaryData, setSummaryData] = useState(null);

  const handleSummarize = async () => {
    if (!summaryFile) return;
    setSummaryState('loading');
    setLoadingMessage('Analyzing document...');
    
    const formData = new FormData();
    formData.append('file', summaryFile);
    formData.append('language', language);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/summarize-document', {
        method: 'POST',
        body: formData
      });
      if (!res.ok) throw new Error("Failed to summarize");
      const data = await res.json();
      setSummaryData(data);
      setSummaryState('result');
    } catch (error) {
      alert("Failed to analyze document.");
      setSummaryState('empty');
    }
  };
"""
content = content.replace("const handleSendOTP = async () => {", states_injection + "\n  const handleSendOTP = async () => {")

# 2. Add resetApp additions
content = content.replace("setInterviewAnswers({});", "setInterviewAnswers({});\n    setSummaryState('empty');\n    setSummaryFile(null);")

# 3. Add Nav button
nav_btn = """<button onClick={() => setActiveTab('schemes')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'schemes' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Schemes</button>
            <button onClick={() => setActiveTab('summarizer')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'summarizer' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Doc Summarizer</button>"""
content = content.replace("""<button onClick={() => setActiveTab('schemes')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'schemes' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Schemes</button>""", nav_btn)

# 4. Add Left View
left_view = """
          {activeTab === 'summarizer' && (
            <div className="flex flex-col h-full animate-subtle">
              <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="text-2xl font-bold text-zinc-900 tracking-tight">Document Summarizer</div>
                <div className="text-zinc-500 text-sm mt-1.5 font-medium">Upload any government notice, FIR, or legal paper to get a clear summary.</div>
              </div>
              <div className="flex-1 flex flex-col p-8 bg-zinc-50/30 justify-center">
                 
                 <div 
                   className="border-2 border-dashed border-zinc-300 rounded-2xl p-10 flex flex-col items-center justify-center bg-white hover:bg-zinc-50 hover:border-blue-400 transition-all cursor-pointer group"
                   onClick={() => document.getElementById('file-upload').click()}
                 >
                   <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                     <UploadCloud size={32} />
                   </div>
                   <div className="text-base font-bold text-zinc-800 mb-2">Click to Upload Document</div>
                   <div className="text-xs font-medium text-zinc-500 mb-6">Supports PDF, JPG, PNG</div>
                   
                   {summaryFile ? (
                     <div className="px-4 py-2 bg-blue-50 text-blue-700 rounded-lg text-sm font-bold flex items-center gap-2">
                       <FileText size={16} /> {summaryFile.name}
                     </div>
                   ) : null}
                   
                   <input 
                     id="file-upload" 
                     type="file" 
                     className="hidden" 
                     accept=".pdf,image/*"
                     onChange={(e) => setSummaryFile(e.target.files[0])}
                   />
                 </div>

                <button 
                  onClick={handleSummarize} 
                  disabled={!summaryFile || summaryState === 'loading'} 
                  className="mt-8 w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 disabled:border-zinc-200 border border-transparent text-white font-semibold text-base py-3.5 rounded-xl transition-all shadow-md active:scale-[0.98]"
                >
                  {summaryState === 'loading' ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                  {summaryState === 'loading' ? 'Analyzing Document...' : 'Generate Summary'}
                </button>
              </div>
            </div>
          )}
"""
# Insert into left column
left_col_marker = "{/* LEFT COLUMN: Input */}"
content = content.replace(left_col_marker, left_col_marker + left_view)

# 5. Add Right View
right_view = """
          {activeTab === 'summarizer' && (
            <div className="h-full flex flex-col relative z-10">
              {summaryState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-12 animate-subtle">
                  <div className="w-20 h-20 bg-white rounded-2xl shadow-sm border border-zinc-200 flex items-center justify-center mb-6 text-zinc-300">
                    <FileText size={36} strokeWidth={1.5} />
                  </div>
                  <div className="text-xl font-bold text-zinc-900 mb-2">Document Analysis</div>
                  <div className="text-zinc-500 text-base max-w-sm leading-relaxed">
                    Upload a file on the left, and our AI will read it and break it down into simple terms.
                  </div>
                </div>
              )}
              {summaryState === 'loading' && (
                <div className="flex flex-col h-full p-8 lg:p-12 animate-subtle max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-3 mb-6 text-blue-600">
                    <Loader2 className="animate-spin" size={20} />
                    <span className="font-semibold text-sm tracking-wide">{loadingMessage}</span>
                  </div>
                </div>
              )}
              {summaryState === 'result' && summaryData && (
                 <div className="flex flex-col h-full p-6 lg:p-10 animate-subtle max-w-4xl mx-auto w-full hide-scroll overflow-y-auto">
                   <div className="text-xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-8 h-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
                        <FileText size={18} strokeWidth={2.5} />
                      </div>
                      Analysis Complete
                    </div>
                   
                   <div className="space-y-6">
                     <div className="bg-white p-7 rounded-2xl border border-zinc-200 shadow-sm relative overflow-hidden group">
                       <div className="absolute left-0 top-0 bottom-0 w-1 bg-indigo-500"></div>
                       <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3">Document Type</div>
                       <div className="font-bold text-xl text-zinc-900">{summaryData.document_type}</div>
                     </div>
                     
                     <div className="bg-white p-7 rounded-2xl border border-zinc-200 shadow-sm">
                       <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3 flex items-center gap-1.5"><Sparkles size={12} className="text-indigo-500"/> Summary</div>
                       <div className="text-base text-zinc-700 leading-relaxed font-medium whitespace-pre-wrap">{summaryData.summary}</div>
                     </div>
                     
                     <div className="mt-8 bg-zinc-900 text-white p-8 rounded-2xl shadow-xl shadow-zinc-900/10 relative overflow-hidden">
                       <div className="absolute -right-4 -bottom-4 text-zinc-800 opacity-50 pointer-events-none"><AlertCircle size={100}/></div>
                       <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3 relative z-10">Action Required</div>
                       <div className="text-lg font-medium leading-relaxed relative z-10">{summaryData.action_required}</div>
                     </div>
                   </div>
                 </div>
              )}
            </div>
          )}
"""
# Insert into right column
right_col_marker = "{/* RIGHT COLUMN: Output */}"
content = content.replace(right_col_marker, right_col_marker + right_view)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print("Frontend successfully repaired and patched")
