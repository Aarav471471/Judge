import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add Mail to the imports
text = text.replace("FileText, Send, Loader2,", "Mail, FileText, Send, Loader2,")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Mail imported successfully.")
