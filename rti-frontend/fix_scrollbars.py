import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the problematic wrapper classes
old_wrapper = '<div className="min-h-screen w-full overflow-x-hidden bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">'
new_wrapper = '<div className="min-h-screen bg-[#f8f9fa] text-slate-900 font-sans flex flex-col selection:bg-[#e0e0ff] selection:text-[#3b36e8]">\n        <style>{`body, html { overflow-x: hidden; margin: 0; padding: 0; }`}</style>'
text = text.replace(old_wrapper, new_wrapper)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Scrollbars fixed!")
