import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("import { useState, useRef } from 'react';", "import { useState, useRef, useEffect } from 'react';")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("useEffect imported successfully.")
