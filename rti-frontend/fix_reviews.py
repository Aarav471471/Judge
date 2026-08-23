import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract the Reviews Section
start_marker = "{/* Reviews Section */}"
# The reviews section goes until the end of its div.
# Looking at my previous injection:
'''
        {/* Reviews Section */}
        <div className="max-w-6xl mx-auto px-6 py-24 border-t border-white/10">
...
        </div>
'''
start_idx = text.find(start_marker)

# Find the end of it. The reviews section was injected right before:
#       </div>
#     </div>
#   );
end_marker = '      </div>\n    </div>\n  );'
end_idx = text.rfind(end_marker)

# Actually, let's just find the exact string I injected.
reviews_html = """
        {/* Reviews Section */}
        <div className="max-w-6xl mx-auto px-6 py-24 border-t border-white/10">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Trusted by Citizens Across India</h2>
            <p className="text-zinc-400 font-medium text-lg">See how CivicAction is helping ordinary people cut through red tape.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {name: "Priya S.", loc: "Bangalore", review: "I spent 6 months trying to get my streetlights fixed. I drafted one RTI using CivicAction and they were repaired in 14 days. Absolutely incredible tool."},
              {name: "Rajesh K.", loc: "Delhi", review: "The Rights Navigator is a gamechanger. When my landlord tried to evict me illegally, I showed him the exact legal clauses the AI gave me. He backed down immediately."},
              {name: "Anil M.", loc: "Mumbai", review: "I had no idea I was eligible for the housing scheme until I used this app. It guided me step-by-step and even drafted the application for me. Highly recommended!"}
            ].map((r, i) => (
              <div key={i} className="bg-zinc-900/50 p-8 rounded-2xl border border-white/10 backdrop-blur-sm flex flex-col justify-between hover:border-blue-500/30 transition-colors">
                <div className="text-zinc-300 font-medium leading-relaxed mb-6">"{r.review}"</div>
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-blue-900/30 border border-blue-500/20 flex items-center justify-center text-blue-400 font-bold">{r.name[0]}</div>
                  <div>
                    <div className="font-bold text-white text-sm">{r.name}</div>
                    <div className="text-xs font-semibold text-zinc-500">{r.loc}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>"""

# Remove it from the bottom
text = text.replace(reviews_html, "")

# Insert it at the end of the landing page
landing_end = """              Start Drafting Now <ArrowRight size={20} />
            </button>
          </div>
        </main>
      </div>
    );
  }"""

new_landing_end = f"""              Start Drafting Now <ArrowRight size={20} />
            </button>
          </div>
{reviews_html}
        </main>
      </div>
    );
  }}"""

text = text.replace(landing_end, new_landing_end)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Reviews moved to landing page.")
