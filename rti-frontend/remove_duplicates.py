import re

app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove duplicate handleSummarize
def remove_duplicate_func(func_name, code):
    pattern = rf'  const {func_name} = async \(\) => {{[\s\S]*?catch \(error\) {{[\s\S]*?alert\("Failed to analyze document."\);[\s\S]*?setSummaryState\(\'empty\'\);[\s\S]*?\}}[\s\S]*?\}};?'
    # Find all occurrences
    matches = list(re.finditer(pattern, code))
    if len(matches) > 1:
        # Keep the last one, remove the rest
        for m in reversed(matches[:-1]): # Remove everything except the last match
            code = code[:m.start()] + code[m.end():]
    return code

text = remove_duplicate_func('handleSummarize', text)

# 2. Remove duplicate states
states_to_dedup = [
    r'const \[summaryFile, setSummaryFile\] = useState\(null\);\n',
    r'const \[summaryState, setSummaryState\] = useState\([\'"]empty[\'"]\);\n',
    r'const \[summaryData, setSummaryData\] = useState\(null\);\n'
]

for pat in states_to_dedup:
    matches = list(re.finditer(pat, text))
    if len(matches) > 1:
        for m in reversed(matches[:-1]):
            text = text[:m.start()] + text[m.end():]

# Clean up empty comments that might be left behind like `// --- Summarizer State ---`
text = re.sub(r'// --- Summarizer State ---\s*\n(?=\s*// ---)', '', text)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Duplicates removed.")
