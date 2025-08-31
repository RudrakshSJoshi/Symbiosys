import asyncio
import os
from tm_mech import compute_tm_score

# Assuming compute_tm_score is defined in your environment or imported from a module
# If it's from a specific module, import it like:
# from your_module import compute_tm_score

async def main():
    seq_pdb_path = r"pdb_data\9fa4a42c9e49c5d2d273e3643fb9a0c943d2b6b25d58092546c9ed2f7f28b3fd.pdb"
    orig_pdb_path = r"pdb_data\eaf1f8d7f5bf78bbefe1100d912a09893361c57dda057f634adb5c5af6dfe79c.pdb"
    
    # Verify files exist before running
    if not os.path.exists(seq_pdb_path):
        print(f"Error: File not found - {seq_pdb_path}")
        return
    if not os.path.exists(orig_pdb_path):
        print(f"Error: File not found - {orig_pdb_path}")
        return
    
    try:
        # Run the async function
        tm_score = await compute_tm_score(
            pdb1_filename=seq_pdb_path,
            pdb2_filename=orig_pdb_path,
            pdb_dir=""  # directory where PDB files are stored
        )
        
        print(f"TM-Score result: {tm_score}")
        
    except Exception as e:
        print(f"Error computing TM-Score: {e}")

# Alternative version if compute_tm_score is not available in this script
# You'll need to import or define the function first

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())