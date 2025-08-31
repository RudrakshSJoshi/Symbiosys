import mdtraj as md
from collections import Counter
import asyncio

async def analyze_pdb_full(pdb_file):
    """
    Async function that combines custom PDB parsing and secondary structure analysis.
    Returns a single natural-language summary string.
    """

    # ---------------------------
    # Custom PDB parsing
    # ---------------------------
    chains = {}
    residues_set = set()
    atom_count = 0

    async def parse_custom():
        nonlocal chains, residues_set, atom_count
        with open(pdb_file, 'r') as f:
            for line in f:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    atom_count += 1
                    chain_id = line[21].strip()
                    res_seq = int(line[22:26].strip())
                    res_name = line[17:20].strip()

                    # Track residues per chain
                    if chain_id not in chains:
                        chains[chain_id] = {}
                    chains[chain_id][res_seq] = res_name

                    # Track unique residues overall
                    residues_set.add((chain_id, res_seq, res_name))

    await parse_custom()

    total_chains = len(chains)
    total_residues = len(residues_set)

    # Generate per-chain residue count
    chain_residue_counts = {cid: len(chain) for cid, chain in chains.items()}

    # Simple “n-mer” detection: first 5 residues per chain
    chain_first_residues = {
        cid: "".join([res for _, res in sorted([(seq, res) for seq, res in chain.items()])][:5])
        for cid, chain in chains.items()
    }

    custom_summary = f"The protein contains {total_residues} residues across {total_chains} chain(s): "
    parts = []
    for cid in sorted(chains.keys()):
        parts.append(f"chain {cid} has {chain_residue_counts[cid]} residues, starting with {chain_first_residues[cid]}")
    custom_summary += "; ".join(parts) + f". Total atoms in structure: {atom_count}."

    # ---------------------------
    # MDTraj DSSP secondary structure analysis
    # ---------------------------
    async def parse_secondary_structure():
        traj = md.load_pdb(pdb_file)
        ss = md.compute_dssp(traj)[0]  # first model
        ss_counts = Counter(ss)
        ss_labels = {
            'H': 'alpha-helix',
            'B': 'isolated beta-bridge',
            'E': 'beta-sheet',
            'G': '3-10 helix',
            'I': 'pi-helix',
            'T': 'turn',
            'S': 'bend',
            '-': 'coil'
        }
        readable_counts = {ss_labels.get(k, k): v for k, v in ss_counts.items()}
        total_residues = len(ss)

        ss_summary = f"It is composed of "
        parts = []
        for label, count in readable_counts.items():
            fraction = count / total_residues * 100
            parts.append(f"{count} residues ({fraction:.1f}%) in {label}")
        ss_summary += ", ".join(parts) + "."
        return ss_summary

    ss_summary = await parse_secondary_structure()

    # ---------------------------
    # Combine summaries
    # ---------------------------
    full_summary = custom_summary + "\n" + ss_summary
    return full_summary


# # ---------------------------
# # Example usage
# # ---------------------------
# if __name__ == "__main__":
#     pdb_file = "example1.pdb"  # replace with your file path

#     async def main():
#         summary = await analyze_pdb_full(pdb_file)
#         print(summary)

#     asyncio.run(main())
