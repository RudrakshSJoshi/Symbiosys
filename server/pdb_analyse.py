def parse_pdb_custom(pdb_file):
    chains = {}
    residues_set = set()
    atom_count = 0

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

    total_chains = len(chains)
    total_residues = len(residues_set)

    # Generate per-chain residue count
    chain_residue_counts = {cid: len(chain) for cid, chain in chains.items()}

    # Simple “n-mer” detection: show first 5 residues of each chain
    chain_first_residues = {cid: "".join([res for _, res in sorted([(seq, res) for seq, res in chain.items()])][:5])
                            for cid, chain in chains.items()}

    # Construct natural-language summary
    summary = f"The protein contains {total_residues} residues across {total_chains} chain(s): "
    parts = []
    for cid in sorted(chains.keys()):
        parts.append(f"chain {cid} has {chain_residue_counts[cid]} residues, starting with {chain_first_residues[cid]}")

    summary += "; ".join(parts) + f". Total atoms in structure: {atom_count}."
    return summary


if __name__ == "__main__":
    pdb_file = "example1.pdb"  # replace with your PDB file
    result = parse_pdb_custom(pdb_file)
    print(result)
