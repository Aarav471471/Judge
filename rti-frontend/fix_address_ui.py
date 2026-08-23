import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_ui = '''                      <div>
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
                      </div>'''

pattern = r'<div>\s*<div className="flex items-center justify-between mb-2">\s*<label.*?Area PIN Code.*?</label>\s*<button.*?Auto-Locate\s*</button>\s*</div>\s*<div className="relative">\s*<input.*?/>\s*(?:\{isFetchingPin.*?</div\>\}\s*)?</div>\s*</div>'

if re.search(pattern, text, re.DOTALL):
    text = re.sub(pattern, new_ui, text, count=1, flags=re.DOTALL)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('Regex UI match replaced successfully!')
else:
    print('Failed to match UI pattern with regex')
