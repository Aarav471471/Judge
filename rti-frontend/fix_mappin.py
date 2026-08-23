import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

if "MapPin" not in text[:500]:
    # Use regex to insert MapPin into the lucide-react import list
    text = re.sub(r'import\s*\{\s*', 'import { MapPin, ', text, count=1)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("MapPin imported.")
