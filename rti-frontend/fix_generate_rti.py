import re

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# I will use a regex to replace the start of `generateRTI` up to `try {`
# Current:
'''
  const generateRTI = async (textToUse = complaint) => {
    if (textToUse.length < 20) return;
    setAppState('loading');
    setLoadingMessage('AI is analyzing and drafting your request...');
    
    try {
'''

old_pattern = r"const generateRTI = async \(textToUse = complaint\) => \{[\s\S]*?try \{"

new_gen = """const generateRTI = async (textToUse = complaint) => {
    if (textToUse.length < 20) return;
    setAppState('loading');
    setLoadingMessage('AI is analyzing and drafting your request...');
    
    let finalPayload = textToUse;
    if (textToUse === complaint && pincode.length === 6 && locationDetails && !locationDetails.includes('Invalid') && !locationDetails.includes('Failed')) {
       finalPayload = `[Location Context: PIN ${pincode}, ${locationDetails}] ` + textToUse;
    }
    
    try {"""

text = re.sub(old_pattern, new_gen, text, count=1)

# I also need to update the body: JSON.stringify({ complaint_text: textToUse... }) to use finalPayload
text = text.replace("complaint_text: textToUse,", "complaint_text: finalPayload,")

with open(r'c:\oosc\Judge\rti-frontend\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("generateRTI payload fixed!")
