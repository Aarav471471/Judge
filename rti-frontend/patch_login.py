import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add `isIntercepting` state
text = text.replace(
    "const [loginStep, setLoginStep] = useState('mobile');",
    "const [loginStep, setLoginStep] = useState('mobile');\n  const [isIntercepting, setIsIntercepting] = useState(false);"
)

# 2. Update `handleSendOTP`
old_send_otp = """  const handleSendOTP = async () => {
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
      } else {
        setAuthError('Failed to send OTP. Try again.');
      }
    } catch (e) {
      setAuthError('Connection error.');
    }
  };"""

new_send_otp = """  const handleSendOTP = async () => {
    const rawMobile = mobileInput.replace(/\\D/g, '');
    if (rawMobile.length !== 10) {
      setAuthError('Please enter a valid 10-digit mobile number');
      return;
    }
    setAuthError('');
    try {
      const res = await fetch('http://127.0.0.1:8000/auth/send-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mobile_number: rawMobile })
      });
      if (res.ok) {
        const data = await res.json();
        setLoginStep('otp');
        if (data.dev_otp) {
          setIsIntercepting(true);
          setTimeout(() => {
            setOtpInput(data.dev_otp);
            setIsIntercepting(false);
          }, 1500);
        }
      } else {
        setAuthError('Failed to send OTP. Try again.');
      }
    } catch (e) {
      setAuthError('Connection error.');
    }
  };"""
text = text.replace(old_send_otp, new_send_otp)

# Update handleVerifyOTP to strip spaces just in case
text = text.replace(
    "body: JSON.stringify({ mobile_number: mobileInput, otp: otpInput })",
    "body: JSON.stringify({ mobile_number: mobileInput.replace(/\\D/g, ''), otp: otpInput.replace(/\\D/g, '') })"
)

# 3. Replace the entire login view block
start_marker = "if (currentView === 'login') {"
end_marker = "  // --- VIEW 1: LANDING PAGE ---"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

new_login = """if (currentView === 'login') {
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
                    value={mobileInput.replace(/\\D/g, '').replace(/(\\d{5})(\\d)/, '$1 $2')}
                    onChange={(e) => setMobileInput(e.target.value.replace(/\\D/g, ''))}
                    className="w-full pl-14 pr-4 py-4 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-[#3b36e8]/20 focus:border-[#3b36e8] focus:bg-white focus:outline-none transition-all font-semibold text-slate-900 text-lg"
                    placeholder="Enter 10-digit number"
                  />
                </div>
              </div>
              <button
                onClick={handleSendOTP}
                disabled={mobileInput.replace(/\\D/g, '').length !== 10}
                className="w-full bg-[#1e1b4b] hover:bg-[#2e2b5e] disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold py-4 rounded-xl transition-all shadow-lg active:scale-95 flex justify-center items-center gap-2 group"
              >
                Send Secure OTP <ArrowRight size={18} className={mobileInput.replace(/\\D/g, '').length === 10 ? 'group-hover:translate-x-1 transition-transform' : ''} />
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
                    onChange={(e) => setOtpInput(e.target.value.replace(/\\D/g, ''))}
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

"""

text = text[:start_idx] + new_login + text[end_idx:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Login page redesigned!")
