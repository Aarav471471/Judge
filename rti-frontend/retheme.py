import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace everything from `// --- VIEW 2: APPLICATION INTERFACE ---` to the end.
new_view_2 = """  // --- VIEW 2: APPLICATION INTERFACE ---
  return (
    <div className="h-screen w-full bg-[#FAFAFA] text-zinc-900 font-sans flex flex-col overflow-hidden fixed inset-0 text-left selection:bg-blue-100 selection:text-blue-900">
      <style>{`
        /* Hide scrollbars for a cleaner look */
        .hide-scroll::-webkit-scrollbar { display: none; }
        .hide-scroll { -ms-overflow-style: none; scrollbar-width: none; }
        
        /* Smooth fade-in animations */
        @keyframes subtleFade { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        .animate-subtle { animation: subtleFade 0.4s ease-out forwards; }
      `}</style>

      {/* Top Navbar */}
      <nav className="h-16 flex items-center justify-between px-6 bg-white/80 backdrop-blur-md border-b border-zinc-200/80 shrink-0 z-20">
        <div className="flex items-center gap-8">
          <div onClick={() => setCurrentView('landing')} className="flex items-center gap-2.5 font-bold text-lg tracking-tight cursor-pointer group">
            <div className="w-8 h-8 bg-zinc-900 text-white rounded-lg flex items-center justify-center shadow-md group-hover:bg-blue-600 transition-colors"><Scale size={16} /></div>
            <span className="text-zinc-900 group-hover:text-blue-600 transition-colors">CivicAction</span>
          </div>
          
          <div className="hidden md:flex items-center gap-2 bg-zinc-100/80 p-1 rounded-lg border border-zinc-200/50">
            <button onClick={() => setActiveTab('rti')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'rti' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>RTI Drafter</button>
            <button onClick={() => setActiveTab('rights')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'rights' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Rights Navigator</button>
            <button onClick={() => setActiveTab('schemes')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'schemes' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Schemes</button>
          </div>
        </div>

        <div className="flex items-center gap-5">
          <div className="flex items-center gap-2 hover:bg-zinc-100 px-3 py-1.5 rounded-lg border border-transparent hover:border-zinc-200 transition-all cursor-pointer">
            <Globe size={16} className="text-zinc-400" />
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-sm font-semibold text-zinc-700 focus:outline-none cursor-pointer appearance-none"
            >
              <option value="English">English</option>
              <option value="Hindi">हिंदी</option>
              <option value="Marathi">मराठी</option>
              <option value="Tamil">தமிழ்</option>
            </select>
            <ChevronDown size={14} className="text-zinc-400 -ml-1" />
          </div>

          <div className="h-5 w-px bg-zinc-200"></div>
          
          <button onClick={resetApp} className="hidden md:flex items-center gap-1.5 text-xs font-bold text-zinc-500 hover:text-zinc-900 transition-colors uppercase tracking-wider">
            <RefreshCcw size={14} /> Reset
          </button>
          
          <div className="flex items-center gap-2 text-sm font-semibold text-zinc-700 bg-white border border-zinc-200 px-3 py-1.5 rounded-lg shadow-sm">
            <Smartphone size={16} className="text-zinc-400" />
            <span>+91 {userMobile}</span>
          </div>
        </div>
      </nav>

      {/* Main Workspace Workspace */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden w-full relative">
        
        {/* LEFT COLUMN: Input */}
        <div className="w-full lg:w-[45%] xl:w-[40%] h-full flex flex-col bg-white border-r border-zinc-200/80 z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)] hide-scroll overflow-y-auto">
          
          {activeTab === 'rti' && (
            <div className="flex flex-col h-full animate-subtle">
              <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="text-2xl font-bold text-zinc-900 tracking-tight">Draft RTI Application</div>
                <div className="text-zinc-500 text-sm mt-1.5 font-medium">Describe your issue naturally. Our AI will handle the bureaucratic formatting.</div>
              </div>

              <div className="flex-1 flex flex-col p-8 bg-zinc-50/30">
                <div className="mb-3 flex items-center justify-between">
                  <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest">Issue Description</label>
                </div>
                
                <div className="relative flex-1 min-h-[300px] mb-6 group">
                  <textarea
                    className="w-full h-full p-5 pb-14 bg-white border border-zinc-200 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none resize-none text-zinc-800 placeholder-zinc-400 transition-all text-base leading-relaxed shadow-sm hide-scroll"
                    placeholder="E.g., The streetlights outside my college have been broken for two months. I have complained twice but nothing happened..."
                    value={complaint}
                    onChange={(e) => setComplaint(e.target.value)}
                    disabled={appState === 'loading' || appState === 'interview'}
                  />
                  <div className="absolute bottom-4 right-4 flex items-center gap-3">
                    <button 
                      onClick={() => handleVoiceInput(isListeningRTI, setIsListeningRTI, setComplaint)}
                      className={`p-2.5 rounded-lg transition-all shadow-sm ${isListeningRTI ? 'bg-red-500 text-white animate-pulse shadow-red-200' : 'bg-white border border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-800 hover:bg-zinc-50'}`}
                      title="Speak your complaint"
                    >
                      {isListeningRTI ? <Mic size={18} /> : <MicOff size={18} />}
                    </button>
                    {complaint.length > 0 && complaint.length < 20 ? (
                      <span className="text-xs font-semibold text-amber-500 bg-amber-50 px-2 py-1 rounded">Too short</span>
                    ) : complaint.length >= 20 ? (
                      <span className="text-xs font-semibold text-emerald-600 bg-emerald-50 px-2 py-1 rounded flex items-center gap-1.5"><CheckCircle size={12} strokeWidth={3}/> Ready</span>
                    ) : null}
                  </div>
                </div>

                <button 
                  onClick={() => generateRTI()}
                  disabled={complaint.length < 20 || appState === 'loading' || appState === 'interview'}
                  className="mt-auto w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 disabled:border-zinc-200 border border-transparent text-white font-semibold text-base py-3.5 rounded-xl transition-all shadow-md active:scale-[0.98]"
                >
                  {appState === 'loading' ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                  {appState === 'loading' ? 'Drafting Document...' : 'Generate Legal Draft'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'rights' && (
            <div className="flex flex-col h-full animate-subtle">
              <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="text-2xl font-bold text-zinc-900 tracking-tight">Rights Navigator</div>
                <div className="text-zinc-500 text-sm mt-1.5 font-medium">Explain your dispute to discover your legal options.</div>
              </div>
              <div className="flex-1 flex flex-col p-8 bg-zinc-50/30">
                <div className="relative flex-1 min-h-[300px] mb-6">
                  <textarea
                    className="w-full h-full p-5 pb-14 bg-white border border-zinc-200 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none resize-none text-zinc-800 placeholder-zinc-400 transition-all text-base leading-relaxed shadow-sm hide-scroll"
                    placeholder="E.g., I was fired from my job without any prior notice or severance pay..."
                    value={rightsSituation}
                    onChange={(e) => setRightsSituation(e.target.value)}
                    disabled={rightsState === 'loading'}
                  />
                  <div className="absolute bottom-4 right-4 flex items-center gap-3">
                    <button 
                      onClick={() => handleVoiceInput(isListeningRights, setIsListeningRights, setRightsSituation)}
                      className={`p-2.5 rounded-lg transition-all shadow-sm ${isListeningRights ? 'bg-red-500 text-white animate-pulse shadow-red-200' : 'bg-white border border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-800 hover:bg-zinc-50'}`}
                    >
                      {isListeningRights ? <Mic size={18} /> : <MicOff size={18} />}
                    </button>
                  </div>
                </div>
                <button 
                  onClick={() => generateRights()}
                  disabled={rightsSituation.length < 10 || rightsState === 'loading'}
                  className="mt-auto w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 text-white font-semibold text-base py-3.5 rounded-xl transition-all shadow-md active:scale-[0.98]"
                >
                  {rightsState === 'loading' ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                  {rightsState === 'loading' ? 'Analyzing Case...' : 'Discover My Rights'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'schemes' && (
            <div className="flex flex-col h-full animate-subtle">
              <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-white/50 backdrop-blur-sm sticky top-0 z-10">
                <div className="text-2xl font-bold text-zinc-900 tracking-tight">Scheme Eligibility</div>
                <div className="text-zinc-500 text-sm mt-1.5 font-medium">Find government welfare programs tailored to you.</div>
              </div>
              <div className="flex-1 flex flex-col p-8 space-y-5 bg-zinc-50/30 hide-scroll overflow-y-auto">
                 <div>
                   <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Age</label>
                   <input type="number" value={schemeProfile.age} onChange={(e) => setSchemeProfile({...schemeProfile, age: parseInt(e.target.value) || ''})} className="w-full bg-white border border-zinc-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                 </div>
                 <div>
                   <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Gender</label>
                   <select value={schemeProfile.gender} onChange={(e) => setSchemeProfile({...schemeProfile, gender: e.target.value})} className="w-full bg-white border border-zinc-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all">
                     <option>Male</option><option>Female</option><option>Other</option>
                   </select>
                 </div>
                 <div>
                   <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Annual Income (₹)</label>
                   <input type="text" value={schemeProfile.income} onChange={(e) => setSchemeProfile({...schemeProfile, income: e.target.value})} className="w-full bg-white border border-zinc-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                 </div>
                 <div>
                   <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Occupation</label>
                   <input type="text" value={schemeProfile.occupation} onChange={(e) => setSchemeProfile({...schemeProfile, occupation: e.target.value})} className="w-full bg-white border border-zinc-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                 </div>
                 <div>
                   <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">State</label>
                   <input type="text" value={schemeProfile.state} onChange={(e) => setSchemeProfile({...schemeProfile, state: e.target.value})} className="w-full bg-white border border-zinc-200 rounded-lg p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                 </div>

                <button onClick={checkSchemes} disabled={schemeState === 'loading'} className="mt-8 w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 text-white font-semibold text-base py-3.5 rounded-xl transition-all shadow-md active:scale-[0.98]">
                  {schemeState === 'loading' ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                  {schemeState === 'loading' ? 'Searching Database...' : 'Find Matches'}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT COLUMN: Output */}
        <div className="w-full lg:w-[55%] xl:w-[60%] h-full flex flex-col bg-[#F9FAFB] hide-scroll overflow-y-auto relative">
          
          {/* Subtle background grid pattern */}
          <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none mix-blend-overlay"></div>
          
          {activeTab === 'rti' && (
            <div className="h-full flex flex-col relative z-10">
              {appState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-12 animate-subtle">
                  <div className="w-20 h-20 bg-white rounded-2xl shadow-sm border border-zinc-200 flex items-center justify-center mb-6 text-zinc-300">
                    <FileText size={36} strokeWidth={1.5} />
                  </div>
                  <div className="text-xl font-bold text-zinc-900 mb-2">No Draft Generated</div>
                  <div className="text-zinc-500 text-base max-w-sm leading-relaxed">
                    Provide the details on the left, and your perfectly formatted legal document will appear here.
                  </div>
                </div>
              )}

              {appState === 'loading' && (
                <div className="flex flex-col h-full p-8 lg:p-12 animate-subtle max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-3 mb-6 text-blue-600">
                    <Loader2 className="animate-spin" size={20} />
                    <span className="font-semibold text-sm tracking-wide">{loadingMessage}</span>
                  </div>
                  <div className="bg-white p-10 rounded-2xl border border-zinc-200 shadow-sm flex-1 animate-pulse">
                    <div className="h-4 bg-zinc-100 rounded-md w-1/3 mb-10"></div>
                    <div className="h-6 bg-zinc-100 rounded-md w-3/4 mb-8"></div>
                    <div className="space-y-4">
                      <div className="h-3 bg-zinc-50 rounded w-full"></div>
                      <div className="h-3 bg-zinc-50 rounded w-full"></div>
                      <div className="h-3 bg-zinc-50 rounded w-11/12"></div>
                      <div className="h-3 bg-zinc-50 rounded w-4/5"></div>
                    </div>
                  </div>
                </div>
              )}

              {appState === 'interview' && (
                <div className="flex flex-col h-full p-8 lg:p-16 animate-subtle max-w-3xl mx-auto w-full justify-center">
                  <div className="bg-white border border-amber-200 shadow-xl shadow-amber-900/5 rounded-3xl p-10 relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-amber-400"></div>
                    
                    <div className="text-2xl font-bold flex items-center gap-3 text-amber-700 mb-3">
                      <AlertCircle size={28} /> Clarification Needed
                    </div>
                    <div className="text-base text-zinc-600 mb-10 leading-relaxed font-medium">
                      To ensure your RTI application is legally sound and actionable, the AI requires a few more specifics.
                    </div>
                    
                    <div className="space-y-8 mb-10">
                      {missingInfo.map((q, idx) => (
                        <div key={idx} className="group">
                          <label className="block text-sm font-bold text-zinc-800 mb-3">{q}</label>
                          <input 
                            type="text"
                            className="w-full bg-zinc-50 border-b-2 border-zinc-200 p-3 text-base focus:border-amber-500 focus:bg-amber-50/30 outline-none transition-all rounded-t-lg"
                            placeholder="Type your answer..."
                            onChange={(e) => setInterviewAnswers({...interviewAnswers, [idx]: e.target.value})}
                          />
                        </div>
                      ))}
                    </div>
                    
                    <button 
                      onClick={submitInterview}
                      className="w-full bg-amber-500 hover:bg-amber-600 text-white font-bold text-lg py-4 rounded-xl transition-all shadow-md active:scale-[0.98] flex justify-center items-center gap-2"
                    >
                      Draft Application <ArrowRight size={20} />
                    </button>
                  </div>
                </div>
              )}

              {appState === 'result' && (
                <div className="flex flex-col h-full p-6 lg:p-10 animate-subtle max-w-5xl mx-auto w-full">
                  <div className="flex items-center justify-between mb-6">
                    <div className="text-xl font-bold flex items-center gap-2.5 text-zinc-900">
                      <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                        <CheckCircle size={18} strokeWidth={2.5} />
                      </div>
                      Draft Ready
                    </div>
                    <div className="flex gap-3">
                      <button className="flex items-center gap-2 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-700 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all active:scale-[0.97]">
                        <Copy size={16} /> Copy
                      </button>
                      <button onClick={handleDownload} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2 px-5 rounded-lg shadow-sm transition-all shadow-blue-600/20 active:scale-[0.97]">
                        <Download size={16} /> Download PDF
                      </button>
                    </div>
                  </div>
                  
                  <div className="bg-white p-8 lg:p-12 rounded-2xl border border-zinc-200 shadow-sm flex-1 flex flex-col mb-4 overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
                       <FileText size={200} />
                    </div>

                    <div className="mb-8 group relative z-10">
                      <label className="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-2">Addressed To</label>
                      <input 
                        type="text" 
                        value={docData.department} 
                        onChange={(e) => setDocData({...docData, department: e.target.value})} 
                        className="w-full bg-transparent text-zinc-900 font-semibold text-lg border-b border-transparent hover:border-zinc-200 focus:border-blue-500 focus:outline-none pb-2 transition-colors" 
                      />
                    </div>
                    
                    <div className="mb-8 group relative z-10">
                      <label className="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-2">Subject</label>
                      <input 
                        type="text" 
                        value={docData.subject} 
                        onChange={(e) => setDocData({...docData, subject: e.target.value})} 
                        className="w-full bg-transparent text-zinc-900 font-bold text-base border-b border-transparent hover:border-zinc-200 focus:border-blue-500 focus:outline-none pb-2 transition-colors" 
                      />
                    </div>
                    
                    <div className="flex-1 flex flex-col group relative z-10">
                      <label className="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3">Application Body</label>
                      <textarea 
                        value={docData.body} 
                        onChange={(e) => setDocData({...docData, body: e.target.value})} 
                        className="w-full flex-1 bg-transparent text-zinc-800 font-medium border border-transparent hover:border-zinc-200 focus:border-blue-500 focus:bg-zinc-50/50 rounded-xl focus:outline-none resize-none leading-[1.8] transition-all text-[15px] p-4 -ml-4 hide-scroll" 
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'rights' && (
             <div className="h-full flex flex-col relative z-10">
              {rightsState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-12 animate-subtle">
                  <div className="w-20 h-20 bg-white rounded-2xl shadow-sm border border-zinc-200 flex items-center justify-center mb-6 text-zinc-300">
                    <Scale size={36} strokeWidth={1.5} />
                  </div>
                  <div className="text-xl font-bold text-zinc-900 mb-2">Know Your Rights</div>
                  <div className="text-zinc-500 text-base max-w-sm leading-relaxed">
                    Enter a situation on the left to see what legal rights apply to your specific case.
                  </div>
                </div>
              )}
              {rightsState === 'loading' && (
                <div className="flex flex-col h-full p-8 lg:p-12 animate-subtle max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-3 mb-6 text-blue-600">
                    <Loader2 className="animate-spin" size={20} />
                    <span className="font-semibold text-sm tracking-wide">{loadingMessage}</span>
                  </div>
                </div>
              )}
              {rightsState === 'result' && rightsData && (
                 <div className="flex flex-col h-full p-6 lg:p-10 animate-subtle max-w-4xl mx-auto w-full hide-scroll overflow-y-auto">
                   <div className="text-xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                        <Scale size={18} strokeWidth={2.5} />
                      </div>
                      Applicable Rights
                    </div>

                   <div className="space-y-5">
                     {rightsData.applicable_rights?.map((right, idx) => (
                       <div key={idx} className="bg-white p-7 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
                         <div className="absolute left-0 top-0 bottom-0 w-1 bg-blue-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                         <div className="font-bold text-lg text-zinc-900 mb-1">{right.right_name}</div>
                         <div className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-3">{right.legal_basis}</div>
                         <div className="text-base text-zinc-600 leading-relaxed font-medium">{right.description}</div>
                       </div>
                     ))}
                   </div>

                   <div className="mt-8 bg-zinc-900 text-white p-8 rounded-2xl shadow-xl shadow-zinc-900/10 relative overflow-hidden">
                     <div className="absolute -right-4 -bottom-4 text-zinc-800 opacity-50 pointer-events-none"><Zap size={100}/></div>
                     <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3 relative z-10">Recommended Action</div>
                     <div className="text-lg font-medium leading-relaxed relative z-10">{rightsData.next_steps}</div>
                   </div>
                 </div>
              )}
            </div>
          )}

          {activeTab === 'schemes' && (
            <div className="h-full flex flex-col relative z-10">
              {schemeState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-12 animate-subtle">
                  <div className="w-20 h-20 bg-white rounded-2xl shadow-sm border border-zinc-200 flex items-center justify-center mb-6 text-zinc-300">
                    <Users size={36} strokeWidth={1.5} />
                  </div>
                  <div className="text-xl font-bold text-zinc-900 mb-2">Discover Welfare Schemes</div>
                  <div className="text-zinc-500 text-base max-w-sm leading-relaxed">
                    Provide your details to discover government programs and financial assistance you qualify for.
                  </div>
                </div>
              )}
              {schemeState === 'loading' && (
                <div className="flex flex-col h-full p-8 lg:p-12 animate-subtle max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-3 mb-6 text-blue-600">
                    <Loader2 className="animate-spin" size={20} />
                    <span className="font-semibold text-sm tracking-wide">{loadingMessage}</span>
                  </div>
                </div>
              )}
              {schemeState === 'result' && schemeData && (
                 <div className="flex flex-col h-full p-6 lg:p-10 animate-subtle max-w-4xl mx-auto w-full hide-scroll overflow-y-auto">
                   <div className="text-xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                        <CheckCircle size={18} strokeWidth={2.5} />
                      </div>
                      Eligible Programs
                    </div>
                   
                   <div className="space-y-6">
                     {schemeData.eligible_schemes?.map((scheme, idx) => (
                       <div key={idx} className="bg-white p-7 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow">
                         <div className="font-bold text-xl text-zinc-900 mb-5">{scheme.scheme_name}</div>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                           <div>
                             <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-2 flex items-center gap-1.5"><Sparkles size={12} className="text-blue-500"/> Benefits</div>
                             <div className="text-sm font-medium text-zinc-700 leading-relaxed">{scheme.benefits}</div>
                           </div>
                           <div>
                             <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-2 flex items-center gap-1.5"><CheckCircle size={12} className="text-emerald-500"/> Qualification</div>
                             <div className="text-sm font-medium text-zinc-700 leading-relaxed">{scheme.eligibility_criteria}</div>
                           </div>
                         </div>
                         {scheme.application_link && (
                           <div className="mt-6 pt-5 border-t border-zinc-100 flex justify-end">
                             <a href={scheme.application_link} target="_blank" rel="noreferrer" className="flex items-center gap-1.5 text-sm font-bold text-blue-600 hover:text-blue-700 hover:underline">
                               Apply Now <ArrowRight size={14} />
                             </a>
                           </div>
                         )}
                       </div>
                     ))}
                   </div>
                 </div>
              )}
            </div>
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
print("Done patching retheme into App.jsx")
