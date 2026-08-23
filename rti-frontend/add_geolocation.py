import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add isLocating state
text = text.replace(
    "const [pincode, setPincode] = useState('');",
    "const [pincode, setPincode] = useState('');\n  const [isLocating, setIsLocating] = useState(false);"
)

# 2. Add handleGetCurrentLocation
location_logic = """
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
  };
"""
text = text.replace(
    "const generateRTI = async",
    location_logic + "\n  const generateRTI = async"
)

# 3. Modify generateRTI finalPayload logic
old_payload = """    if (textToUse === complaint && pincode.length === 6 && locationDetails && !locationDetails.includes('Invalid') && !locationDetails.includes('Failed')) {
       finalPayload = `[Location Context: PIN ${pincode}, ${locationDetails}] ` + textToUse;
    }"""
new_payload = """    if (textToUse === complaint && locationDetails && !locationDetails.includes('Invalid') && !locationDetails.includes('Failed')) {
       finalPayload = `[Location Context: ${pincode ? 'PIN ' + pincode + ', ' : ''}${locationDetails}] ` + textToUse;
    }"""
text = text.replace(old_payload, new_payload)

# 4. Modify the UI label to include the button
old_label = """                    <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest mb-2">PIN Code</label>"""
new_label = """                    <div className="flex justify-between items-center mb-2">
                      <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-widest">PIN Code (Optional)</label>
                      <button onClick={handleGetCurrentLocation} className="text-[10px] text-indigo-600 font-bold hover:text-indigo-800 flex items-center gap-1 bg-indigo-50 px-2 py-0.5 rounded transition-colors active:scale-95">
                        {isLocating ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />} Auto-Locate
                      </button>
                    </div>"""
text = text.replace(old_label, new_label)

# 5. Fix MapPin import just in case
if "MapPin" not in text[:500]:
    text = text.replace("import { Mail", "import { MapPin, Mail")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Geolocation added.")
