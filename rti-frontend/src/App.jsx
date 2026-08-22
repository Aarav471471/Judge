import { useState } from 'react';

function App() {
  const [complaint, setComplaint] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const generateRTI = async () => {
    if (!complaint) return;
    setLoading(true);
    
    try {
      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          complaint_text: complaint,
          applicant_id: "IIT2025002"
        })
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error("Error generating RTI:", error);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/download_pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ applicant_id: "IIT2025002" })
      });
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'RTI_Application.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error("Error downloading PDF:", error);
    }
  };

  return (
    <div className="flex h-screen bg-[#0D1117] text-white font-sans">
      
      {/* Left Panel: Conversational Input */}
      <div className="w-1/3 p-8 border-r border-gray-800 flex flex-col justify-center">
        <h1 className="text-3xl font-bold mb-2">RTI Auto-Drafter</h1>
        <p className="text-gray-400 mb-8 text-sm">Describe your civic issue in plain language, and our AI will draft the legal request.</p>
        
        <textarea
          className="w-full p-4 bg-[#323744] rounded-lg border border-gray-700 focus:outline-none focus:border-blue-500 min-h-[150px] mb-4"
          placeholder="e.g., The streetlights outside my college have been broken for two months..."
          value={complaint}
          onChange={(e) => setComplaint(e.target.value)}
        ></textarea>
        
        <button 
          onClick={generateRTI}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
        >
          {loading ? 'Drafting Legal Notice...' : 'Generate RTI Application'}
        </button>
      </div>

      {/* Right Panel: Document Preview */}
      <div className="w-2/3 p-8 bg-[#161B22] overflow-y-auto">
        {response ? (
          <div className="bg-[#323744] p-8 rounded-lg shadow-xl border border-gray-700 max-w-3xl mx-auto">
            <h2 className="text-xl font-bold mb-4 border-b border-gray-600 pb-2">Drafted RTI Application</h2>
            
            <div className="mb-6">
              <span className="text-gray-400 text-sm font-semibold uppercase">Target Department:</span>
              <p className="text-lg font-medium text-blue-400">{response.department_identified}</p>
            </div>

            {response.missing_info && response.missing_info.length > 0 && (
              <div className="mb-6 bg-yellow-900/30 border border-yellow-700 p-4 rounded text-yellow-200">
                <h3 className="font-bold mb-2">Action Required - Missing Details:</h3>
                <ul className="list-disc pl-5">
                  {response.missing_info.map((info, idx) => (
                    <li key={idx}>{info}</li>
                  ))}
                </ul>
              </div>
            )}

            <div>
              <span className="text-gray-400 text-sm font-semibold uppercase">Document Preview:</span>
              <pre className="whitespace-pre-wrap mt-2 text-gray-200 font-mono text-sm">
                
                {response.rti_draft_preview}
              </pre>
              
              <button 
                onClick={downloadPDF}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-lg"
              >
                Download Print-Ready PDF
              </button>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-600">
            <p>Your drafted document will appear here.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;