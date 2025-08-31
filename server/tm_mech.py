import subprocess
import os
import re

async def compute_tm_score(pdb1_filename: str, pdb2_filename: str, pdb_dir: str = "pdb_data") -> float:
    """
    Computes TM-score between two PDB files using TM-align, with debug prints.
    """
    try:
        print(f"📌 Starting TM-score computation between {pdb1_filename} and {pdb2_filename}")
        pdb1_path = os.path.join(pdb_dir, pdb1_filename)
        pdb2_path = os.path.join(pdb_dir, pdb2_filename)
        print(f"Using paths:\n  pdb1: {pdb1_path}\n  pdb2: {pdb2_path}")

        # Check if files exist
        if not os.path.exists(pdb1_path):
            raise FileNotFoundError(f"PDB file not found: {pdb1_path}")
        if not os.path.exists(pdb2_path):
            raise FileNotFoundError(f"PDB file not found: {pdb2_path}")
        if not os.path.exists(".\\TMalign.exe"):
            raise FileNotFoundError("TMalign.exe not found in current directory")

        # Use subprocess.run instead of asyncio for simplicity
        cmd = [".\\TMalign.exe", pdb2_path, pdb1_path]
        print(f"Running command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd()  # Explicitly set working directory
        )

        if result.returncode != 0:
            raise RuntimeError(f"TM-align failed with return code {result.returncode}:\n{result.stderr}")

        print("📄 TM-align output:\n", result.stdout)

        match = re.search(r"TM-score=\s*([0-9.]+)\s*\(if normalized by length of Chain_1", result.stdout)
        if not match:
            raise ValueError(f"Could not parse TM-score from TM-align output")

        tm_score = float(match.group(1))
        print(f"✅ Computed TM-score: {tm_score}")
        return tm_score

    except Exception as e:
        print(f"❌ Error in compute_tm_score: {e}")
        raise