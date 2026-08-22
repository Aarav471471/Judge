import { useState, useRef, useEffect } from 'react';
import { 
  FileText, Send, Loader2, Paperclip, UploadCloud, 
  ChevronLeft, Copy, Download, RefreshCcw, LayoutTemplate, 
  MessageSquare, PlusCircle, AlertCircle, CheckCircle, Users, 
  Scale, BarChart3, ArrowRight, Zap, Shield, HelpCircle, ChevronDown, ChevronUp,
  Gavel, Database 
} from 'lucide-react';

function App() {
  const [currentView, setCurrentView] = useState('landing'); // 'landing', 'app', or 'database'
  const [openFAQ, setOpenFAQ] = useState(null); 
  
  const [complaint, setComplaint] = useState('');
  const [appState, setAppState] = useState('empty'); 
  const [loadingMessage, setLoadingMessage] = useState('');
  const [showAttachment, setShowAttachment] = useState(false);
  const [file, setFile] = useState(null);
  
  const [docData, setDocData] = useState({ department: '', subject: '', body: '' });
  
  // Database cases state for the new database page
  const [casesList, setCasesList] = useState([]);
  const [dbLoading, setDbLoading] = useState(false);

  const fileInputRef = useRef(null);

  const suggestions = [
    "Broken streetlight", 
    "Ration card delay", 
    "Pothole complaint"
  ];

  const faqs = [
    {
      q: "Is this legally valid?",
      a: "Yes. The generated document follows the standard structure required under the Right to Information Act, 2005. You simply need to print it, sign it, attach the nominal fee, and submit it."
    },
    {
      q: "What happens after I download it?",
      a: "You must mail the printed application via Speed Post or deliver it in person to the Public Information Officer (PIO) of the concerned department. Some states also allow uploading this PDF to their online RTI portals."
    },
    {
      q: "Do I need a lawyer?",
      a: "No. The RTI Act was specifically designed for everyday citizens. Our tool bridges the gap between plain language and formal bureaucratic phrasing so you don't need any legal representation."
    }
  ];

  const generateRTI = async () => {
    if (complaint.length < 20) return;
    setAppState('loading');
    setLoadingMessage('Identifying the right department...');
    
    try {
      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ complaint_text: complaint, applicant_id: "IIT2025002" })
      });
      if (!res.ok) throw new Error("Backend connection failed");
      const data = await res.json();
      
      const newDepartment = data.department_identified || "Public Information Officer";
      const newSubject = "Information Request under RTI Act, 2005";
      const newBody = data.rti_draft_preview || "";

      setDocData({
        department: newDepartment,
        subject: newSubject,
        body: newBody
      });
      setAppState('result');

      // Automatically push/save to your friend's database backend endpoint if available
      fetch('http://127.0.0.1:8000/cases', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ department: newDepartment, subject: newSubject, body: newBody })
      }).catch(err => console.log("DB Auto-save notice:", err));

    } catch (error) {
      console.error(error);
      alert("Failed to connect to the AI engine. Is the FastAPI server running?");
      setAppState('empty');
    }
  };

  // Fetch all complaints from your friend's database when entering the database view
  const fetchAllCases = async () => {
    setDbLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/cases'); // Adjust to match your friend's FastAPI route
      if (!res.ok) throw new Error("Failed to fetch cases");
      const data = await res.json();
      setCasesList(data);
    } catch (error) {
      console.error("Error fetching database cases:", error);
      setCasesList([]);
    } finally {
      setDbLoading(false);
    }
  };

  useEffect(() => {
    if (currentView === 'database') {
      fetchAllCases();
    }
  }, [currentView]);

  const handleDownload = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/download_pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ applicant_id: "IIT2025002" })
      });
      if (!res.ok) throw new Error("Download failed");
      
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'RTI_Application.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      alert("Failed to download PDF.");
    }
  };

  const resetApp = () => {
    setAppState('empty');
    setComplaint('');
    setDocData({ department: '', subject: '', body: '' });
    setShowAttachment(false);
    setFile(null);
  };

  // --- VIEW 1: LANDING PAGE (Fully Restored) ---
  if (currentView === 'landing') {
    return (
      <div className="min-h-screen w-full bg-white text-slate-900 font-sans flex flex-col">
        <nav className="w-full flex items-center justify-between px-8 py-5 bg-white border-b border-slate-200 shrink-0">
          <div className="flex items-center gap-3 font-bold text-xl tracking-wide text-slate-900">
            <img src="/image.jpg.jpg" alt="Official Emblem" className="h-12 w-auto mix-blend-multiply" />
            <div className="flex flex-col justify-center">
              <span>RTI Auto-Drafter</span>
              <span className="text-[10px] text-slate-500 uppercase tracking-widest font-medium mt-0.5">Civic Action Engine</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setCurrentView('database')}
              className="text-slate-600 hover:text-blue-600 font-medium text-sm flex items-center gap-1.5 transition-colors"
            >
              <Database size={16} /> All Complaints (DB)
            </button>
            <button 
              onClick={() => setCurrentView('app')}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-5 rounded-lg transition-colors shadow-sm text-sm"
            >
              Launch App
            </button>
          </div>
        </nav>

        <main className="flex-1 flex flex-col items-center justify-start px-6 max-w-5xl mx-auto py-16 pb-24 w-full">
          <div className="text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-50 text-blue-700 font-medium text-sm mb-6 border border-blue-100">
              <Scale size={16} /> Democratizing Legal Action
            </div>
            <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-6 leading-tight text-slate-900">
              Draft Legal Notices in <span className="text-blue-600">Plain Language.</span>
            </h1>
            <p className="text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
              Describe your civic issue like you are talking to a friend. Our AI instantly formats it into a legally sound Right to Information (RTI) application ready for submission.
            </p>
            <button 
              onClick={() => setCurrentView('app')}
              className="text-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-10 rounded-xl transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
            >
              Start Drafting Now
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 w-full max-w-4xl text-center">
            <div className="flex flex-col items-center">
              <div className="w-14 h-14 bg-slate-50 border border-slate-200 rounded-2xl flex items-center justify-center mb-4 text-blue-600 shadow-sm">
                <MessageSquare size={24} />
              </div>
              <h3 className="font-bold text-lg text-slate-900 mb-2">1. Describe your issue</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Explain the problem in everyday language. No legal jargon required.</p>
            </div>
            <div className="flex flex-col items-center relative">
              <div className="hidden md:block absolute top-7 left-[-20%] w-[40%] border-t-2 border-dashed border-slate-200"></div>
              <div className="hidden md:block absolute top-7 right-[-20%] w-[40%] border-t-2 border-dashed border-slate-200"></div>
              <div className="w-14 h-14 bg-slate-50 border border-slate-200 rounded-2xl flex items-center justify-center mb-4 text-blue-600 shadow-sm relative z-10">
                <Zap size={24} />
              </div>
              <h3 className="font-bold text-lg text-slate-900 mb-2">2. AI drafts your RTI</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Our engine identifies the right department and formats a formal legal request.</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-14 h-14 bg-slate-50 border border-slate-200 rounded-2xl flex items-center justify-center mb-4 text-blue-600 shadow-sm">
                <Download size={24} />
              </div>
              <h3 className="font-bold text-lg text-slate-900 mb-2">3. Download & submit</h3>
              <p className="text-slate-500 text-sm leading-relaxed">Get a print-ready PDF instantly. Just sign it and send it to the PIO.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 w-full">
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col items-center">
              <CheckCircle size={32} className="text-green-500 mb-3" />
              <h3 className="text-3xl font-bold text-slate-900 mb-1">12,450+</h3>
              <p className="text-slate-500 font-medium text-sm">Cases Drafted</p>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col items-center">
              <Users size={32} className="text-blue-500 mb-3" />
              <h3 className="text-3xl font-bold text-slate-900 mb-1">98.2%</h3>
              <p className="text-slate-500 font-medium text-sm">Citizen Satisfaction</p>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col items-center">
              <FileText size={32} className="text-purple-500 mb-3" />
              <h3 className="text-3xl font-bold text-slate-900 mb-1">&lt; 3 Min</h3>
              <p className="text-slate-500 font-medium text-sm">Average Draft Time</p>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-6 md:gap-12 mt-8 w-full">
            <div className="flex items-center gap-2 text-slate-500 text-sm font-medium">
              <CheckCircle size={16} className="text-blue-500" /> Free & no login required
            </div>
            <div className="flex items-center gap-2 text-slate-500 text-sm font-medium">
              <Shield size={16} className="text-blue-500" /> Built for RTI Act, 2005 (India)
            </div>
            <div className="flex items-center gap-2 text-slate-500 text-sm font-medium">
              <AlertCircle size={16} className="text-blue-500" /> Drafting aid, not legal advice
            </div>
          </div>

          <div className="mt-24 w-full bg-slate-50 p-8 md:p-12 rounded-3xl border border-slate-200 shadow-sm">
            <h3 className="text-2xl font-bold text-slate-900 mb-8 text-center">See it in action</h3>
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm relative">
                <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <MessageSquare size={14} /> You type this
                </div>
                <p className="text-slate-700 text-lg leading-relaxed italic">
                  "The streetlights near my college have been broken for 3 months and it's unsafe at night. I want to know when they will be fixed and how much money is given for repairs."
                </p>
                <div className="absolute -right-4 md:-right-6 top-1/2 -translate-y-1/2 w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white shadow-lg md:rotate-0 rotate-90 md:translate-y-0 translate-y-16">
                  <ArrowRight size={16} />
                </div>
              </div>
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm font-serif">
                <div className="text-xs font-bold font-sans text-blue-600 uppercase tracking-wider mb-4 flex items-center gap-2 border-b border-slate-100 pb-3">
                  <Gavel size={14} className="text-slate-900" /> AI generates this
                </div>
                <div className="space-y-3 text-sm text-slate-800">
                  <p><strong>To:</strong> Public Information Officer (PIO)<br/>Municipal Corporation</p>
                  <p><strong>Subject:</strong> Information Request under RTI Act, 2005 regarding streetlight maintenance.</p>
                  <p className="pt-2">Sir/Madam,</p>
                  <p>Kindly provide the following information:</p>
                  <ol className="list-decimal pl-5 space-y-1">
                    <li>The estimated timeline for restoring functional streetlights in the specified area.</li>
                    <li>Details of the allocated budget for street lighting repairs in this ward for the current financial year.</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-24 w-full bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
            <h3 className="text-xl font-bold text-slate-900 mb-8 flex items-center justify-center gap-2">
              <BarChart3 size={24} className="text-slate-400" /> Platform Usage by Case Type
            </h3>
            <div className="space-y-6 max-w-3xl mx-auto">
              <div>
                <div className="flex justify-between text-sm font-bold mb-2">
                  <span className="text-slate-900">Civic & Infrastructure (Streetlights, Roads)</span>
                  <span className="text-slate-500">45%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3">
                  <div className="bg-blue-600 h-3 rounded-full" style={{ width: '45%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-bold mb-2">
                  <span className="text-slate-900">Financial & Consumer Rights (Scams, Refunds)</span>
                  <span className="text-slate-500">25%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3">
                  <div className="bg-slate-700 h-3 rounded-full" style={{ width: '25%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm font-bold mb-2">
                  <span className="text-slate-900">Tenancy & Housing (Evictions, Deposits)</span>
                  <span className="text-slate-500">15%</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-3">
                  <div className="bg-slate-400 h-3 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-24 w-full max-w-3xl mx-auto">
            <h3 className="text-2xl font-bold text-slate-900 mb-8 text-center flex items-center justify-center gap-2">
              <HelpCircle size={24} className="text-blue-600" /> Frequently Asked Questions
            </h3>
            <div className="space-y-4">
              {faqs.map((faq, idx) => (
                <div key={idx} className="border border-slate-200 rounded-xl bg-white overflow-hidden shadow-sm">
                  <button 
                    onClick={() => setOpenFAQ(openFAQ === idx ? null : idx)}
                    className="w-full flex items-center justify-between p-5 text-left bg-white hover:bg-slate-50 transition-colors"
                  >
                    <span className="font-semibold text-slate-900">{faq.q}</span>
                    {openFAQ === idx ? <ChevronUp size={20} className="text-slate-400" /> : <ChevronDown size={20} className="text-slate-400" />}
                  </button>
                  {openFAQ === idx && (
                    <div className="p-5 pt-0 text-slate-600 text-sm leading-relaxed border-t border-slate-100">
                      {faq.a}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </main>

        <footer className="w-full bg-slate-50 border-t border-slate-200 mt-12 py-10 px-8">
          <div className="max-w-5xl mx-auto flex flex-col md:flex-row justify-between items-center md:items-start gap-8">
            <div className="text-center md:text-left">
              <div className="flex items-center justify-center md:justify-start gap-3 font-bold text-lg text-slate-900 mb-2">
                <img src="/image.jpg.jpg" alt="Official Emblem" className="h-8 w-auto mix-blend-multiply opacity-80 grayscale" />
                <span>RTI Auto-Drafter</span>
              </div>
              <p className="text-sm text-slate-500 mb-4">Empowering citizens through accessible legal tech.</p>
            </div>
            <div className="flex gap-8 text-sm font-medium text-slate-600">
              <a href="#" className="hover:text-blue-600 transition-colors">About</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Other Tools</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Feedback</a>
            </div>
            <div className="text-center md:text-right">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Suite</p>
              <p className="text-xs text-slate-500">
                Part of the <span className="font-semibold text-slate-700 hover:text-blue-600 cursor-pointer transition-colors">Civic Rights Navigator</span> suite.<br/>
                Explore <a href="#" className="text-blue-600 hover:underline">Scheme Eligibility</a> and <a href="#" className="text-blue-600 hover:underline">Form Filler</a>.
              </p>
            </div>
          </div>
        </footer>
      </div>
    );
  }

  // --- VIEW 3: ALL COMPLAINTS DATABASE PAGE ---
  if (currentView === 'database') {
    return (
      <div className="min-h-screen w-full bg-slate-50 text-slate-900 font-sans flex flex-col">
        <nav className="flex items-center justify-between px-8 py-5 bg-white border-b border-slate-200 shrink-0">
          <div 
            onClick={() => setCurrentView('landing')}
            className="flex items-center gap-3 font-bold text-lg tracking-wide cursor-pointer text-slate-900"
          >
            <img src="/image.jpg.jpg" alt="Official Emblem" className="h-10 w-auto mix-blend-multiply" />
            <span>RTI Auto-Drafter</span>
          </div>
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setCurrentView('app')}
              className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-lg shadow-sm"
            >
              AI Assistant
            </button>
            <button 
              onClick={() => { resetApp(); setCurrentView('app'); }}
              className="flex items-center gap-1.5 text-blue-700 bg-blue-50 px-3 py-1.5 rounded-md text-sm font-medium"
            >
              <PlusCircle size={16} /> New Case
            </button>
          </div>
        </nav>

        <main className="flex-1 max-w-4xl w-full mx-auto p-8">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h2 className="text-2xl font-bold text-slate-900">All Submitted Complaints</h2>
              <p className="text-sm text-slate-500">Live records pulled from your teammate's database backend.</p>
            </div>
            <button 
              onClick={fetchAllCases}
              className="bg-white border border-slate-300 text-slate-700 text-sm font-semibold py-2 px-4 rounded-lg shadow-sm hover:bg-slate-50 transition-colors"
            >
              Refresh Data
            </button>
          </div>

          {dbLoading ? (
            <div className="flex items-center justify-center py-20 text-slate-500 gap-2">
              <Loader2 className="animate-spin" size={20} /> Loading database records...
            </div>
          ) : casesList.length === 0 ? (
            <div className="bg-white border border-slate-200 rounded-xl p-12 text-center shadow-sm">
              <Database className="mx-auto text-slate-300 mb-3" size={40} />
              <p className="text-slate-700 font-medium mb-1">No complaints found in the database.</p>
              <p className="text-slate-400 text-xs mb-4">Try generating a new application in the AI Assistant to populate records.</p>
              <button 
                onClick={() => setCurrentView('app')}
                className="bg-blue-600 text-white text-sm font-semibold py-2 px-5 rounded-lg shadow-sm"
              >
                Create First Case
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {casesList.map((item, index) => (
                <div key={index} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold px-2.5 py-1 bg-blue-50 text-blue-700 rounded-full border border-blue-100">
                      {item.department || "Public Information Officer"}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">ID: #{item.id || index + 1}</span>
                  </div>
                  <h3 className="font-bold text-slate-900 mb-1">{item.subject || "Information Request under RTI Act, 2005"}</h3>
                  <p className="text-slate-600 text-sm whitespace-pre-line line-clamp-3">{item.body}</p>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    );
  }

  // --- VIEW 2: APPLICATION INTERFACE ---
  return (
    <div className="h-screen w-full bg-slate-50 text-slate-900 font-sans flex flex-col overflow-hidden fixed inset-0">
      
      <nav className="flex flex-wrap items-center justify-between px-6 py-4 bg-white border-b border-slate-200 shrink-0 gap-4 w-full">
        <div className="flex items-center gap-6">
          <div 
            onClick={() => setCurrentView('landing')}
            className="flex items-center gap-3 font-bold text-lg tracking-wide cursor-pointer hover:opacity-75 transition-opacity text-slate-900"
          >
            <img src="/image.jpg.jpg" alt="Official Emblem" className="h-10 w-auto mix-blend-multiply" />
            <span>RTI Auto-Drafter</span>
          </div>
          
          <div className="hidden md:flex items-center gap-5 text-sm font-medium text-slate-500 border-l border-slate-200 pl-6">
            <button 
              onClick={() => setCurrentView('database')}
              className="flex items-center gap-1.5 hover:text-slate-900 transition-colors"
            >
              <Database size={16} /> All Complaints (DB)
            </button>
            <button 
              onClick={() => setCurrentView('app')}
              className="flex items-center gap-1.5 hover:text-slate-900 transition-colors"
            >
              <MessageSquare size={16} /> AI Assistant
            </button>
            {/* Functional New Case Button */}
            <button 
              onClick={resetApp}
              className="flex items-center gap-1.5 text-blue-700 bg-blue-50 px-3 py-1.5 rounded-md hover:bg-blue-100 transition-colors"
            >
              <PlusCircle size={16} /> New Case
            </button>
          </div>
        </div>

        <div className="hidden lg:flex items-center gap-2 text-sm font-medium">
          <span className={appState === 'empty' ? 'text-blue-600 font-bold' : 'text-slate-400'}>1. Describe</span>
          <ChevronLeft size={14} className="text-slate-300 rotate-180" />
          <span className={appState === 'loading' ? 'text-blue-600 font-bold' : (appState === 'result' ? 'text-slate-900' : 'text-slate-400')}>2. Review</span>
          <ChevronLeft size={14} className="text-slate-300 rotate-180" />
          <span className={appState === 'result' ? 'text-blue-600 font-bold' : 'text-slate-400'}>3. Download</span>
        </div>
      </nav>

      <div className="flex flex-col lg:flex-row flex-1 overflow-hidden w-full relative">
        
        {/* LEFT COLUMN */}
        <div className="w-full lg:w-[40%] p-6 lg:p-10 flex flex-col border-r border-slate-200 bg-white overflow-y-auto z-10 relative">
          
          <h1 className="text-2xl font-bold mb-2 text-slate-900">Describe the Issue</h1>
          <p className="text-slate-500 mb-6 text-sm leading-relaxed">
            Explain the problem in your own words. Don't worry about legal formatting.
          </p>

          <div className="flex flex-wrap gap-2 mb-4">
            {suggestions.map((chip, idx) => (
              <button 
                key={idx}
                onClick={() => setComplaint(chip)}
                className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs text-slate-600 hover:border-blue-600 hover:bg-blue-50 hover:text-blue-700 transition-colors font-medium"
              >
                {chip}
              </button>
            ))}
          </div>
          
          <textarea
            className="w-full p-4 bg-slate-50 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-100 focus:border-blue-500 min-h-[160px] resize-none text-slate-900 placeholder-slate-400 transition-all"
            placeholder="e.g., The streetlights outside my college have been broken for two months..."
            value={complaint}
            onChange={(e) => setComplaint(e.target.value)}
            disabled={appState === 'loading'}
          />
          
          <div className="flex flex-col gap-1 mt-2">
            <p className="text-slate-500 text-xs flex items-center gap-1.5 font-medium">
              <AlertCircle size={14} className="text-blue-500 shrink-0" />
              We'll ask 1-2 follow-up questions if needed before drafting.
            </p>
            {complaint.length > 0 && complaint.length < 20 && (
              <p className="text-orange-500 text-xs font-medium pl-[22px]">
                Add a bit more detail ({complaint.length}/20 characters minimum)
              </p>
            )}
          </div>

          <div className="mt-8 border-t border-slate-100 pt-6">
            {!showAttachment ? (
              <button 
                onClick={() => setShowAttachment(true)}
                className="flex items-center gap-2 text-sm text-slate-600 hover:text-blue-600 transition-colors font-medium"
              >
                <Paperclip size={16} /> Optional: attach a related notice or reply you received
              </button>
            ) : (
              <div className="animate-in fade-in slide-in-from-top-2 duration-300">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-slate-900">Supporting Document</span>
                  <button 
                    onClick={() => {
                      if (file) setFile(null);
                      else setShowAttachment(false);
                    }} 
                    className="text-xs font-semibold text-slate-400 hover:text-slate-900 transition-colors"
                  >
                    {file ? "Remove" : "Skip for now"}
                  </button>
                </div>
                <div 
                  className="p-6 border-2 border-dashed border-slate-300 rounded-lg bg-slate-50 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50/50 transition-colors"
                  onClick={() => fileInputRef.current?.click()}
                >
                  <UploadCloud className="mx-auto text-slate-400 mb-2" size={24} />
                  <p className="text-sm font-medium text-slate-900">Drag & drop a legal document</p>
                  <input 
                    type="file" 
                    className="hidden" 
                    ref={fileInputRef}
                    onChange={(e) => setFile(e.target.files[0])} 
                  />
                  {file && <p className="text-blue-600 text-sm mt-3 font-semibold">{file.name}</p>}
                </div>
              </div>
            )}
          </div>

          <div className="mt-6">
            <button 
              onClick={generateRTI}
              disabled={complaint.length < 20 || appState === 'loading'}
              className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-200 disabled:text-slate-400 disabled:border-transparent text-white font-semibold py-3.5 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:shadow-none"
            >
              {appState === 'loading' ? <Loader2 className="animate-spin" size={20} /> : <Send size={20} />}
              {appState === 'loading' ? 'Drafting...' : 'Generate Application'}
            </button>
            
            <p className="text-center text-slate-400 text-xs mt-4 leading-relaxed max-w-[90%] mx-auto font-medium flex items-center justify-center gap-1.5">
              <Scale size={14} className="text-slate-400 shrink-0" strokeWidth={2} />
              <span>This is a drafting aid, not legal advice — review before submitting.</span>
            </p>
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="w-full lg:w-[60%] p-6 lg:p-10 bg-slate-50 flex flex-col overflow-y-auto relative z-0">
          
          <Scale className="absolute -top-16 -right-16 w-96 h-96 text-slate-900 opacity-5 pointer-events-none" strokeWidth={1} />

          {appState === 'empty' && (
            <div className="w-full max-w-2xl bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden relative z-10">
              <div className="p-8 text-center bg-white border-b border-slate-100">
                <div className="mx-auto w-16 h-16 bg-blue-50 text-slate-900 rounded-full flex items-center justify-center mb-6 border border-blue-100">
                  <Scale size={32} strokeWidth={1.5} />
                </div>
                <h2 className="text-xl font-bold mb-3 text-slate-900">Ready to Draft</h2>
                <p className="text-slate-500 text-sm leading-relaxed font-medium max-w-sm mx-auto">
                  Describe your issue on the left. We'll generate a formally structured RTI application addressed to the correct government department.
                </p>
              </div>
              
              <div className="p-8 bg-slate-50/50 opacity-60 select-none pointer-events-none">
                <div className="border-2 border-dashed border-slate-200 rounded-xl p-6 bg-white">
                  <div className="flex items-center gap-2 mb-6 text-slate-400">
                    <Gavel size={16} className="text-slate-900" strokeWidth={2} />
                    <span className="text-xs font-bold uppercase tracking-wider">Draft Preview</span>
                  </div>
                  
                  <div className="space-y-6">
                    <div>
                      <div className="h-2 w-8 bg-slate-300 rounded mb-2"></div>
                      <div className="h-3 w-48 bg-slate-200 rounded mb-1"></div>
                      <div className="h-3 w-32 bg-slate-200 rounded"></div>
                    </div>
                    <div>
                      <div className="h-2 w-12 bg-slate-300 rounded mb-2"></div>
                      <div className="h-3 w-full max-w-md bg-slate-200 rounded"></div>
                    </div>
                    <div className="pt-2 space-y-3">
                      <div className="h-2 w-full bg-slate-200 rounded"></div>
                      <div className="h-2 w-full bg-slate-200 rounded"></div>
                      <div className="h-2 w-5/6 bg-slate-200 rounded"></div>
                      <div className="h-2 w-4/5 bg-slate-200 rounded"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {appState === 'loading' && (
            <div className="max-w-2xl w-full relative z-10">
              <div className="flex items-center gap-3 mb-8 text-blue-600">
                <Loader2 className="animate-spin" size={20} />
                <span className="font-bold">{loadingMessage}</span>
              </div>
              <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm animate-pulse">
                <div className="h-4 bg-slate-200 rounded w-1/3 mb-8"></div>
                <div className="h-6 bg-slate-200 rounded w-3/4 mb-4"></div>
                <div className="space-y-3">
                  <div className="h-3 bg-slate-100 rounded w-full"></div>
                  <div className="h-3 bg-slate-100 rounded w-5/6"></div>
                  <div className="h-3 bg-slate-100 rounded w-full"></div>
                  <div className="h-3 bg-slate-100 rounded w-4/5"></div>
                </div>
              </div>
            </div>
          )}

          {appState === 'result' && (
            <div className="max-w-3xl w-full flex flex-col h-full animate-in fade-in duration-500 relative z-10">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-slate-900">
                <Gavel className="text-slate-900" size={24} /> Review & Edit
              </h2>
              
              <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex-1 mb-6">
                
                <div className="mb-5">
                  <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">To Department</label>
                  <input 
                    type="text"
                    value={docData.department}
                    onChange={(e) => setDocData({...docData, department: e.target.value})}
                    className="w-full bg-slate-50 text-slate-900 p-3 rounded border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none font-medium transition-shadow"
                  />
                </div>

                <div className="mb-5">
                  <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Subject</label>
                  <input 
                    type="text"
                    value={docData.subject}
                    onChange={(e) => setDocData({...docData, subject: e.target.value})}
                    className="w-full bg-slate-50 text-slate-900 p-3 rounded border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none font-medium transition-shadow"
                  />
                </div>

                <div className="mb-2 h-[250px]">
                  <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Application Body</label>
                  <textarea 
                    value={docData.body}
                    onChange={(e) => setDocData({...docData, body: e.target.value})}
                    className="w-full h-full bg-slate-50 text-slate-700 p-4 rounded border border-slate-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none resize-none leading-relaxed transition-shadow"
                  />
                </div>
              </div>

              <div className="flex flex-wrap gap-4 shrink-0">
                <button 
                  onClick={handleDownload}
                  className="flex-1 min-w-[200px] flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors shadow-md"
                >
                  <Download size={18} /> Download as PDF
                </button>
                <button 
                  onClick={() => navigator.clipboard.writeText(docData.body)}
                  className="flex items-center justify-center gap-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-semibold py-3 px-6 rounded-lg transition-colors shadow-sm"
                >
                  <Copy size={18} /> Copy Text
                </button>
                <button 
                  onClick={resetApp}
                  className="flex items-center justify-center gap-2 bg-white hover:bg-slate-50 border border-slate-300 text-slate-700 font-semibold py-3 px-6 rounded-lg transition-colors shadow-sm ml-auto"
                >
                  <RefreshCcw size={18} /> Start Over
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;