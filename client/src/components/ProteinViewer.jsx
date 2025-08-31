import React, { useEffect, useRef } from "react";

const ProteinViewer = ({ pdbData }) => {
  const viewerRef = useRef(null);

  // Helper function to get PDB content as string
  const getPdbContent = (pdbItem) => {
    if (typeof pdbItem === 'string') {
      return pdbItem;
    } else if (pdbItem && typeof pdbItem === 'object') {
      return pdbItem.pdb_content || pdbItem.content || pdbItem.data || 
             pdbItem.structure || JSON.stringify(pdbItem);
    }
    return String(pdbItem);
  };

  useEffect(() => {
    if (!pdbData || !viewerRef.current || !window.$3Dmol) return;

    // Clear previous content
    viewerRef.current.innerHTML = "";

    // Calculate grid dimensions
    const numStructures = pdbData.length;
    const rows = Math.ceil(Math.sqrt(numStructures));
    const cols = Math.ceil(numStructures / rows);

    // Create viewer grid configuration
    const config = {
      rows: rows,
      cols: cols,
      control_all: true,
    };

    const viewer_config = { 
      backgroundColor: 'white' 
    };

    // Create the viewer grid
    const viewers = window.$3Dmol.createViewerGrid(viewerRef.current, config, viewer_config);

    // Load each PDB structure into its respective viewer cell
    pdbData.forEach((data, index) => {
      const row = Math.floor(index / cols);
      const col = index % cols;
      
      if (viewers[row] && viewers[row][col]) {
        const viewer = viewers[row][col];
        const pdbContent = getPdbContent(data);
        viewer.addModel(pdbContent, "pdb");
        viewer.setStyle({}, { cartoon: { color: 'spectrum' } });
        viewer.zoomTo();
        viewer.render();
      }
    });

  }, [pdbData]);

  return (
    <div>
      <h2>3D Protein Structures ({pdbData.length} results)</h2>
      <div
        ref={viewerRef}
        style={{ 
          width: "100%", 
          height: "600px", 
          border: "1px solid #ccc",
          display: "grid",
          gridTemplateColumns: `repeat(${Math.ceil(Math.sqrt(pdbData?.length || 1))}, 1fr)`,
          gap: "10px"
        }}
      />
    </div>
  );
};

export default ProteinViewer;