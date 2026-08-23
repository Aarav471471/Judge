import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

old_str = '              {appState === \'interview\' && (\n                <div className="flex flex-col h-full p-8 lg:p-16 animate-subtle max-w-3xl mx-auto w-full justify-center">'
new_str = '              {appState === \'interview\' && (\n                <div className="flex flex-col py-12 px-8 lg:px-16 animate-subtle max-w-3xl mx-auto w-full">'

text = text.replace(old_str, new_str)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed clipping issue.")
