import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add States
state_code = """  const [pincode, setPincode] = useState('');
  const [locationDetails, setLocationDetails] = useState('');
  const [isFetchingPin, setIsFetchingPin] = useState(false);

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
"""

text = text.replace("const [complaint, setComplaint] = useState('');", "const [complaint, setComplaint] = useState('');\n" + state_code)

# 2. Modify generateRTI to include PIN code context
old_gen = """  const generateRTI = async (textToUse = complaint) => {
    setAppState('loading');
    setLoadingMessage('Drafting Document...');
    
    try {
      const res = await fetch('http://127.0.0.1:8000/draft-rti', {"""

new_gen = """  const generateRTI = async (textToUse = complaint) => {
    setAppState('loading');
    setLoadingMessage('Drafting Document...');
    
    let finalPayload = textToUse;
    if (textToUse === complaint && pincode.length === 6 && locationDetails && !locationDetails.includes('Invalid') && !locationDetails.includes('Failed')) {
       finalPayload = `[Location Context: PIN ${pincode}, ${locationDetails}]\n` + textToUse;
    }
    
    try {
      const res = await fetch('http://127.0.0.1:8000/draft-rti', {"""

text = text.replace(old_gen, new_gen)

old_body = """        body: JSON.stringify({ 
          complaint: textToUse,"""
new_body = """        body: JSON.stringify({ 
          complaint: finalPayload,"""
text = text.replace(old_body, new_body)

# 3. Add PIN code UI to Left Column of RTI Drafter
old_rti_left = """              <div className="flex-1 flex flex-col p-8 bg-zinc-50/30">
                <div className="mb-3 flex items-center justify-between">
                  <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest">Issue Description</label>
                </div>"""

new_rti_left = """              <div className="flex-1 flex flex-col p-8 bg-zinc-50/30">
                <div className="mb-6">
                  <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2 mb-2">
                    <span className="bg-zinc-200 text-zinc-600 px-1.5 py-0.5 rounded text-[9px]">Optional</span>
                    Area PIN Code
                  </label>
                  <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <svg className="h-4 w-4 text-zinc-400" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
                    </div>
                    <input 
                      type="text" 
                      placeholder="e.g. 110001" 
                      value={pincode}
                      onChange={handlePinChange}
                      maxLength="6"
                      className="w-full bg-white border border-zinc-200 rounded-xl py-3 pl-10 pr-4 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none transition-all text-sm font-semibold shadow-sm text-zinc-800 placeholder-zinc-400"
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

                <div className="mb-3 flex items-center justify-between mt-2">
                  <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest">Issue Description</label>
                </div>"""

text = text.replace(old_rti_left, new_rti_left)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("PIN code auto-fetch feature added to RTI Drafter.")
