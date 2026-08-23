import { useState, useRef, useEffect } from 'react';
import { 
  MapPin, Mail, FileText, Send, Loader2, Paperclip, UploadCloud, 
  ChevronLeft, Copy, Download, RefreshCcw,
  MessageSquare, PlusCircle, AlertCircle, CheckCircle, Users, 
  Scale, BarChart3, ArrowRight, Zap, Shield, HelpCircle, ChevronDown, ChevronUp,
  Gavel, Smartphone, KeyRound, Sparkles, Mic, MicOff, Globe
} from 'lucide-react';


const LocationMapModal = ({ onClose, onLocationSelect }) => {
  useEffect(() => {
    if (!window.L) return;
    const map = window.L.map('mapModal').setView([20.5937, 78.9629], 5); // India center
    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap'
    }).addTo(map);

    let marker;

    map.on('click', async (e) => {
      const { lat, lng } = e.latlng;
      if (marker) map.removeLayer(marker);
      marker = window.L.marker([lat, lng]).addTo(map);
      
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`);
        const data = await res.json();
        if (data && data.display_name) {
          onLocationSelect(data.display_name);
        }
      } catch (err) {
        console.error("Map click fetch error", err);
      }
    });

    // Try to get user location to center the map quickly
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        map.setView([pos.coords.latitude, pos.coords.longitude], 13);
      }, () => {});
    }

    return () => {
      map.remove();
    };
  }, [onLocationSelect]);

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-6">
      <div className="bg-white rounded-3xl w-full max-w-4xl overflow-hidden shadow-2xl flex flex-col animate-subtle border border-zinc-200/50">
        <div className="p-5 border-b border-zinc-100 flex justify-between items-center bg-zinc-50">
          <div className="font-bold text-zinc-900 text-lg flex items-center gap-2"><Globe size={20} className="text-emerald-600"/> Pinpoint Incident Location</div>
          <button onClick={onClose} className="text-zinc-500 hover:text-zinc-900 transition-colors font-bold text-sm bg-zinc-200/50 hover:bg-zinc-200 px-3 py-1.5 rounded-lg">
            Close Map
          </button>
        </div>
        <div className="p-0 relative">
          <div id="mapModal" style={{ height: '65vh', width: '100%', zIndex: 1 }}></div>
          <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur-md px-6 py-3 rounded-full shadow-lg border border-zinc-200/50 text-sm font-bold text-zinc-800 z-[1000] pointer-events-none flex items-center gap-2">
            <MapPin size={16} className="text-red-500 animate-bounce" /> Tap anywhere on the map to set the exact address
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [currentView, setCurrentView] = useState('landing'); 
  const [openFAQ, setOpenFAQ] = useState(null); 
  const [showMap, setShowMap] = useState(false); 
  
  // Auth state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userMobile, setUserMobile] = useState('');
  const [loginStep, setLoginStep] = useState('mobile');
  const [isIntercepting, setIsIntercepting] = useState(false); 
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
  const [applicantName, setApplicantName] = useState('');
  const [dashboardData, setDashboardData] = useState([]);
  const [isFetchingDashboard, setIsFetchingDashboard] = useState(false);
  const [isDraftingAppeal, setIsDraftingAppeal] = useState(false);
  const [attachment, setAttachment] = useState(null);
  const attachmentInputRef = useRef(null);

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

  const [address, setAddress] = useState('');
  const [isLocating, setIsLocating] = useState(false);
  const [locationDetails, setLocationDetails] = useState('');
  const [isFetchingPin, setIsFetchingPin] = useState(false);

  const handleChatSubmit = (e) => {
    e.preventDefault();
    if(!chatInput.trim()) return;
    
    const val = chatInput;
    setChatMessages(prev => [...prev, { role: 'user', text: val }]);
    setChatInput('');
    
    if (chatStep === 'name') {
      setApplicantName(val);
      setTimeout(() => {
        setChatMessages(prev => [...prev, { role: 'bot', text: `Nice to meet you, ${val}. What is your full residential address? (You can type 'skip' to use the map later)` }]);
        setChatStep('address');
      }, 500);
    } else if (chatStep === 'address') {
      if (val.toLowerCase() !== 'skip') setAddress(val);
      setTimeout(() => {
        setChatMessages(prev => [...prev, { role: 'bot', text: `Got it! Lastly, describe the issue you are facing or the information you need in detail.` }]);
        setChatStep('issue');
      }, 500);
    } else if (chatStep === 'issue') {
      setComplaint(val);
      setTimeout(() => {
        setChatMessages(prev => [...prev, { role: 'bot', text: `Perfect! I've populated your form. Redirecting...` }]);
        setTimeout(() => setAppState('empty'), 1200);
      }, 500);
    }
  };

  const handlePinChange = async (e) => {
    const val = e.target.value.replace(/\D/g, '').slice(0, 6);
    setPincode(val);
    
    if (val.length === 6) {
      setIsFetchingPin(true);
      try {
        const res = await fetch(`https://api.postalpincode.in/pincode/${val}`);
        const data = await res.json();
        if (data && data[0].Status === 'Success') {
          const po = data[0].PostOffice[0];
          setLocationDetails(`${po.Name}, ${po.District}, ${po.State}`);
        } else {
          setLocationDetails('Invalid PIN code');
        }
      } catch (err) {
        setLocationDetails('Failed to fetch location');
      }
      setIsFetchingPin(false);
    } else {
      setLocationDetails('');
    }
  };

  const [appState, setAppState] = useState('empty'); 
  const [chatMessages, setChatMessages] = useState([{ role: 'bot', text: 'Hello! I am your AI assistant. To start, what is your full name?' }]);
  const [chatInput, setChatInput] = useState('');
  const [chatStep, setChatStep] = useState('name'); 
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

            // --- Summarizer State ---
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
        body: JSON.stringify({ mobile_number: mobileInput.replace(/\D/g, ''), otp: otpInput.replace(/\D/g, '') })
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

  
  const handleGetCurrentLocation = () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }
    setIsLocating(true);
    navigator.geolocation.getCurrentPosition(async (position) => {
      try {
        const { latitude, longitude } = position.coords;
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
        const data = await res.json();
        
        if (data && data.display_name) {
          setAddress(data.display_name);
        }
      } catch (e) {
        console.error("Location error", e);
        setLocationDetails("Failed to fetch location");
      }
      setIsLocating(false);
    }, () => {
      alert("Unable to retrieve your location. Please check browser permissions.");
      setIsLocating(false);
    });
  };

  const generateRTI = async (textToUse = complaint) => {
    if (textToUse.length < 20) return;
    setAppState('loading');
    setLoadingMessage('AI is analyzing and drafting your request...');
    
    let finalPayload = textToUse;
    if (textToUse === complaint && address) {
       finalPayload = `[Applicant Full Address: ${address}] ` + textToUse;
    }
    
    try {
      const formData = new FormData();
      formData.append('complaint_text', finalPayload);
      formData.append('applicant_id', userMobile);
      formData.append('language', language);
      formData.append('applicant_name', applicantName || 'Citizen');
      if (attachment) {
        formData.append('file', attachment);
      }

      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        body: formData
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
    const combined = complaint + "\n\nFollow-up Details:\n" + missingInfo.map((q, i) => `Q: ${q}\nA: ${interviewAnswers[i] || 'Unknown'}`).join('\n');
    setComplaint(combined);
    generateRTI(combined);
  };


  const [isAutomating, setIsAutomating] = useState(false);

  const handleAutoFill = async () => {
    setIsAutomating(true);
    try {
      await fetch('http://127.0.0.1:8000/auto_fill_portal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          applicant_name: applicantName,
          address: address,
          complaint: docData.body,
          department: docData.department || ''
        })
      });
    } catch (err) {
      console.error(err);
    }
    setTimeout(() => setIsAutomating(false), 3000);
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
    setSummaryState('empty');
    setSummaryFile(null);
    setSummaryState('empty');
    setSummaryFile(null);
    setSummaryState('empty');
    setSummaryFile(null);
  };

  // --- VIEW 0: LOGIN PAGE ---
  if (currentView === 'login') {
    return (
      <div className="min-h-screen w-full bg-[#f8f9fa] flex flex-col justify-center items-center p-6 relative overflow-hidden selection:bg-[#e0e0ff] selection:text-[#3b36e8]">
        {/* Minimal aesthetic background elements */}
        <div className="absolute top-[-20%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-slate-100/50 blur-3xl pointer-events-none"></div>
        
        <div className="w-full max-w-md bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-200 p-10 relative z-10">
          <div className="text-center mb-10">
            <div className="mx-auto w-16 h-16 bg-[#1e1b4b] text-white rounded-2xl flex items-center justify-center mb-6 shadow-md shadow-indigo-900/20">
              <Scale size={32} />
            </div>
            <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Welcome Back</h2>
            <p className="text-slate-500 text-sm mt-3 font-medium">Secure, passwordless entry to your civic dashboard.</p>
          </div>

          {authError && (
            <div className="mb-6 p-4 bg-red-50 border border-red-100 text-red-600 text-sm rounded-xl flex items-center gap-3 font-medium">
              <AlertCircle size={18} className="shrink-0" /> {authError}
            </div>
          )}

          {loginStep === 'mobile' ? (
            <div className="space-y-6">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-2">Mobile Number</label>
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <span className="text-slate-400 font-semibold">+91</span>
                  </div>
                  <input
                    type="text"
                    maxLength={11} // 10 digits + 1 space
                    value={mobileInput.replace(/\D/g, '').replace(/(\d{5})(\d)/, '$1 $2')}
                    onChange={(e) => setMobileInput(e.target.value.replace(/\D/g, ''))}
                    className="w-full pl-14 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#3b36e8]/20 focus:border-[#3b36e8] focus:bg-white focus:outline-none transition-all font-semibold text-slate-900 text-lg"
                    placeholder="Enter 10-digit number"
                  />
                </div>
              </div>
              <button
                onClick={handleSendOTP}
                disabled={mobileInput.replace(/\D/g, '').length !== 10}
                className="w-full bg-[#1e1b4b] hover:bg-[#2e2b5e] disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold py-4 rounded-xl transition-all shadow-lg active:scale-95 flex justify-center items-center gap-2 group"
              >
                Send Secure OTP <ArrowRight size={18} className={mobileInput.replace(/\D/g, '').length === 10 ? 'group-hover:translate-x-1 transition-transform' : ''} />
              </button>
            </div>
          ) : (
            <div className="space-y-6">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-2">Verification Code</label>
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    {isIntercepting ? <Loader2 size={20} className="text-[#3b36e8] animate-spin" /> : <KeyRound size={20} className="text-slate-400" />}
                  </div>
                  <input
                    type="text"
                    maxLength={6}
                    value={otpInput}
                    onChange={(e) => setOtpInput(e.target.value.replace(/\D/g, ''))}
                    className="w-full pl-12 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#3b36e8]/20 focus:border-[#3b36e8] focus:bg-white focus:outline-none transition-all text-center tracking-[0.5em] font-mono text-2xl text-slate-900 font-bold"
                    placeholder="------"
                  />
                </div>
                {isIntercepting ? (
                  <p className="text-xs text-[#3b36e8] text-center mt-4 font-bold flex items-center justify-center gap-1.5 animate-pulse">
                    <Sparkles size={14} /> Intercepting secure SMS...
                  </p>
                ) : (
                  <p className="text-xs text-emerald-600 text-center mt-4 font-bold flex items-center justify-center gap-1.5">
                    <CheckCircle size={14} /> Code automatically retrieved
                  </p>
                )}
              </div>
              <button
                onClick={handleVerifyOTP}
                disabled={otpInput.length !== 6 || isIntercepting}
                className="w-full bg-[#3b36e8] hover:bg-[#2e2bcf] disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold py-4 rounded-xl transition-all shadow-lg active:scale-95"
              >
                Verify & Access Dashboard
              </button>
            </div>
          )}
        </div>
        <button onClick={() => setCurrentView('landing')} className="mt-8 text-slate-500 hover:text-[#1e1b4b] font-bold text-sm flex items-center gap-1.5 transition-colors">
          <ChevronLeft size={16} /> Return to Homepage
        </button>
      </div>
    );
  }

  // --- VIEW 1: LANDING PAGE ---
  if (currentView === 'landing') {
    return (
      <div className="min-h-screen bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">
        <style>{`body, html { overflow-x: hidden; margin: 0; padding: 0; }`}</style>
        <nav className="w-full flex items-center justify-between px-8 py-6 bg-transparent absolute top-0 z-50">
          <div className="flex items-center gap-3 font-bold text-2xl tracking-tight text-slate-900 cursor-pointer">
            <div className="w-10 h-10 bg-[#1e1b4b] text-white rounded-lg flex items-center justify-center shadow-sm"><Scale size={20} /></div>
            <div className="flex flex-col justify-center leading-tight"><span>Civic<span className="text-[#3b36e8] font-normal">Action</span></span></div>
          </div>
          <button onClick={() => setCurrentView(isAuthenticated ? 'app' : 'login')} className="bg-transparent hover:bg-slate-100 text-slate-800 font-semibold py-2 px-6 rounded-lg border border-slate-300 transition-all shadow-sm">
            {isAuthenticated ? 'Go to Dashboard' : 'Sign In'}
          </button>
        </nav>
        
        <main className="flex-1 w-full flex flex-col pt-16 md:pt-20">
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
              {/* Flex container ensures content dictates height and never overlaps text */}
              <div className="relative w-full max-w-[450px] flex flex-col items-end">
                
                {/* Yellow Card (You Type) */}
                <div className="w-[85%] bg-[#fffdf0] border border-[#fde68a] rounded-xl p-5 sm:p-6 shadow-sm rotate-[-2deg] self-start z-10 transition-transform hover:rotate-0">
                  <div className="text-[#b45309] text-[11px] font-bold uppercase tracking-widest mb-3">You Type</div>
                  <div className="text-[#334155] font-medium text-base sm:text-[17px] leading-relaxed">
                    "My road hasn't been repaired even though funds were sanctioned last year — why?"
                  </div>
                </div>
                
                {/* White Card (Drafted) */}
                <div className="w-[92%] bg-white border border-slate-200 rounded-xl p-6 sm:p-8 shadow-2xl z-20 -mt-4 sm:-mt-8 rotate-[2deg] relative transition-transform hover:rotate-0">
                  <div className="absolute -top-6 -right-3 sm:-top-8 sm:-right-6 w-[70px] h-[70px] sm:w-[90px] sm:h-[90px] rounded-full border-[3px] border-[#dc2626] text-[#dc2626] flex flex-col items-center justify-center rotate-[15deg] bg-white shadow-sm z-30">
                    <span className="text-[7px] sm:text-[9px] font-extrabold tracking-widest uppercase mb-0.5">Drafted</span>
                    <span className="text-[9px] sm:text-[11px] font-bold font-mono">RTI-01</span>
                  </div>
                  <div className="font-mono text-[11px] sm:text-[13px] text-slate-700 space-y-4 sm:space-y-5 leading-relaxed">
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
            </div>          </div>

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

  // --- VIEW 2: APPLICATION INTERFACE ---
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
            <button onClick={() => setActiveTab('dashboard')} className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-all duration-200 ${activeTab === 'dashboard' ? 'bg-white text-zinc-900 shadow-sm' : 'text-zinc-500 hover:text-zinc-800'}`}>Dashboard</button>
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

          {/* TAB 1: RTI DRAFTER */}
          {activeTab === 'rti' && (
            <div className="animate-subtle">
              
              {appState === 'chat' && (
                <div className="max-w-2xl mx-auto bg-white rounded-3xl shadow-sm border border-zinc-200 overflow-hidden flex flex-col h-[600px]">
                  <div className="px-6 py-4 border-b border-zinc-100 bg-zinc-50 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white shadow-sm">
                        <Sparkles size={20} />
                      </div>
                      <div>
                        <div className="font-bold text-zinc-900">AI Assistant</div>
                        <div className="text-xs text-blue-600 font-semibold">Conversational Form Filler</div>
                      </div>
                    </div>
                    <button onClick={() => setAppState('empty')} className="text-sm font-bold text-zinc-500 hover:text-zinc-800 bg-zinc-100 px-3 py-1.5 rounded-lg">Back to Form</button>
                  </div>
                  <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-4 bg-[#f8f9fa]">
                    {chatMessages.map((msg, i) => (
                      <div key={i} className={`flex ${msg.role === 'bot' ? 'justify-start' : 'justify-end'}`}>
                        <div className={`max-w-[80%] px-4 py-3 rounded-2xl text-sm ${msg.role === 'bot' ? 'bg-white border border-zinc-200 text-zinc-800 rounded-tl-none shadow-sm font-medium' : 'bg-blue-600 text-white rounded-tr-none font-medium'}`}>
                          {msg.text}
                        </div>
                      </div>
                    ))}
                  </div>
                  <form onSubmit={handleChatSubmit} className="p-4 border-t border-zinc-100 bg-white">
                    <div className="relative">
                      <input 
                        type="text" 
                        value={chatInput}
                        onChange={e => setChatInput(e.target.value)}
                        placeholder="Type your answer here..."
                        className="w-full bg-zinc-50 border border-zinc-200 rounded-xl py-3 pl-4 pr-12 focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-none text-sm font-medium"
                        autoFocus
                      />
                      <button type="submit" disabled={!chatInput.trim()} className="absolute right-2 top-2 p-1.5 bg-blue-600 text-white rounded-lg disabled:opacity-50">
                        <ArrowRight size={16} />
                      </button>
                    </div>
                  </form>
                </div>
              )}

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
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                            <span className="bg-red-100 text-red-600 px-1.5 py-0.5 rounded text-[9px]">Required</span>
                            Full Address
                          </label>
                          <div className="flex gap-2">
                            <button onClick={() => setShowMap(true)} className="text-[10px] text-emerald-600 font-bold hover:text-emerald-800 flex items-center gap-1.5 bg-emerald-50 px-2.5 py-1 rounded transition-all active:scale-95 shadow-sm border border-emerald-200 hover:bg-emerald-100">
                              <Globe size={12} /> Open Map
                            </button>
                            <button onClick={handleGetCurrentLocation} className="text-[10px] text-blue-600 font-bold hover:text-blue-800 flex items-center gap-1.5 bg-blue-50 px-2.5 py-1 rounded transition-all active:scale-95 shadow-sm border border-blue-200 hover:bg-blue-100">
                              {isLocating ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />} Auto-Locate
                            </button>
                          </div>
                        </div>
                        <div className="relative">
                          <input 
                            type="text" 
                            placeholder="e.g. 123 Main St, New Delhi, 110001" 
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            className="w-full bg-zinc-50 border border-zinc-200 rounded-xl py-3 px-4 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none transition-all text-sm font-semibold text-zinc-800 placeholder-zinc-400"
                          />
                          
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

                                      <div className="flex flex-col sm:flex-row items-center gap-4">
                    <button 
                      onClick={() => generateRTI()}
                      disabled={!applicantName || !address || complaint.length < 20 || appState === 'loading' || appState === 'interview'}
                      className="flex-1 w-full flex items-center justify-center gap-2 bg-zinc-900 hover:bg-black disabled:bg-zinc-100 disabled:text-zinc-400 disabled:border-zinc-200 border border-transparent text-white font-semibold py-4 rounded-xl shadow-sm transition-all active:scale-[0.98]"
                    >
                      {appState === 'loading' ? (
                        <><Loader2 className="animate-spin" size={18} /> Analyzing Issue...</>
                      ) : (
                        <>Draft Application <ArrowRight size={18} /></>
                      )}
                    </button>
                    <div className="text-zinc-400 font-bold text-sm">OR</div>
                    <button 
                      onClick={() => setAppState('chat')}
                      className="flex-1 w-full bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-lg py-4 px-6 rounded-xl border border-blue-200 shadow-sm transition-all active:scale-[0.98] flex items-center justify-center gap-2"
                    >
                      <MessageSquare size={20} />
                      Conversational Fill
                    </button>
                  </div>
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
                  <div className="flex flex-col sm:flex-row items-center gap-4">
                    <button 
                      onClick={submitInterview}
                      disabled={!complaint || !applicantName || !address}
                      className="flex-1 w-full bg-amber-500 hover:bg-amber-600 disabled:bg-zinc-300 disabled:cursor-not-allowed text-white font-bold text-lg py-4 rounded-xl transition-all shadow-md active:scale-[0.98] flex justify-center items-center gap-2"
                    >
                      Draft Application <ArrowRight size={20} />
                    </button>
                    <div className="text-zinc-400 font-bold text-sm">OR</div>
                    <button 
                      onClick={() => setAppState('chat')}
                      className="flex-1 w-full bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold text-lg py-4 px-6 rounded-xl border border-blue-200 shadow-sm transition-all active:scale-[0.98] flex items-center justify-center gap-2"
                    >
                      <MessageSquare size={20} />
                      Conversational Fill
                    </button>
                  </div>
                </div>
              )}

              {appState === 'result' && (
                <div className="max-w-4xl mx-auto animate-subtle">
                  <div className="flex items-center justify-between mb-6">
                    <button onClick={() => { setAppState('empty'); setComplaint(''); setMissingInfo([]); setInterviewAnswers({}); setPincode(''); setLocationDetails(''); setApplicantName(''); setAttachment(null); }} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors">
                      <ArrowRight className="rotate-180" size={16} /> Start Over
                    </button>
                    <div className="flex gap-3">
                      <button onClick={handleDraftAppeal} className="flex items-center gap-2 bg-amber-100 hover:bg-amber-200 text-amber-800 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all">
                        <AlertCircle size={16} /> Draft First Appeal
                      </button>
                      <button onClick={handleEmail} className="flex items-center gap-2 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-700 font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all">
                        <Mail size={16} /> Send via Email
                      </button>
                      <button onClick={handleAutoFill} disabled={isAutomating} className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white font-semibold text-sm py-2 px-4 rounded-lg shadow-sm transition-all shadow-emerald-600/20">
                        {isAutomating ? <Loader2 size={16} className="animate-spin" /> : <Globe size={16} />}
                        {isAutomating ? 'Initiating CivicAssist...' : 'Auto-Fill Official Portal'}
                      </button>
                      <button onClick={handleDownload} className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm py-2 px-5 rounded-lg shadow-sm transition-all shadow-blue-600/20">
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
                   <button onClick={() => { setRightsState('empty'); setRightsSituation(''); }} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
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
                   <button onClick={() => { setSchemeState('empty'); setSchemeProfile({age:'', gender:'Male', income:'', occupation:'', state:''}); }} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
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
                   <button onClick={() => { setSummaryState('empty'); setSummaryFile(null); setSummaryData(null); }} className="flex items-center gap-1.5 text-sm font-bold text-zinc-500 hover:text-zinc-900 transition-colors mb-6">
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

      {/* Map Modal */}
      {showMap && (
        <LocationMapModal 
          onClose={() => setShowMap(false)} 
          onLocationSelect={(addr) => {
            setAddress(addr);
            setShowMap(false);
          }} 
        />
      )}
    </div>
  );
}

export default App;
