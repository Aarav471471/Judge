import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# I am going to nuke everything from `{/* Main Workspace Workspace */}` to the end of the file.
# Then reconstruct it perfectly to avoid any more parsing errors.
# We have `retheme.py` which contains the perfect layout, I just need to add the summarizer pieces inside the correct columns.

with open(r'c:\oosc\Judge\rti-frontend\retheme.py', 'r', encoding='utf-8') as f:
    retheme_code = f.read()
    
# Extract new_view_2 from retheme.py
import ast
# To avoid parsing python AST, I will just grab the string manually from retheme.py
start_str = 'new_view_2 = """  // --- VIEW 2: APPLICATION INTERFACE ---'
end_str = '"""\n\nnew_content = re.sub('
start_idx = retheme_code.find(start_str) + len('new_view_2 = """')
end_idx = retheme_code.find(end_str)
clean_view_2 = retheme_code[start_idx:end_idx]

# I will inject the Summarizer pieces into clean_view_2

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
                   <div className="text-xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8 shrink-0">
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

# Insert left view INSIDE the left column container
clean_view_2 = clean_view_2.replace(
    "{/* LEFT COLUMN: Input */}\n        <div className=\"w-full lg:w-[45%] xl:w-[40%] h-full flex flex-col bg-white border-r border-zinc-200/80 z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)] hide-scroll overflow-y-auto\">",
    "{/* LEFT COLUMN: Input */}\n        <div className=\"w-full lg:w-[45%] xl:w-[40%] h-full flex flex-col bg-white border-r border-zinc-200/80 z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)] hide-scroll overflow-y-auto\">\n" + left_view
)

# Insert right view INSIDE the right column container
clean_view_2 = clean_view_2.replace(
    "<div className=\"absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none mix-blend-overlay\"></div>",
    "<div className=\"absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none mix-blend-overlay\"></div>\n" + right_view
)

# Add nav button back
nav_btn = """<button onClick={() => setActiveTab('schemes')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'schemes' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Schemes</button>
            <button onClick={() => setActiveTab('summarizer')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'summarizer' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Doc Summarizer</button>"""
clean_view_2 = clean_view_2.replace("""<button onClick={() => setActiveTab('schemes')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'schemes' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Schemes</button>""", nav_btn)

# Now, find where `VIEW 2` starts in App.jsx and replace everything after it.
start_view_2_idx = text.find("  // --- VIEW 2: APPLICATION INTERFACE ---")
final_app_jsx = text[:start_view_2_idx] + clean_view_2

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(final_app_jsx)

print("Nuked layout and rebuilt it perfectly.")
