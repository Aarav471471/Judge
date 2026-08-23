import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

stats_html = """
          {/* Stats Section */}
          <div className="w-full bg-white border-y border-zinc-200 py-16 relative z-10">
            <div className="max-w-5xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-12 text-center divide-y md:divide-y-0 md:divide-x divide-zinc-200">
              <div className="flex flex-col items-center justify-center pt-6 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="text-indigo-600" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">42,500<span className="text-indigo-600">+</span></span>
                </div>
                <div className="text-xs font-bold text-zinc-500 uppercase tracking-widest mt-1">Cases Drafted & Solved</div>
              </div>
              
              <div className="flex flex-col items-center justify-center pt-8 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <Shield className="text-blue-500" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">94<span className="text-blue-500">%</span></span>
                </div>
                <div className="text-xs font-bold text-zinc-500 uppercase tracking-widest mt-1">Resolution Success Rate</div>
              </div>
              
              <div className="flex flex-col items-center justify-center pt-8 md:pt-0">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="text-emerald-500" size={24} />
                  <span className="text-4xl md:text-5xl font-extrabold text-slate-900">4.9<span className="text-emerald-500">/5</span></span>
                </div>
                <div className="text-xs font-bold text-zinc-500 uppercase tracking-widest mt-1">Citizen Satisfaction Rating</div>
              </div>
            </div>
          </div>
"""

# Insert right after the Hero section
text = text.replace("          </div>\n\n          {/* Reviews Section */}", "          </div>\n" + stats_html + "\n          {/* Reviews Section */}")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Stats section injected.")
