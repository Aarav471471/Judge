import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extract the summarizer Right View block that is misplaced
start_tag = "          {activeTab === 'summarizer' && ("
end_tag = "          )}\n"

# The block is right after {/* RIGHT COLUMN: Output */}
marker = "{/* RIGHT COLUMN: Output */}\n"
start_idx = text.find(marker) + len(marker)

# Find where it ends
# The block ends before `<div className="w-full lg:w-[55%] xl:w-[60%] h-full flex flex-col bg-[#F9FAFB] hide-scroll overflow-y-auto relative">`
end_idx = text.find('<div className="w-full lg:w-[55%]', start_idx)

misplaced_block = text[start_idx:end_idx]

# Remove the misplaced block from there
new_text = text[:start_idx] + text[end_idx:]

# Now insert it INSIDE the right column, just after the noise.svg div
noise_div = "<div className=\"absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] pointer-events-none mix-blend-overlay\"></div>"
noise_idx = new_text.find(noise_div) + len(noise_div)

final_text = new_text[:noise_idx] + "\n" + misplaced_block + new_text[noise_idx:]

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Layout nesting perfectly fixed!")
