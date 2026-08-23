import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new View 2
new_view_2 = """  // --- VIEW 2: APPLICATION INTERFACE ---
  return (
    <div className="h-screen w-full bg-slate-50 text-slate-900 font-sans flex flex-col overflow-hidden fixed inset-0 text-left">
      
      {/* Top Navbar */}
      <nav className="h-14 flex items-center justify-between px-5 bg-white border-b border-slate-200 shrink-0 z-20">
        <div className="flex items-center gap-6">
          <div 
            onClick={() => setCurrentView('landing')}
            className="flex items-center gap-2 font-bold text-base tracking-tight cursor-pointer hover:text-indigo-600 transition-colors"
          >
            <div className="w-6 h-6 bg-indigo-600 text-white rounded-md flex items-center justify-center">
              <Scale size={14} />
            </div>
            <span>CivicAction</span>
          </div>
          
          <div className="hidden md:flex items-center gap-1 ml-4 border-l border-slate-200 pl-4">
            <button 
              onClick={() => setActiveTab('rti')}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'rti' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}
            >
              RTI Drafter
            </button>
            <button 
              onClick={() => setActiveTab('rights')}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'rights' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}
            >
              Rights Navigator
            </button>
            <button 
              onClick={() => setActiveTab('schemes')}
              className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'schemes' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}
            >
              Schemes
            </button>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button 
            onClick={resetApp}
            className="hidden md:flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-indigo-600 transition-colors"
          >
            <PlusCircle size={14} /> Reset
          </button>
          <div className="h-4 w-px bg-slate-200"></div>
          <div className="flex items-center gap-2 text-sm font-medium text-slate-600">
            <Smartphone size={14} className="text-slate-400" />
            <span>+91 {userMobile}</span>
          </div>
        </div>
      </nav>

      {/* Main App Workspace */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden w-full relative bg-slate-50">
        
        {/* LEFT COLUMN: Input */}
        <div className="w-full lg:w-[40%] h-full flex flex-col bg-white border-r border-slate-200 z-10 overflow-y-auto">
          
          {activeTab === 'rti' && (
            <>
              <div className="px-6 pt-6 pb-4 border-b border-slate-100">
                <h1 className="text-lg font-semibold text-slate-900">Application Details</h1>
                <p className="text-slate-500 text-xs mt-1">Describe your issue. Our AI will handle the legal formatting.</p>
              </div>

              <div className="flex-1 flex flex-col p-6">
                <div className="mb-3">
                  <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Issue Description</label>
                </div>
                <div className="relative flex-1 min-h-[250px] mb-6">
                  <textarea
                    className="w-full h-full p-4 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none resize-none text-slate-800 placeholder-slate-400 transition-all text-sm leading-relaxed shadow-sm scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-transparent"
                    placeholder="E.g., The streetlights outside my college have been broken for two months..."
                    value={complaint}
                    onChange={(e) => setComplaint(e.target.value)}
                    disabled={appState === 'loading'}
                  />
                  <div className="absolute bottom-3 right-3 flex items-center">
                    {complaint.length > 0 && complaint.length < 20 ? (
                      <span className="text-[10px] font-medium text-amber-600">Too short</span>
                    ) : complaint.length >= 20 ? (
                      <span className="text-[10px] font-medium text-emerald-600 flex items-center gap-1"><CheckCircle size={10}/> Ready</span>
                    ) : null}
                  </div>
                </div>

                <div className="mb-6">
                  {!showAttachment ? (
                    <button 
                      onClick={() => setShowAttachment(true)}
                      className="flex items-center gap-1.5 text-xs font-medium text-slate-500 hover:text-indigo-600 transition-colors"
                    >
                      <Paperclip size={14} /> Attach supporting documents (Optional)
                    </button>
                  ) : (
                    <div className="p-4 border border-dashed border-slate-300 rounded-lg bg-slate-50 hover:bg-indigo-50/50 hover:border-indigo-300 transition-colors cursor-pointer" onClick={() => fileInputRef.current?.click()}>
                      <div className="flex justify-between items-center mb-1">
                        <div className="flex items-center gap-1.5 text-slate-700 font-medium text-xs">
                          <UploadCloud size={14} /> Upload Document
                        </div>
                        <button onClick={(e) => { e.stopPropagation(); setShowAttachment(false); setFile(null); }} className="text-[10px] font-semibold text-slate-400 hover:text-slate-900">Close</button>
                      </div>
                      <input type="file" className="hidden" ref={fileInputRef} onChange={(e) => setFile(e.target.files[0])} />
                      <p className="text-[10px] text-slate-500">{file ? <span className="text-indigo-600 font-medium">{file.name}</span> : 'Click to browse'}</p>
                    </div>
                  )}
                </div>

                <button 
                  onClick={generateRTI}
                  disabled={complaint.length < 20 || appState === 'loading'}
                  className="mt-auto w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 text-white font-medium text-sm py-3 rounded-lg transition-all shadow-sm"
                >
                  {appState === 'loading' ? <Loader2 className="animate-spin" size={16} /> : <Sparkles size={16} />}
                  {appState === 'loading' ? 'Generating Draft...' : 'Generate Legal Draft'}
                </button>
              </div>
            </>
          )}

          {activeTab === 'rights' && (
            <>
              <div className="px-6 pt-6 pb-4 border-b border-slate-100">
                <h1 className="text-lg font-semibold text-slate-900">Rights Navigator</h1>
                <p className="text-slate-500 text-xs mt-1">Describe a legal or civic situation to learn your rights.</p>
              </div>
              <div className="flex-1 flex flex-col p-6">
                <div className="relative flex-1 min-h-[250px] mb-6">
                  <textarea
                    className="w-full h-full p-4 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none resize-none text-slate-800 placeholder-slate-400 transition-all text-sm leading-relaxed shadow-sm scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-transparent"
                    placeholder="E.g., I was fired from my job without any prior notice or compensation..."
                    value={rightsSituation}
                    onChange={(e) => setRightsSituation(e.target.value)}
                    disabled={rightsState === 'loading'}
                  />
                </div>
                <button 
                  onClick={generateRights}
                  disabled={rightsSituation.length < 10 || rightsState === 'loading'}
                  className="mt-auto w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 text-white font-medium text-sm py-3 rounded-lg transition-all shadow-sm"
                >
                  {rightsState === 'loading' ? <Loader2 className="animate-spin" size={16} /> : <Sparkles size={16} />}
                  {rightsState === 'loading' ? 'Analyzing...' : 'Discover My Rights'}
                </button>
              </div>
            </>
          )}

          {activeTab === 'schemes' && (
            <>
              <div className="px-6 pt-6 pb-4 border-b border-slate-100">
                <h1 className="text-lg font-semibold text-slate-900">Scheme Eligibility</h1>
                <p className="text-slate-500 text-xs mt-1">Provide your profile to find applicable government schemes.</p>
              </div>
              <div className="flex-1 flex flex-col p-6 space-y-4">
                 <div>
                   <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Age</label>
                   <input type="number" value={schemeProfile.age} onChange={(e) => setSchemeProfile({...schemeProfile, age: parseInt(e.target.value) || ''})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" />
                 </div>
                 <div>
                   <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Gender</label>
                   <select value={schemeProfile.gender} onChange={(e) => setSchemeProfile({...schemeProfile, gender: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none">
                     <option>Male</option><option>Female</option><option>Other</option>
                   </select>
                 </div>
                 <div>
                   <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Annual Income (INR)</label>
                   <input type="text" value={schemeProfile.income} onChange={(e) => setSchemeProfile({...schemeProfile, income: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" />
                 </div>
                 <div>
                   <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Occupation</label>
                   <input type="text" value={schemeProfile.occupation} onChange={(e) => setSchemeProfile({...schemeProfile, occupation: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" />
                 </div>
                 <div>
                   <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">State</label>
                   <input type="text" value={schemeProfile.state} onChange={(e) => setSchemeProfile({...schemeProfile, state: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" />
                 </div>

                <button 
                  onClick={checkSchemes}
                  disabled={schemeState === 'loading'}
                  className="mt-6 w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 disabled:text-slate-400 text-white font-medium text-sm py-3 rounded-lg transition-all shadow-sm"
                >
                  {schemeState === 'loading' ? <Loader2 className="animate-spin" size={16} /> : <Sparkles size={16} />}
                  {schemeState === 'loading' ? 'Checking...' : 'Find Schemes'}
                </button>
              </div>
            </>
          )}

        </div>

        {/* RIGHT COLUMN: Output */}
        <div className="w-full lg:w-[60%] h-full flex flex-col bg-slate-50 overflow-y-auto">
          
          {activeTab === 'rti' && (
            <>
              {appState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-10 animate-in fade-in duration-500">
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300">
                    <FileText size={28} strokeWidth={1.5} />
                  </div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">No Draft Generated Yet</h2>
                  <p className="text-slate-500 text-sm max-w-sm">
                    Fill out the details on the left, and your formatted RTI application will appear here.
                  </p>
                </div>
              )}

              {appState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in duration-300 max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600">
                    <Loader2 className="animate-spin" size={18} />
                    <span className="font-medium text-sm">{loadingMessage}</span>
                  </div>
                  <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex-1 animate-pulse">
                    <div className="h-3 bg-slate-200 rounded w-1/4 mb-8"></div>
                    <div className="h-6 bg-slate-200 rounded w-3/4 mb-6"></div>
                    <div className="space-y-3">
                      <div className="h-2 bg-slate-100 rounded w-full"></div>
                      <div className="h-2 bg-slate-100 rounded w-full"></div>
                      <div className="h-2 bg-slate-100 rounded w-5/6"></div>
                      <div className="h-2 bg-slate-100 rounded w-full"></div>
                    </div>
                  </div>
                </div>
              )}

              {appState === 'result' && (
                <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto w-full">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900">
                      <CheckCircle className="text-emerald-500" size={20} /> Draft Ready for Review
                    </h2>
                    <div className="flex gap-2">
                      <button className="flex items-center justify-center gap-1.5 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-medium text-sm py-1.5 px-3 rounded-md transition-colors shadow-sm">
                        <Copy size={14} /> Copy
                      </button>
                      <button 
                        onClick={handleDownload}
                        className="flex items-center justify-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm py-1.5 px-4 rounded-md transition-colors shadow-sm"
                      >
                        <Download size={14} /> Download PDF
                      </button>
                    </div>
                  </div>
                  
                  <div className="bg-white p-6 lg:p-8 rounded-xl border border-slate-200 shadow-sm flex-1 flex flex-col mb-2 overflow-hidden">
                    <div className="mb-5 group">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Addressed To</label>
                      <input 
                        type="text"
                        value={docData.department}
                        onChange={(e) => setDocData({...docData, department: e.target.value})}
                        className="w-full bg-transparent text-slate-900 font-medium text-base border-b border-transparent hover:border-slate-200 focus:border-indigo-500 focus:outline-none pb-1 transition-colors"
                      />
                    </div>

                    <div className="mb-5 group">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Subject</label>
                      <input 
                        type="text"
                        value={docData.subject}
                        onChange={(e) => setDocData({...docData, subject: e.target.value})}
                        className="w-full bg-transparent text-slate-900 font-medium text-sm border-b border-transparent hover:border-slate-200 focus:border-indigo-500 focus:outline-none pb-1 transition-colors"
                      />
                    </div>

                    <div className="flex-1 flex flex-col group">
                      <label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Application Body</label>
                      <textarea 
                        value={docData.body}
                        onChange={(e) => setDocData({...docData, body: e.target.value})}
                        className="w-full flex-1 bg-transparent text-slate-800 border border-transparent hover:border-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:bg-white rounded-md focus:outline-none resize-none leading-relaxed transition-all text-sm p-2 -ml-2 scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-transparent"
                      />
                    </div>
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === 'rights' && (
            <>
              {rightsState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-10 animate-in fade-in duration-500">
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300">
                    <Scale size={28} strokeWidth={1.5} />
                  </div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">Know Your Rights</h2>
                  <p className="text-slate-500 text-sm max-w-sm">
                    Enter a situation on the left to see what legal rights apply.
                  </p>
                </div>
              )}
              {rightsState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in duration-300 max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600">
                    <Loader2 className="animate-spin" size={18} />
                    <span className="font-medium text-sm">{loadingMessage}</span>
                  </div>
                </div>
              )}
              {rightsState === 'result' && rightsData && (
                 <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto w-full">
                   <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900 mb-4">
                     <Scale className="text-indigo-600" size={20} /> Applicable Rights
                   </h2>
                   <div className="space-y-4">
                     {rightsData.applicable_rights?.map((right, idx) => (
                       <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                         <h3 className="font-bold text-slate-900">{right.right_name}</h3>
                         <p className="text-xs text-indigo-600 font-semibold mt-1">{right.legal_basis}</p>
                         <p className="text-sm text-slate-600 mt-2">{right.description}</p>
                       </div>
                     ))}
                   </div>
                   <div className="mt-6 bg-indigo-50 border border-indigo-100 p-5 rounded-xl">
                     <h3 className="text-xs font-bold text-indigo-800 uppercase tracking-wider mb-2">Recommended Next Step</h3>
                     <p className="text-sm text-indigo-900">{rightsData.next_steps}</p>
                   </div>
                 </div>
              )}
            </>
          )}

          {activeTab === 'schemes' && (
            <>
              {schemeState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-10 animate-in fade-in duration-500">
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300">
                    <AlertCircle size={28} strokeWidth={1.5} />
                  </div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">Discover Schemes</h2>
                  <p className="text-slate-500 text-sm max-w-sm">
                    Enter your profile details to see which government schemes you qualify for.
                  </p>
                </div>
              )}
              {schemeState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in duration-300 max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600">
                    <Loader2 className="animate-spin" size={18} />
                    <span className="font-medium text-sm">{loadingMessage}</span>
                  </div>
                </div>
              )}
              {schemeState === 'result' && schemeData && (
                 <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto w-full">
                   <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900 mb-4">
                     <CheckCircle className="text-emerald-500" size={20} /> Eligible Schemes
                   </h2>
                   <div className="space-y-4">
                     {schemeData.eligible_schemes?.map((scheme, idx) => (
                       <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                         <h3 className="font-bold text-slate-900 text-base">{scheme.scheme_name}</h3>
                         <div className="mt-3 space-y-2">
                           <div><span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Benefits</span><p className="text-sm text-slate-700">{scheme.benefits}</p></div>
                           <div><span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Why You Qualify</span><p className="text-sm text-slate-700">{scheme.eligibility_criteria}</p></div>
                           {scheme.application_link && (
                             <div className="pt-2">
                               <a href={scheme.application_link} target="_blank" rel="noreferrer" className="text-sm font-semibold text-indigo-600 hover:underline">{scheme.application_link}</a>
                             </div>
                           )}
                         </div>
                       </div>
                     ))}
                   </div>
                 </div>
              )}
            </>
          )}

        </div>
      </div>
    </div>
  );
}
export default App;
"""

new_content = re.sub(r'  // --- VIEW 2: APPLICATION INTERFACE ---.*', new_view_2, content, flags=re.DOTALL)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Done patching App.jsx")
