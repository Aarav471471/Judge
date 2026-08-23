import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# I will replace the graphic block entirely
# Currently it is inside `{/* Right Side: Graphic */}`
start_marker = "{/* Right Side: Graphic */}"
end_marker = "          </div>\n\n          {/* Stats Section */}"
start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

new_graphic = """{/* Right Side: Graphic */}
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
            </div>"""

text = text[:start_idx] + new_graphic + text[end_idx:]

# Ensure overflow-x-hidden on the main min-h-screen wrapper to prevent horizontal scrolling
wrapper_start = '<div className="min-h-screen w-full bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">'
wrapper_end = '<div className="min-h-screen w-full overflow-x-hidden bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">'
text = text.replace(wrapper_start, wrapper_end)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Right side graphic redesigned with flex logic.")
