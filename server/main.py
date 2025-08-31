import uvicorn
import os
import random
import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fetch_protein import fetch_pdb
from dssp_serve import run_dssp
from fetch_biosimilars import generate_biosimilars_async
from model_loader import model_loader
from tm_mech import compute_tm_score
from dssp_analyse import analyze_pdb_full
import asyncio
import hashlib

app = FastAPI()

# Load model at application startup
@app.on_event("startup")
async def startup_event():
    """Load the model when the application starts"""
    print("Loading ProtGPT2 model...")
    model_loader.load_model()
    print("Application startup complete")

# allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FoldSeqRequest(BaseModel):
    fold_seq: str

@app.post("/fetch_pdb")
async def fetch_pdb_endpoint(req: FoldSeqRequest):
    """
    Generate biosimilars, fetch PDBs, compute TM-score vs original PDB,
    and generate natural-language descriptions for each protein.
    """
    try:
        # 1️⃣ Fetch original PDB for the input fold sequence
        success_orig, original_pdb = await fetch_pdb(req.fold_seq)
        if not success_orig or not original_pdb:
            raise HTTPException(status_code=400, detail="Failed to fetch original PDB for input sequence")

        # Get the file path for the original PDB
        orig_file_hash = hashlib.sha256(req.fold_seq.encode()).hexdigest()
        orig_pdb_path = os.path.join("pdb_data", f"{orig_file_hash}.pdb")

        # 2️⃣ Generate biosimilars
        biosimilars = await generate_biosimilars_async(model_loader, req.fold_seq)

        pdb_results = []
        tm_scores = []
        descriptions = []

        for i, seq in enumerate(biosimilars):
            print(f"Fetching PDB for sequence {i+1}: {seq}")

            # Add 1-second delay between requests
            if i > 0:
                await asyncio.sleep(1)

            try:
                success, pdb_content = await fetch_pdb(seq)
                if success and pdb_content:
                    # File path for the generated PDB
                    seq_file_hash = hashlib.sha256(seq.encode()).hexdigest()
                    seq_pdb_path = os.path.join("pdb_data", f"{seq_file_hash}.pdb")

                    # Compute TM-score
                    try:
                        tm_score = await compute_tm_score(
                            pdb1_filename=f"{seq_file_hash}.pdb",
                            pdb2_filename=f"{orig_file_hash}.pdb",
                            pdb_dir="pdb_data"
                        )
                    except Exception as e:
                        print(f"❌ Error computing TM-score for sequence {i+1}: {e}")
                        tm_score = 0.0

                    # Generate natural-language description
                    try:
                        description = await analyze_pdb_full(seq_pdb_path)
                    except Exception as e:
                        print(f"❌ Error analyzing PDB for sequence {i+1}: {e}")
                        description = "Failed to generate description."

                    pdb_results.append({
                        "sequence": seq,
                        "pdb_data": pdb_content
                    })
                    tm_scores.append(tm_score)
                    descriptions.append(description)
                    print(f"✅ Sequence {i+1}: fetched PDB, TM-score={tm_score}, description generated")

                else:
                    print(f"❌ Failed to fetch PDB for sequence {i+1}")
                    descriptions.append("Failed to fetch PDB.")

            except Exception as e:
                print(f"❌ Error fetching PDB for sequence {i+1}: {e}")
                descriptions.append("Failed to fetch PDB.")
                continue

        # Return results
        return {
            "status": "success",
            "original_pdb": original_pdb,
            "pdb_data": pdb_results,
            "tm_scores": tm_scores,
            "description": descriptions,
            "total_generated": len(biosimilars),
            "successful_fetches": len(pdb_results),
            "failed_fetches": len(biosimilars) - len(pdb_results)
        }

    except HTTPException:
        raise
    except Exception as exc:
        print("Error in /fetch_pdb:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


    
@app.post("/fake_fetch_pdb")
async def fake_fetch_pdb_endpoint(req: FoldSeqRequest):
    """
    Fake endpoint that randomly loads PDB files from the pdb_data directory
    to save time during testing and development.
    """
    try:
        # Get list of all PDB files in the directory
        pdb_dir = "pdb_data"
        if not os.path.exists(pdb_dir):
            return {
                "status": "error",
                "message": "pdb_data directory not found"
            }
        
        pdb_files = [f for f in os.listdir(pdb_dir) if f.endswith('.pdb')]
        
        if not pdb_files:
            return {
                "status": "error",
                "message": "No PDB files found in pdb_data directory"
            }
        
        # Randomly select 2 PDB files (or fewer if not enough available)
        num_to_select = min(2, len(pdb_files))
        selected_files = random.sample(pdb_files, num_to_select)
        
        pdb_results = []
        for i, pdb_file in enumerate(selected_files):
            try:
                file_path = os.path.join(pdb_dir, pdb_file)
                
                # Read the PDB file content asynchronously
                async with aiofiles.open(file_path, 'r') as f:
                    pdb_content = await f.read()
                
                # Create a fake sequence based on the input or use a placeholder
                fake_sequence = req.fold_seq[:50] + f"_fake_{i+1}" if req.fold_seq else f"fake_sequence_{i+1}"
                
                pdb_results.append({
                    "sequence": fake_sequence,
                    "pdb_data": pdb_content
                })
                print(f"✅ Successfully loaded fake PDB from: {pdb_file}")
                
            except Exception as e:
                print(f"❌ Error reading PDB file {pdb_file}: {e}")
                continue

        # Return the fake results
        return {
            "status": "success",
            "pdb_data": pdb_results,
            "total_generated": len(pdb_results),
            "successful_fetches": len(pdb_results),
            "failed_fetches": 0,
            "note": "This is fake data loaded from local PDB files for testing"
        }

    except Exception as exc:
        print("Error in /fake_fetch_pdb:", exc)
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/check")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)