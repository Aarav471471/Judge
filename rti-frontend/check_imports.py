import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Find all JSX tags
used_tags = set(re.findall(r'<([A-Z][a-zA-Z0-9_]*)', text))

# 2. Find all imports
imported_vars = set()
for match in re.finditer(r'import\s+\{([^}]+)\}', text):
    parts = match.group(1).split(',')
    for p in parts:
        if p.strip():
            imported_vars.add(p.strip())

# Add React hooks to imported
react_imports = set(['useState', 'useEffect', 'useRef'])
imported_vars.update(react_imports)

# Are there any Capitalized tags used that aren't imported?
# Note: we might have local components.
local_components = set(re.findall(r'(?:const|function)\s+([A-Z][a-zA-Z0-9_]*)', text))

missing = used_tags - imported_vars - local_components
print("Missing Capitalized Components:", missing)

# Check for any undefined variables used in the script
# We can just look at the console log in the browser, but we can't.
