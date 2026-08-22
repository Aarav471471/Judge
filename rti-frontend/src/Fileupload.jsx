import { useState, useRef } from 'react';
import { UploadCloud } from 'lucide-react';

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  return (
    <div 
      className="mt-6 p-6 border-2 border-dashed border-gray-700 rounded-lg bg-[#161B22] text-center cursor-pointer hover:border-blue-500 transition-colors"
      onClick={() => fileInputRef.current.click()}
    >
      <UploadCloud className="mx-auto text-gray-500 mb-3" size={32} />
      <p className="text-sm text-gray-400">Drag & drop a legal document to analyze</p>
      <p className="text-xs text-gray-600 mt-1">or click to browse</p>
      
      <input 
        type="file" 
        className="hidden" 
        ref={fileInputRef}
        onChange={(e) => setFile(e.target.files[0])} 
      />
      
      {file && <p className="text-green-500 text-sm mt-3">{file.name} selected</p>}
    </div>
  );
}