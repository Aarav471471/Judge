import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("Start Drafting Now <ArrowRight size=20 />", "Start Drafting Now <ArrowRight size={20} />")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed JSX parser error.")
