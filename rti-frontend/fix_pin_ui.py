import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

old_pin_block = """                      <div>
                        <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2 mb-2">
                          <span className="bg-red-100 text-red-600 px-1.5 py-0.5 rounded text-[9px]">Required</span>
                          Area PIN Code
                        </label>
                        <div className="relative">"""

new_pin_block = """                      <div>
                        <div className="flex items-center justify-between mb-2">
                          <label className="text-[11px] font-bold text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                            <span className="bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded text-[9px]">Optional</span>
                            Area PIN Code
                          </label>
                          <button onClick={handleGetCurrentLocation} className="text-[10px] text-blue-600 font-bold hover:text-blue-800 flex items-center gap-1 bg-blue-50 px-2 py-1 rounded transition-colors active:scale-95 shadow-sm border border-blue-100">
                            {isLocating ? <Loader2 size={12} className="animate-spin" /> : <MapPin size={12} />} Auto-Locate
                          </button>
                        </div>
                        <div className="relative">"""

if old_pin_block in text:
    text = text.replace(old_pin_block, new_pin_block)
else:
    print("WARNING: Could not find the PIN block to replace!")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("PIN code block updated in UI!")
