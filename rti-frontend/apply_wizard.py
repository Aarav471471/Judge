import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Add applicantName state
if "const [applicantName, setApplicantName] = useState('');" not in text:
    text = text.replace("const [pincode, setPincode] = useState('');", "const [applicantName, setApplicantName] = useState('');\n  const [pincode, setPincode] = useState('');")

# Update validation
old_gen_btn = "disabled={complaint.length < 20 || appState === 'loading' || appState === 'interview'}"
new_gen_btn = "disabled={!applicantName || pincode.length !== 6 || complaint.length < 20 || appState === 'loading' || appState === 'interview'}"
text = text.replace(old_gen_btn, new_gen_btn)

# Define the new View 2 which replaces the left/right column structure completely.
new_view_2 = """  // --- VIEW 2: APPLICATION INTERFACE ---
  return (
    <div className="h-screen w-full bg-[#FAFAFA] text-zinc-900 font-sans flex flex-col overflow-hidden fixed inset-0 text-left selection:bg-blue-100 selection:text-blue-900">
      <style>{`
        .hide-scroll::-webkit-scrollbar { display: none; }
        .hide-scroll { -ms-overflow-style: none; scrollbar-width: none; }
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
            <button onClick={() => setActiveTab('summarizer')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'summarizer' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Doc Summarizer</button>
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
      <div className="flex-1 overflow-y-auto bg-[#F9FAFB] relative hide-scroll">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none mix-blend-overlay"></div>
        
        <div className="max-w-5xl mx-auto w-full py-12 px-6 relative z-10">
          
          {/* TAB 1: RTI DRAFTER */}
          {activeTab === 'rti' && (
            <div className="animate-subtle">
              {appState === 'empty' && (
                <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-sm border border-zinc-200 overflow-hidden">
                  <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-zinc-50/50">
                    <div className="text-2xl font-bold text-zinc-900 tracking-tight">Draft RTI Application</div>
                    <div className="text-zinc-500 text-sm mt-1.5 font-medium">Describe your issue naturally. Our AI will handle the bureaucratic formatting.</div>
                  </div>
                  <div className="p-8">
                    <div className="grid grid-cols-2 gap-6 mb-8">
                      <div>
                        <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2 mb-2">
                          <span className="bg-red-100 text-red-600 px-1.5 py-0.5 rounded text-[9px]">Required</span>
                          Full Name
                        </label>
                        <input 
                          type="text" 
                          placeholder="e.g. Rahul Sharma" 
                          value={applicantName}
                          onChange={(e) => setApplicantName(e.target.value)}
                          className="w-full bg-zinc-50 border border-zinc-200 rounded-xl py-3 px-4 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none transition-all text-sm font-semibold text-zinc-800 placeholder-zinc-400"
                        />
                      </div>
                      <div>
                        <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2 mb-2">
                          <span className="bg-red-100 text-red-600 px-1.5 py-0.5 rounded text-[9px]">Required</span>
                          Area PIN Code
                        </label>
                        <div className="relative">
                          <input 
                            type="text" 
                            placeholder="e.g. 110001" 
                            value={pincode}
                            onChange={handlePinChange}
                            maxLength="6"
                            className="w-full bg-zinc-50 border border-zinc-200 rounded-xl py-3 pl-4 pr-10 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none transition-all text-sm font-semibold text-zinc-800 placeholder-zinc-400"
                          />
                          <div className="absolute inset-y-0 right-3 flex items-center">
                            {isFetchingPin && <Loader2 className="animate-spin text-zinc-400" size={16} />}
                            {!isFetchingPin && locationDetails && !locationDetails.includes('Invalid') && <CheckCircle className="text-emerald-500" size={16} />}
                          </div>
                        </div>
                        {locationDetails && (
                          <div className={`mt-2 text-xs font-semibold ${locationDetails.includes('Invalid') || locationDetails.includes('Failed') ? 'text-red-500' : 'text-blue-600'} animate-subtle flex items-center gap-1.5`}>
                            {locationDetails.includes('Invalid') || locationDetails.includes('Failed') ? null : <span className="w-1.5 h-1.5 rounded-full bg-blue-500 inline-block"></span>}
                            {locationDetails}
                          </div>
                        )}
                      </div>
                    </div>
                    
                    <div className="mb-2 flex items-center justify-between">
                      <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest">Issue Description</label>
                    </div>
                    <div className="relative min-h-[250px] mb-6 group">
                      <textarea
                        className="w-full h-full min-h-[250px] p-5 pb-14 bg-zinc-50 border border-zinc-200 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none resize-none text-zinc-800 placeholder-zinc-400 transition-all text-base leading-relaxed hide-scroll"
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
                      disabled={!applicantName || pincode.length !== 6 || complaint.length < 20 || appState === 'loading' || appState === 'interview'}
                      className="w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 disabled:border-zinc-200 border border-transparent text-white font-semibold text-base py-4 rounded-xl transition-all shadow-md active:scale-[0.98]"
                    >
                      <Sparkles size={18} /> Generate Legal Draft
                    </button>
                  </div>
                </div>
              )}
              
              {appState === 'loading' && (
                <div className="flex flex-col items-center justify-center py-20 text-blue-600 animate-subtle">
                  <Loader2 className="animate-spin mb-4" size={40} />
                  <span className="font-semibold text-lg tracking-wide">{loadingMessage}</span>
                </div>
              )}

              {appState === 'interview' && (
                <div className="max-w-3xl mx-auto bg-white border border-amber-200 shadow-xl shadow-amber-900/5 rounded-3xl p-10 relative overflow-hidden animate-subtle">
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
              )}

              {appState === 'result' && (
                <div className="max-w-4xl mx-auto animate-subtle">
                  <div className="flex items-center justify-between mb-6">
                    <button onClick={() => setAppState('empty')} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors">
                      <ArrowRight className="rotate-180" size={16} /> Start Over
                    </button>
                    <div className="flex gap-3">
                      <button className="flex items-center gap-2 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-700 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all active:scale-[0.97]">
                        <Copy size={16} /> Copy
                      </button>
                      <button onClick={handleDownload} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2 px-5 rounded-lg shadow-sm transition-all shadow-blue-600/20 active:scale-[0.97]">
                        <Download size={16} /> Download PDF
                      </button>
                    </div>
                  </div>
                  <div className="bg-white p-10 lg:p-14 rounded-2xl border border-zinc-200 shadow-sm flex flex-col mb-12 relative overflow-hidden">
                    <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none"><FileText size={200} /></div>
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
                    <div className="flex flex-col group relative z-10 min-h-[400px]">
                      <label className="block text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3">Application Body</label>
                      <textarea 
                        value={docData.body} 
                        onChange={(e) => setDocData({...docData, body: e.target.value})} 
                        className="w-full min-h-[400px] flex-1 bg-transparent text-zinc-800 font-medium border border-transparent hover:border-zinc-200 focus:border-blue-500 focus:bg-zinc-50/50 rounded-xl focus:outline-none resize-y leading-[1.8] transition-all text-[15px] p-4 -ml-4" 
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: RIGHTS NAVIGATOR */}
          {activeTab === 'rights' && (
             <div className="animate-subtle">
              {rightsState === 'empty' && (
                <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-sm border border-zinc-200 overflow-hidden">
                  <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-zinc-50/50">
                    <div className="text-2xl font-bold text-zinc-900 tracking-tight">Rights Navigator</div>
                    <div className="text-zinc-500 text-sm mt-1.5 font-medium">Explain your dispute to discover your legal options.</div>
                  </div>
                  <div className="p-8">
                    <div className="relative min-h-[250px] mb-6 group">
                      <textarea
                        className="w-full h-full min-h-[250px] p-5 pb-14 bg-zinc-50 border border-zinc-200 rounded-xl focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none resize-none text-zinc-800 placeholder-zinc-400 transition-all text-base leading-relaxed hide-scroll"
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
                      className="w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 text-white font-semibold text-base py-4 rounded-xl transition-all shadow-md active:scale-[0.98]"
                    >
                      <Sparkles size={18} /> Discover My Rights
                    </button>
                  </div>
                </div>
              )}
              {rightsState === 'loading' && (
                <div className="flex flex-col items-center justify-center py-20 text-blue-600 animate-subtle">
                  <Loader2 className="animate-spin mb-4" size={40} />
                  <span className="font-semibold text-lg tracking-wide">{loadingMessage}</span>
                </div>
              )}
              {rightsState === 'result' && rightsData && (
                 <div className="max-w-4xl mx-auto animate-subtle">
                   <button onClick={() => setRightsState('empty')} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
                      <ArrowRight className="rotate-180" size={16} /> Start Over
                   </button>
                   <div className="text-2xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                        <Scale size={20} strokeWidth={2.5} />
                      </div>
                      Applicable Rights
                   </div>
                   <div className="space-y-5">
                     {rightsData.applicable_rights?.map((right, idx) => (
                       <div key={idx} className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow relative overflow-hidden group">
                         <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-blue-500 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                         <div className="font-bold text-xl text-zinc-900 mb-2">{right.right_name}</div>
                         <div className="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4">{right.legal_basis}</div>
                         <div className="text-base text-zinc-600 leading-relaxed font-medium">{right.description}</div>
                       </div>
                     ))}
                   </div>
                   <div className="mt-8 bg-zinc-900 text-white p-10 rounded-2xl shadow-xl shadow-zinc-900/10 relative overflow-hidden mb-12">
                     <div className="absolute -right-4 -bottom-4 text-zinc-800 opacity-50 pointer-events-none"><Zap size={150}/></div>
                     <div className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-3 relative z-10">Recommended Action</div>
                     <div className="text-xl font-medium leading-relaxed relative z-10">{rightsData.next_steps}</div>
                   </div>
                 </div>
              )}
            </div>
          )}

          {/* TAB 3: SCHEMES */}
          {activeTab === 'schemes' && (
            <div className="animate-subtle">
              {schemeState === 'empty' && (
                <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-sm border border-zinc-200 overflow-hidden">
                  <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-zinc-50/50">
                    <div className="text-2xl font-bold text-zinc-900 tracking-tight">Discover Welfare Schemes</div>
                    <div className="text-zinc-500 text-sm mt-1.5 font-medium">Provide your details to discover government programs and financial assistance you qualify for.</div>
                  </div>
                  <div className="p-8">
                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                       <div>
                         <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Age</label>
                         <input type="number" value={schemeProfile.age} onChange={(e) => setSchemeProfile({...schemeProfile, age: parseInt(e.target.value) || ''})} className="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                       </div>
                       <div>
                         <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Gender</label>
                         <select value={schemeProfile.gender} onChange={(e) => setSchemeProfile({...schemeProfile, gender: e.target.value})} className="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all">
                           <option>Male</option><option>Female</option><option>Other</option>
                         </select>
                       </div>
                       <div>
                         <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Annual Income (₹)</label>
                         <input type="text" value={schemeProfile.income} onChange={(e) => setSchemeProfile({...schemeProfile, income: e.target.value})} className="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                       </div>
                       <div>
                         <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Occupation</label>
                         <input type="text" value={schemeProfile.occupation} onChange={(e) => setSchemeProfile({...schemeProfile, occupation: e.target.value})} className="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                       </div>
                       <div className="md:col-span-2">
                         <label className="block text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-2">State</label>
                         <input type="text" value={schemeProfile.state} onChange={(e) => setSchemeProfile({...schemeProfile, state: e.target.value})} className="w-full bg-zinc-50 border border-zinc-200 rounded-xl p-3 text-sm font-medium focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10 outline-none transition-all" />
                       </div>
                     </div>
                    <button onClick={checkSchemes} disabled={schemeState === 'loading'} className="mt-8 w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 text-white font-semibold text-base py-4 rounded-xl transition-all shadow-md active:scale-[0.98]">
                      <Sparkles size={18} /> Find Matches
                    </button>
                  </div>
                </div>
              )}
              {schemeState === 'loading' && (
                <div className="flex flex-col items-center justify-center py-20 text-blue-600 animate-subtle">
                  <Loader2 className="animate-spin mb-4" size={40} />
                  <span className="font-semibold text-lg tracking-wide">{loadingMessage}</span>
                </div>
              )}
              {schemeState === 'result' && schemeData && (
                 <div className="max-w-4xl mx-auto animate-subtle">
                   <button onClick={() => setSchemeState('empty')} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
                      <ArrowRight className="rotate-180" size={16} /> Start Over
                   </button>
                   <div className="text-2xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                        <CheckCircle size={20} strokeWidth={2.5} />
                      </div>
                      Eligible Programs
                   </div>
                   <div className="space-y-6 mb-12">
                     {schemeData.eligible_schemes?.map((scheme, idx) => (
                       <div key={idx} className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm hover:shadow-md transition-shadow">
                         <div className="font-bold text-2xl text-zinc-900 mb-6">{scheme.scheme_name}</div>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                           <div>
                             <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3 flex items-center gap-1.5"><Sparkles size={12} className="text-blue-500"/> Benefits</div>
                             <div className="text-base font-medium text-zinc-700 leading-relaxed">{scheme.benefits}</div>
                           </div>
                           <div>
                             <div className="text-[11px] font-bold text-zinc-400 uppercase tracking-widest mb-3 flex items-center gap-1.5"><CheckCircle size={12} className="text-emerald-500"/> Qualification</div>
                             <div className="text-base font-medium text-zinc-700 leading-relaxed">{scheme.eligibility_criteria}</div>
                           </div>
                         </div>
                         {scheme.application_link && (
                           <div className="mt-8 pt-6 border-t border-zinc-100 flex justify-end">
                             <a href={scheme.application_link} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-base font-bold text-blue-600 hover:text-blue-700 hover:underline">
                               Apply Now <ArrowRight size={16} />
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

          {/* TAB 4: SUMMARIZER */}
          {activeTab === 'summarizer' && (
            <div className="animate-subtle">
              {summaryState === 'empty' && (
                <div className="max-w-3xl mx-auto bg-white rounded-3xl shadow-sm border border-zinc-200 overflow-hidden">
                  <div className="px-8 pt-8 pb-6 border-b border-zinc-100 bg-zinc-50/50">
                    <div className="text-2xl font-bold text-zinc-900 tracking-tight">Document Summarizer</div>
                    <div className="text-zinc-500 text-sm mt-1.5 font-medium">Upload any government notice, FIR, or legal paper to get a clear summary.</div>
                  </div>
                  <div className="p-8">
                     <div 
                       className="border-2 border-dashed border-zinc-300 rounded-2xl p-12 flex flex-col items-center justify-center bg-zinc-50 hover:bg-zinc-100 hover:border-blue-400 transition-all cursor-pointer group"
                       onClick={() => document.getElementById('file-upload').click()}
                     >
                       <div className="w-20 h-20 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-5 group-hover:scale-110 transition-transform">
                         <UploadCloud size={40} />
                       </div>
                       <div className="text-lg font-bold text-zinc-800 mb-2">Click to Upload Document</div>
                       <div className="text-sm font-medium text-zinc-500 mb-6">Supports PDF, JPG, PNG</div>
                       
                       {summaryFile ? (
                         <div className="px-5 py-2.5 bg-blue-50 text-blue-700 rounded-xl text-base font-bold flex items-center gap-2">
                           <FileText size={18} /> {summaryFile.name}
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
                      className="mt-8 w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 disabled:border-zinc-200 border border-transparent text-white font-semibold text-base py-4 rounded-xl transition-all shadow-md active:scale-[0.98]"
                    >
                      <Sparkles size={18} /> Generate Summary
                    </button>
                  </div>
                </div>
              )}
              {summaryState === 'loading' && (
                <div className="flex flex-col items-center justify-center py-20 text-blue-600 animate-subtle">
                  <Loader2 className="animate-spin mb-4" size={40} />
                  <span className="font-semibold text-lg tracking-wide">{loadingMessage}</span>
                </div>
              )}
              {summaryState === 'result' && summaryData && (
                 <div className="max-w-4xl mx-auto animate-subtle">
                   <button onClick={() => setSummaryState('empty')} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
                      <ArrowRight className="rotate-180" size={16} /> Start Over
                   </button>
                   <div className="text-2xl font-bold flex items-center gap-2.5 text-zinc-900 mb-8">
                      <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600">
                        <FileText size={20} strokeWidth={2.5} />
                      </div>
                      Analysis Complete
                    </div>
                   <div className="space-y-6 mb-12">
                     <div className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm relative overflow-hidden group">
                       <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-indigo-500"></div>
                       <div className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-3">Document Type</div>
                       <div className="font-bold text-2xl text-zinc-900">{summaryData.document_type}</div>
                     </div>
                     <div className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm">
                       <div className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-4 flex items-center gap-1.5"><Sparkles size={14} className="text-indigo-500"/> Summary</div>
                       <div className="text-lg text-zinc-700 leading-[1.8] font-medium whitespace-pre-wrap">{summaryData.summary}</div>
                     </div>
                     <div className="mt-8 bg-zinc-900 text-white p-10 rounded-2xl shadow-xl shadow-zinc-900/10 relative overflow-hidden">
                       <div className="absolute -right-4 -bottom-4 text-zinc-800 opacity-50 pointer-events-none"><AlertCircle size={150}/></div>
                       <div className="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-3 relative z-10">Action Required</div>
                       <div className="text-xl font-medium leading-relaxed relative z-10">{summaryData.action_required}</div>
                     </div>
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

start_idx = text.find("  // --- VIEW 2: APPLICATION INTERFACE ---")
final_app_jsx = text[:start_idx] + new_view_2

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(final_app_jsx)

print("Wizard UI implementation complete")
