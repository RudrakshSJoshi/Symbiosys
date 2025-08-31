import tempfile, io, asyncio
from Bio.PDB import PDBParser, DSSP, PDBIO

async def run_dssp(pdb_string: str) -> str:
    """
    Takes a raw PDB string, runs DSSP,
    and returns a modified PDB string with
    secondary structure encoded in B-factor.
    """
    # Write PDB string to a temporary file (DSSP requires file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdb") as tmp:
        tmp.write(pdb_string.encode())
        pdb_path = tmp.name

    # Parse structure
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("prot", pdb_path)
    model = structure[0]

    # Run DSSP in a thread (since it's blocking)
    def _dssp():
        return DSSP(model, pdb_path)

    dssp = await asyncio.to_thread(_dssp)

    # Map DSSP codes to numbers (for coloring in 3Dmol by B-factor)
    ss_map = {"H": 1, "B": 2, "E": 3, "G": 4, "I": 5, "T": 6, "S": 7, "-": 0}

    for key in dssp.keys():
        chain, res_id = key
        res_num = res_id[1]
        try:
            residue = model[chain][res_num]
            ss_code = dssp[key][2]
            for atom in residue:
                atom.set_bfactor(ss_map.get(ss_code, 0))
        except Exception:
            continue

    # Save modified PDB to string
    io_out = io.StringIO()
    io_obj = PDBIO()
    io_obj.set_structure(structure)
    io_obj.save(io_out)

    return io_out.getvalue()
