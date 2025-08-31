import aiohttp
import aiofiles
import os
import hashlib

# Ensure the pdb_data directory exists
os.makedirs("pdb_data", exist_ok=True)

async def fetch_pdb(fold_sequence: str) -> tuple[bool, str | None]:
    """
    Fetches the PDB for a given fold sequence from ESM Atlas API.
    
    Returns:
        (success: bool, pdb_content: str | None)
    """
    # Use a hash of the fold_sequence for unique filenames
    file_hash = hashlib.sha256(fold_sequence.encode()).hexdigest()
    file_path = os.path.join("pdb_data", f"{file_hash}.pdb")
    
    # Check if file already exists
    if os.path.exists(file_path):
        print(f"PDB for this sequence is cached: {file_path}")
        async with aiofiles.open(file_path, 'r') as f:
            pdb_content = await f.read()
        return True, pdb_content
    
    url = "https://api.esmatlas.com/foldSequence/v1/pdb/"
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=fold_sequence) as response:
            if response.status == 200:
                pdb_content = await response.text()
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(pdb_content)
                print(f"PDB fetched and saved to: {file_path}")
                return True, pdb_content
            else:
                print(f"Failed to fetch PDB. Status code: {response.status}")
                return False, None
