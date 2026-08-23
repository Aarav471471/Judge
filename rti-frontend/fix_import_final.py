import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the incorrect import from 'react'
text = text.replace("import { MapPin, useState", "import { useState")

# Add MapPin to lucide-react correctly
text = text.replace("import { \n  Mail", "import { \n  MapPin, Mail")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Imports fixed!")
