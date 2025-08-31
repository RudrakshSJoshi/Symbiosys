import React from "react";

const ResultsList = ({ sequence, pdbData }) => {
  // Helper function to safely get PDB content as string
  const getPdbContent = (pdbItem) => {
    if (typeof pdbItem === 'string') {
      return pdbItem;
    } else if (pdbItem && typeof pdbItem === 'object') {
      // Handle different possible object structures
      return pdbItem.pdb_content || pdbItem.content || pdbItem.data || 
             pdbItem.structure || JSON.stringify(pdbItem, null, 2);
    }
    return String(pdbItem);
  };

  // Calculate total size safely
  const calculateTotalSize = () => {
    try {
      const totalLength = pdbData.reduce((total, pdb) => {
        const content = getPdbContent(pdb);
        return total + (content ? content.length : 0);
      }, 0);
      return (totalLength / 1024).toFixed(2);
    } catch (error) {
      return "N/A";
    }
  };

  return (
    <div>
      <h2>Results</h2>
      <ul>
        <li>Sequence length: {sequence.length}</li>
        <li>Number of structures: {pdbData.length}</li>
        <li>Total PDB data size: {calculateTotalSize()} KB</li>
        <li>Status: Success ✅</li>
      </ul>
      
      {pdbData.length > 1 && (
        <div>
          <h3>Individual Structures</h3>
          {pdbData.map((pdb, index) => {
            const pdbContent = getPdbContent(pdb);
            return (
              <div key={index} style={{ marginBottom: '20px' }}>
                <h4>Structure {index + 1}</h4>
                <pre style={{ 
                  fontSize: '10px', 
                  background: '#f5f5f5', 
                  padding: '10px', 
                  overflow: 'auto',
                  maxHeight: '200px'
                }}>
                  {pdbContent ? pdbContent.substring(0, 500) + '...' : 'No PDB content available'}
                </pre>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ResultsList;