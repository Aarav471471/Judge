import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Start Over for RTI Drafter
text = text.replace(
    "onClick={() => setAppState('empty')}", 
    "onClick={() => { setAppState('empty'); setComplaint(''); setMissingInfo([]); setInterviewAnswers({}); setPincode(''); setLocationDetails(''); setApplicantName(''); }}"
)

# Fix Start Over for Rights Navigator
text = text.replace(
    "onClick={() => setRightsState('empty')}", 
    "onClick={() => { setRightsState('empty'); setRightsSituation(''); }}"
)

# Fix Start Over for Schemes
text = text.replace(
    "onClick={() => setSchemeState('empty')}", 
    "onClick={() => { setSchemeState('empty'); setSchemeProfile({age:'', gender:'Male', income:'', occupation:'', state:''}); }}"
)

# Fix Start Over for Summarizer
text = text.replace(
    "onClick={() => setSummaryState('empty')}", 
    "onClick={() => { setSummaryState('empty'); setSummaryFile(null); setSummaryData(null); }}"
)

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Start Over buttons reset logic fixed.")
