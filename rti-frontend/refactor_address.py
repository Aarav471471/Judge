import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. State changes
text = text.replace(
    "const [pincode, setPincode] = useState('');",
    "const [address, setAddress] = useState('');"
)

# 2. handleGetCurrentLocation update
old_loc = """  const handleGetCurrentLocation = () => {
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
        
        if (data && data.address) {
          const pin = data.address.postcode || '';
          if (pin && pin.length === 6) {
             setPincode(pin);
             // The useEffect will automatically fetch the location details from postal API
          } else {
             // Fallback if no exact PIN but we have city/state
             const cityStr = data.address.city || data.address.county || data.address.town || data.address.suburb || '';
             const stateStr = data.address.state || '';
             setLocationDetails(`${cityStr}, ${stateStr}`.replace(/^, /, '').trim());
          }
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
  };"""

new_loc = """  const handleGetCurrentLocation = () => {
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
      }
      setIsLocating(false);
    }, () => {
      alert("Unable to retrieve your location. Please check browser permissions.");
      setIsLocating(false);
    });
  };"""
text = text.replace(old_loc, new_loc)


# 3. Payload update
old_payload = """    if (textToUse === complaint && locationDetails && !locationDetails.includes('Invalid') && !locationDetails.includes('Failed')) {
       finalPayload = `[Location Context: ${pincode ? 'PIN ' + pincode + ', ' : ''}${locationDetails}] ` + textToUse;
    }"""
new_payload = """    if (textToUse === complaint && address) {
       finalPayload = `[Applicant Address: ${address}] ` + textToUse;
    }"""
text = text.replace(old_payload, new_payload)


# 4. Button disabled update
text = text.replace(
    "disabled={!complaint || !applicantName}",
    "disabled={!complaint || !applicantName || !address}"
)


# 5. UI replace
old_ui = """                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                            <span className="bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded text-[9px]">Optional</span>
                            Area PIN Code
                          </label>
                          <button onClick={handleGetCurrentLocation} className="text-[10px] text-blue-600 font-bold hover:text-blue-800 flex items-center gap-1 bg-blue-50 px-2 py-1 rounded transition-colors active:scale-95 shadow-sm border border-blue-100">
                            {isLocating ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />} Auto-Locate
                          </button>
                        </div>
                        <div className="relative">
                          <input 
                            type="text" 
                            placeholder="e.g. 110001" 
                            value={pincode}
                            onChange={handlePinChange}
                            maxLength="6"
                            className="w-full bg-zinc-50 border border-zinc-200 rounded-xl py-3 pl-4 pr-10 focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 focus:outline-none transition-all text-sm font-semibold text-zinc-800 placeholder-zinc-400"
                          />
                          {isFetchingPin && <div className="absolute right-3 top-3"><Loader2 size={16} className="animate-spin text-zinc-400" /></div>}
                        </div>
                      </div>"""

new_ui = """                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                            <span className="bg-red-100 text-red-600 px-1.5 py-0.5 rounded text-[9px]">Required</span>
                            Full Address
                          </label>
                          <button onClick={handleGetCurrentLocation} className="text-[10px] text-blue-600 font-bold hover:text-blue-800 flex items-center gap-1 bg-blue-50 px-2 py-1 rounded transition-colors active:scale-95 shadow-sm border border-blue-100">
                            {isLocating ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />} Auto-Locate
                          </button>
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
                      </div>"""

if old_ui in text:
    text = text.replace(old_ui, new_ui)
else:
    print("Warning: Could not find exact UI block. Attempting regex...")
    text = re.sub(r'<div>\s*<div className="flex items-center justify-between mb-2">.*?Area PIN Code.*?</div>\s*</div>\s*</div>', new_ui, text, flags=re.DOTALL)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Refactored PIN to Address.")
