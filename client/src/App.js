import React, { useState } from 'react';
import './App.css';

function App() {
  const [sequence, setSequence] = useState('');
  const [error, setError] = useState('');
  const [iframes, setIframes] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIframes([]);

    if (!sequence) {
      setError('Please enter a sequence!');
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/fetch_pdb", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fold_seq: sequence })
      });

      const data = await res.json();
      if (data.status === "success" && data.pdb_data) {
        const pdbArray = Array.isArray(data.pdb_data) ? data.pdb_data : [data.pdb_data];
        
        // Create iframe elements
        const newIframes = pdbArray.map((item, idx) => {
          const iframeId = `protein-iframe-${idx}`;
          
          // Create iframe and set up message handler after it loads
          setTimeout(() => {
            const iframe = document.getElementById(iframeId);
            if (iframe) {
              iframe.onload = () => {
                iframe.contentWindow.postMessage({
                  pdb: item.pdb_data,
                  sequence: item.sequence,
                  name: `Protein ${idx + 1}`,
                  tm_score: data.tm_scores[idx],
                  description: data.description[idx]
                }, "*");
              };
            }
          }, 100);
          
          return {
            id: iframeId,
            key: idx
          };
        });
        
        setIframes(newIframes);
      } else {
        setError('Failed to fetch PDB data.');
      }
    } catch (err) {
      console.error(err);
      setError('Error fetching PDB.');
    }
  };

  return (
    <div className="App">
      <h1>Protein Folding Viewer (iFrame Version)</h1>

      <form onSubmit={handleSubmit}>
        <textarea 
          id="sequence"
          rows="5" 
          cols="60" 
          placeholder="Enter protein sequence..."
          value={sequence}
          onChange={(e) => setSequence(e.target.value)}
        ></textarea>
        <br />
        <button type="submit">Submit</button>
      </form>

      {error && <div id="error" style={{color: 'red'}}>{error}</div>}
      
      <div id="iframe-container">
        {iframes.map(iframe => (
          <iframe
            key={iframe.key}
            id={iframe.id}
            src="/sample.html" // This should be in your public folder
            title="Protein Viewer"
            style={{
              border: '1px solid #ccc',
              margin: '20px auto',
              width: '90vw',
              height: '360px',
              display: 'block'
            }}
          ></iframe>
        ))}
      </div>
    </div>
  );
}

export default App;