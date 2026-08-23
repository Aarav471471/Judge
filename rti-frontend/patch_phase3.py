import re

# We will read the current App.jsx, but honestly since we are adding so much logic, 
# it's better to just write the new one completely to avoid patching nightmares.

NEW_APP_JSX = """import { useState, useRef } from 'react';
import { 
  FileText, Send, Loader2, Paperclip, UploadCloud, 
  ChevronLeft, Copy, Download, RefreshCcw,
  MessageSquare, PlusCircle, AlertCircle, CheckCircle, Users, 
  Scale, BarChart3, ArrowRight, Zap, Shield, HelpCircle, ChevronDown, ChevronUp,
  Gavel, Smartphone, KeyRound, Sparkles, Mic, MicOff, Globe
} from 'lucide-react';

function App() {
  const [currentView, setCurrentView] = useState('landing'); 
  const [openFAQ, setOpenFAQ] = useState(null); 
  
  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userMobile, setUserMobile] = useState('');
  const [loginStep, setLoginStep] = useState('mobile'); 
  const [mobileInput, setMobileInput] = useState('');
  const [otpInput, setOtpInput] = useState('');
  const [authError, setAuthError] = useState('');
  
  // App State
  const [activeTab, setActiveTab] = useState('rti'); 
  const [language, setLanguage] = useState('English');

  // Voice Input State
  const recognitionRef = useRef(null);
  const [isListeningRTI, setIsListeningRTI] = useState(false);
  const [isListeningRights, setIsListeningRights] = useState(false);

  const handleVoiceInput = (isListening, setListening, setter) => {
    if (isListening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voice input is not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    const langMap = { 'English': 'en-IN', 'Hindi': 'hi-IN', 'Marathi': 'mr-IN', 'Tamil': 'ta-IN' };
    recognition.lang = langMap[language] || 'en-IN';
    recognition.interimResults = false;
    
    recognition.onstart = () => setListening(true);
    recognition.onresult = (e) => {
      const text = e.results[0][0].transcript;
      setter(prev => prev + (prev ? " " : "") + text);
      setListening(false);
    };
    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognition.start();
    recognitionRef.current = recognition;
  };

  // --- RTI Drafter State ---
  const [complaint, setComplaint] = useState('');
  const [appState, setAppState] = useState('empty'); 
  const [loadingMessage, setLoadingMessage] = useState('');
  const [showAttachment, setShowAttachment] = useState(false);
  const [file, setFile] = useState(null);
  const [docData, setDocData] = useState({ department: '', subject: '', body: '' });
  const [missingInfo, setMissingInfo] = useState([]);
  const [interviewAnswers, setInterviewAnswers] = useState({});
  const fileInputRef = useRef(null);

  // --- Rights Navigator State ---
  const [rightsSituation, setRightsSituation] = useState('');
  const [rightsState, setRightsState] = useState('empty');
  const [rightsData, setRightsData] = useState(null);

  // --- Schemes State ---
  const [schemeProfile, setSchemeProfile] = useState({ age: 30, gender: 'Male', income: '150000', occupation: 'Farmer', state: 'Uttar Pradesh' });
  const [schemeState, setSchemeState] = useState('empty');
  const [schemeData, setSchemeData] = useState(null);

  const handleSendOTP = async () => {
    if (mobileInput.length !== 10) {
      setAuthError('Please enter a valid 10-digit mobile number');
      return;
    }
    setAuthError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/auth/send-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: mobileInput })
      });
      if (res.ok) {
        const data = await res.json();
        setLoginStep('otp');
        if (data.dev_otp) {
          setOtpInput(data.dev_otp);
        }
      } else {
        setAuthError('Failed to send OTP.');
      }
    } catch (e) {
      setAuthError('Connection error.');
    }
  };

  const handleVerifyOTP = async () => {
    if (otpInput.length !== 6) {
      setAuthError('OTP must be 6 digits');
      return;
    }
    setAuthError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/auth/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: mobileInput, otp: otpInput })
      });
      if (res.ok) {
        setIsAuthenticated(true);
        setUserMobile(mobileInput);
        setCurrentView('app');
      } else {
        setAuthError('Invalid OTP');
      }
    } catch (e) {
      setAuthError('Connection error.');
    }
  };

  const generateRTI = async (textToUse = complaint) => {
    if (textToUse.length < 20) return;
    setAppState('loading');
    setLoadingMessage('AI is analyzing and drafting your request...');
    
    try {
      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ complaint_text: textToUse, applicant_id: userMobile, language })
      });
      if (!res.ok) throw new Error("Backend connection failed");
      const data = await res.json();
      
      if (data.missing_info && data.missing_info.length > 0) {
        setMissingInfo(data.missing_info);
        setAppState('interview');
      } else {
        setDocData({
          department: data.department_identified || "Public Information Officer",
          subject: "Information Request under RTI Act, 2005",
          body: data.rti_draft_preview || ""
        });
        setAppState('result');
      }
    } catch (error) {
      console.error(error);
      alert("Failed to connect to the AI engine.");
      setAppState('empty');
    }
  };

  const submitInterview = () => {
    const combined = complaint + "\\n\\nFollow-up Details:\\n" + missingInfo.map((q, i) => `Q: ${q}\\nA: ${interviewAnswers[i] || 'Unknown'}`).join('\\n');
    setComplaint(combined);
    generateRTI(combined);
  };

  const handleDownload = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/download_pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          applicant_id: userMobile,
          department: docData.department,
          subject: docData.subject,
          body: docData.body
        })
      });
      if (!res.ok) throw new Error("Download failed");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `RTI_Application_${userMobile}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Failed to download PDF.");
    }
  };

  const generateRights = async (textToUse = rightsSituation) => {
    if (textToUse.length < 10) return;
    setRightsState('loading');
    setLoadingMessage('Analyzing legal rights...');
    try {
      const res = await fetch('http://127.0.0.1:8000/navigate-rights', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ situation: textToUse, applicant_id: userMobile, language })
      });
      if (!res.ok) throw new Error("Backend connection failed");
      const data = await res.json();
      setRightsData(data);
      setRightsState('result');
    } catch (error) {
      console.error(error);
      alert("Failed to connect to the AI engine.");
      setRightsState('empty');
    }
  };

  const checkSchemes = async () => {
    setSchemeState('loading');
    setLoadingMessage('Matching government schemes...');
    try {
      const res = await fetch('http://127.0.0.1:8000/check-schemes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...schemeProfile, applicant_id: userMobile, language })
      });
      if (!res.ok) throw new Error("Backend connection failed");
      const data = await res.json();
      setSchemeData(data);
      setSchemeState('result');
    } catch (error) {
      console.error(error);
      alert("Failed to connect to the AI engine.");
      setSchemeState('empty');
    }
  };

  const resetApp = () => {
    setAppState('empty');
    setComplaint('');
    setDocData({ department: '', subject: '', body: '' });
    setShowAttachment(false);
    setFile(null);
    setRightsState('empty');
    setRightsSituation('');
    setSchemeState('empty');
    setMissingInfo([]);
    setInterviewAnswers({});
  };

  // --- VIEW 0: LOGIN PAGE ---
  if (currentView === 'login') {
    return (
      <div className="min-h-screen w-full bg-gradient-to-br from-indigo-50 via-white to-blue-50 flex flex-col justify-center items-center p-6 relative overflow-hidden">
        <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] rounded-full bg-indigo-100/40 blur-3xl mix-blend-multiply pointer-events-none"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] rounded-full bg-blue-100/40 blur-3xl mix-blend-multiply pointer-events-none"></div>
        
        <div className="w-full max-w-md bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white p-10 relative z-10 transition-all">
          <div className="text-center mb-10">
            <div className="mx-auto w-16 h-16 bg-gradient-to-tr from-indigo-600 to-blue-500 text-white rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-indigo-200 rotate-3">
              <Shield size={32} />
            </div>
            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Welcome Back</h2>
            <p className="text-slate-500 text-sm mt-3 leading-relaxed">Secure, passwordless entry to your civic dashboard.</p>
          </div>

          {authError && (
            <div className="mb-6 p-4 bg-red-50/80 backdrop-blur-sm border border-red-100 text-red-600 text-sm rounded-xl flex items-center gap-3">
              <AlertCircle size={18} className="shrink-0" /> {authError}
            </div>
          )}

          {loginStep === 'mobile' ? (
            <div className="space-y-6">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Mobile Number</label>
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <span className="text-slate-400 font-semibold group-focus-within:text-indigo-500 transition-colors">+91</span>
                  </div>
                  <input
                    type="text"
                    maxLength={10}
                    value={mobileInput}
                    onChange={(e) => setMobileInput(e.target.value.replace(/\\D/g, ''))}
                    className="w-full pl-14 pr-4 py-4 bg-slate-50/50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 focus:bg-white focus:outline-none transition-all font-medium text-slate-900 text-lg"
                    placeholder="Enter 10-digit number"
                  />
                </div>
              </div>
              <button
                onClick={handleSendOTP}
                disabled={mobileInput.length !== 10}
                className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 disabled:from-slate-300 disabled:to-slate-300 text-white font-bold py-4 rounded-xl transition-all shadow-lg flex justify-center items-center gap-2"
              >
                Send Secure OTP <ArrowRight size={20} />
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div>
                <label className="block text-xs font-bold text-slate-500 uppercase tracking-widest mb-2">Verification Code</label>
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <KeyRound size={20} className="text-slate-400" />
                  </div>
                  <input
                    type="text"
                    maxLength={6}
                    value={otpInput}
                    onChange={(e) => setOtpInput(e.target.value.replace(/\\D/g, ''))}
                    className="w-full pl-12 pr-4 py-4 bg-slate-50/50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 focus:bg-white focus:outline-none transition-all text-center tracking-[0.5em] font-mono text-2xl text-slate-900 font-bold"
                    placeholder="------"
                  />
                </div>
                <p className="text-xs text-emerald-600 text-center mt-4 font-medium flex items-center justify-center gap-1.5 bg-emerald-50 py-2 rounded-lg">
                  <Sparkles size={14} /> Auto-filled by development environment
                </p>
              </div>
              <button
                onClick={handleVerifyOTP}
                disabled={otpInput.length !== 6}
                className="w-full bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 disabled:from-slate-300 disabled:to-slate-300 text-white font-bold py-4 rounded-xl transition-all shadow-lg"
              >
                Verify & Access Dashboard
              </button>
            </div>
          )}
        </div>
        <button onClick={() => setCurrentView('landing')} className="mt-10 text-slate-500 hover:text-slate-900 font-semibold text-sm flex items-center gap-2">
          <ChevronLeft size={16} /> Return to Homepage
        </button>
      </div>
    );
  }

  // --- VIEW 1: LANDING PAGE ---
  if (currentView === 'landing') {
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
        <main className="flex-1 flex flex-col items-center justify-start pt-32 pb-24 w-full relative overflow-hidden">
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
            <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="group text-lg bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 px-10 rounded-full transition-all flex items-center gap-2 mx-auto shadow-xl hover:shadow-indigo-300">
              Start Drafting Now <ArrowRight size={20} />
            </button>
          </div>
        </main>
      </div>
    );
  }

  // --- VIEW 2: APPLICATION INTERFACE ---
  return (
    <div className="h-screen w-full bg-slate-50 text-slate-900 font-sans flex flex-col overflow-hidden fixed inset-0 text-left">
      <nav className="h-14 flex items-center justify-between px-5 bg-white border-b border-slate-200 shrink-0 z-20">
        <div className="flex items-center gap-6">
          <div onClick={() => setCurrentView('landing')} className="flex items-center gap-2 font-bold text-base tracking-tight cursor-pointer hover:text-indigo-600 transition-colors">
            <div className="w-6 h-6 bg-indigo-600 text-white rounded-md flex items-center justify-center"><Scale size={14} /></div>
            <span>CivicAction</span>
          </div>
          
          <div className="hidden md:flex items-center gap-1 ml-4 border-l border-slate-200 pl-4">
            <button onClick={() => setActiveTab('rti')} className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'rti' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}>RTI Drafter</button>
            <button onClick={() => setActiveTab('rights')} className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'rights' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}>Rights Navigator</button>
            <button onClick={() => setActiveTab('schemes')} className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'schemes' ? 'text-indigo-700 bg-indigo-50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'}`}>Schemes</button>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
            <Globe size={14} className="text-slate-500" />
            <select 
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-transparent text-sm font-medium text-slate-700 focus:outline-none cursor-pointer"
            >
              <option value="English">English</option>
              <option value="Hindi">हिंदी (Hindi)</option>
              <option value="Marathi">मराठी (Marathi)</option>
              <option value="Tamil">தமிழ் (Tamil)</option>
            </select>
          </div>

          <button onClick={resetApp} className="hidden md:flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-indigo-600 transition-colors">
            <PlusCircle size={14} /> Reset
          </button>
          <div className="h-4 w-px bg-slate-200"></div>
          <div className="flex items-center gap-2 text-sm font-medium text-slate-600">
            <Smartphone size={14} className="text-slate-400" />
            <span>+91 {userMobile}</span>
          </div>
        </div>
      </nav>

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
                    className="w-full h-full p-4 pb-12 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none resize-none text-slate-800 placeholder-slate-400 transition-all text-sm leading-relaxed shadow-sm scrollbar-thin"
                    placeholder="E.g., The streetlights outside my college have been broken for two months..."
                    value={complaint}
                    onChange={(e) => setComplaint(e.target.value)}
                    disabled={appState === 'loading' || appState === 'interview'}
                  />
                  <div className="absolute bottom-3 right-3 flex items-center gap-3">
                    <button 
                      onClick={() => handleVoiceInput(isListeningRTI, setIsListeningRTI, setComplaint)}
                      className={`p-2 rounded-full transition-colors ${isListeningRTI ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-slate-100 text-slate-500 hover:bg-indigo-50 hover:text-indigo-600'}`}
                      title="Speak your complaint"
                    >
                      {isListeningRTI ? <Mic size={16} /> : <MicOff size={16} />}
                    </button>
                    {complaint.length > 0 && complaint.length < 20 ? (
                      <span className="text-[10px] font-medium text-amber-600">Too short</span>
                    ) : complaint.length >= 20 ? (
                      <span className="text-[10px] font-medium text-emerald-600 flex items-center gap-1"><CheckCircle size={10}/> Ready</span>
                    ) : null}
                  </div>
                </div>
                <button 
                  onClick={() => generateRTI()}
                  disabled={complaint.length < 20 || appState === 'loading' || appState === 'interview'}
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
                    className="w-full h-full p-4 pb-12 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:outline-none resize-none text-slate-800 placeholder-slate-400 transition-all text-sm leading-relaxed shadow-sm"
                    placeholder="E.g., I was fired from my job without any prior notice..."
                    value={rightsSituation}
                    onChange={(e) => setRightsSituation(e.target.value)}
                    disabled={rightsState === 'loading'}
                  />
                  <div className="absolute bottom-3 right-3 flex items-center gap-3">
                    <button 
                      onClick={() => handleVoiceInput(isListeningRights, setIsListeningRights, setRightsSituation)}
                      className={`p-2 rounded-full transition-colors ${isListeningRights ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-slate-100 text-slate-500 hover:bg-indigo-50 hover:text-indigo-600'}`}
                      title="Speak your situation"
                    >
                      {isListeningRights ? <Mic size={16} /> : <MicOff size={16} />}
                    </button>
                  </div>
                </div>
                <button 
                  onClick={() => generateRights()}
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
                 <div><label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Age</label><input type="number" value={schemeProfile.age} onChange={(e) => setSchemeProfile({...schemeProfile, age: parseInt(e.target.value) || ''})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" /></div>
                 <div><label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Gender</label><select value={schemeProfile.gender} onChange={(e) => setSchemeProfile({...schemeProfile, gender: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none"><option>Male</option><option>Female</option><option>Other</option></select></div>
                 <div><label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Annual Income (INR)</label><input type="text" value={schemeProfile.income} onChange={(e) => setSchemeProfile({...schemeProfile, income: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" /></div>
                 <div><label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Occupation</label><input type="text" value={schemeProfile.occupation} onChange={(e) => setSchemeProfile({...schemeProfile, occupation: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" /></div>
                 <div><label className="block text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">State</label><input type="text" value={schemeProfile.state} onChange={(e) => setSchemeProfile({...schemeProfile, state: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-md p-2 text-sm focus:border-indigo-500 focus:outline-none" /></div>
                <button onClick={checkSchemes} disabled={schemeState === 'loading'} className="mt-6 w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 text-white font-medium text-sm py-3 rounded-lg transition-all shadow-sm">
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
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300"><FileText size={28} strokeWidth={1.5} /></div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">No Draft Generated Yet</h2>
                  <p className="text-slate-500 text-sm max-w-sm">Fill out the details on the left, and your formatted RTI application will appear here.</p>
                </div>
              )}
              {appState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600"><Loader2 className="animate-spin" size={18} /><span className="font-medium text-sm">{loadingMessage}</span></div>
                  <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex-1 animate-pulse">
                    <div className="h-3 bg-slate-200 rounded w-1/4 mb-8"></div>
                    <div className="h-6 bg-slate-200 rounded w-3/4 mb-6"></div>
                    <div className="space-y-3"><div className="h-2 bg-slate-100 rounded w-full"></div><div className="h-2 bg-slate-100 rounded w-full"></div><div className="h-2 bg-slate-100 rounded w-5/6"></div></div>
                  </div>
                </div>
              )}
              {appState === 'interview' && (
                <div className="flex flex-col h-full p-6 lg:p-10 animate-in fade-in slide-in-from-bottom-4 max-w-3xl mx-auto w-full">
                  <h2 className="text-xl font-bold flex items-center gap-2 text-amber-600 mb-2">
                    <AlertCircle size={24} /> Missing Information Detected
                  </h2>
                  <p className="text-sm text-slate-600 mb-8 leading-relaxed">
                    To make your legal application effective and complete, the AI requires a few more specifics that were missing from your initial description.
                  </p>
                  <div className="space-y-5 mb-8">
                    {missingInfo.map((q, idx) => (
                      <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                        <label className="block text-sm font-semibold text-slate-800 mb-3">{q}</label>
                        <input 
                          type="text"
                          className="w-full bg-slate-50 border border-slate-200 p-3 rounded-lg text-sm focus:border-indigo-500 focus:outline-none transition-colors"
                          placeholder="Your answer..."
                          onChange={(e) => setInterviewAnswers({...interviewAnswers, [idx]: e.target.value})}
                        />
                      </div>
                    ))}
                  </div>
                  <button 
                    onClick={submitInterview}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl transition-all shadow-md flex justify-center items-center gap-2"
                  >
                    Submit Answers & Draft Application <ArrowRight size={18} />
                  </button>
                </div>
              )}
              {appState === 'result' && (
                <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900"><CheckCircle className="text-emerald-500" size={20} /> Draft Ready for Review</h2>
                    <div className="flex gap-2">
                      <button className="flex items-center gap-1.5 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-medium text-sm py-1.5 px-3 rounded-md shadow-sm"><Copy size={14} /> Copy</button>
                      <button onClick={handleDownload} className="flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm py-1.5 px-4 rounded-md shadow-sm"><Download size={14} /> Download PDF</button>
                    </div>
                  </div>
                  <div className="bg-white p-6 lg:p-8 rounded-xl border border-slate-200 shadow-sm flex-1 flex flex-col mb-2 overflow-hidden">
                    <div className="mb-5 group"><label className="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Addressed To</label><input type="text" value={docData.department} onChange={(e) => setDocData({...docData, department: e.target.value})} className="w-full bg-transparent text-slate-900 font-medium text-base border-b border-transparent hover:border-slate-200 focus:border-indigo-500 focus:outline-none pb-1 transition-colors" /></div>
                    <div className="mb-5 group"><label className="block text-[10px] font-semibold text-slate-500 uppercase mb-1">Subject</label><input type="text" value={docData.subject} onChange={(e) => setDocData({...docData, subject: e.target.value})} className="w-full bg-transparent text-slate-900 font-medium text-sm border-b border-transparent hover:border-slate-200 focus:border-indigo-500 focus:outline-none pb-1 transition-colors" /></div>
                    <div className="flex-1 flex flex-col group"><label className="block text-[10px] font-semibold text-slate-500 uppercase mb-2">Application Body</label><textarea value={docData.body} onChange={(e) => setDocData({...docData, body: e.target.value})} className="w-full flex-1 bg-transparent text-slate-800 border border-transparent hover:border-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 focus:bg-white rounded-md focus:outline-none resize-none leading-relaxed transition-all text-sm p-2 -ml-2 scrollbar-thin" /></div>
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === 'rights' && (
            <>
              {rightsState === 'empty' && (
                <div className="flex flex-col items-center justify-center h-full text-center p-10 animate-in fade-in duration-500">
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300"><Scale size={28} strokeWidth={1.5} /></div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">Know Your Rights</h2>
                  <p className="text-slate-500 text-sm max-w-sm">Enter a situation on the left to see what legal rights apply.</p>
                </div>
              )}
              {rightsState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600"><Loader2 className="animate-spin" size={18} /><span className="font-medium text-sm">{loadingMessage}</span></div>
                </div>
              )}
              {rightsState === 'result' && rightsData && (
                 <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                   <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900 mb-4"><Scale className="text-indigo-600" size={20} /> Applicable Rights</h2>
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
                  <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center mb-4 border border-slate-200 text-slate-300"><AlertCircle size={28} strokeWidth={1.5} /></div>
                  <h2 className="text-base font-semibold text-slate-900 mb-1">Discover Schemes</h2>
                  <p className="text-slate-500 text-sm max-w-sm">Enter your profile details to see which government schemes you qualify for.</p>
                </div>
              )}
              {schemeState === 'loading' && (
                <div className="flex flex-col h-full p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                  <div className="flex items-center gap-2 mb-4 text-indigo-600"><Loader2 className="animate-spin" size={18} /><span className="font-medium text-sm">{loadingMessage}</span></div>
                </div>
              )}
              {schemeState === 'result' && schemeData && (
                 <div className="flex flex-col h-full p-6 lg:p-8 animate-in fade-in max-w-4xl mx-auto w-full">
                   <h2 className="text-lg font-semibold flex items-center gap-2 text-slate-900 mb-4"><CheckCircle className="text-emerald-500" size={20} /> Eligible Schemes</h2>
                   <div className="space-y-4">
                     {schemeData.eligible_schemes?.map((scheme, idx) => (
                       <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                         <h3 className="font-bold text-slate-900 text-base">{scheme.scheme_name}</h3>
                         <div className="mt-3 space-y-2">
                           <div><span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Benefits</span><p className="text-sm text-slate-700">{scheme.benefits}</p></div>
                           <div><span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Why You Qualify</span><p className="text-sm text-slate-700">{scheme.eligibility_criteria}</p></div>
                           {scheme.application_link && (
                             <div className="pt-2"><a href={scheme.application_link} target="_blank" rel="noreferrer" className="text-sm font-semibold text-indigo-600 hover:underline">{scheme.application_link}</a></div>
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

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(NEW_APP_JSX)
print("Done patching Phase 3 into App.jsx")
