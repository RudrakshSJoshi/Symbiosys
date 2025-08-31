# SYMBIOSYS — Synthetic Yield‑driven Molecular Biosimilar Innovation & Optimization via Structural Yield Simulation

![SYMBIOSYS Logo](https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Screenshot%202025-08-31%20113422-aqdNwQ5sufPQTvf9BXLR0U4E0DrPiH.png)

AI-powered Biosimilar Designer & Pharmacovigilance Platform to enable affordable, local biologic manufacturing in Latin America.

## Problem Statement — Why Latin America
- Biologics (monoclonal antibodies, hormones, enzymes) are life-changing but often unaffordable across LATAM due to import dependence, complex manufacturing, and long comparability studies.
- Development is costly ($0.95–$2.3B) with low success rates (≈10–15% to approval). These costs roll into prices paid by ministries of health and public payers.
- Local manufacturers face barriers: limited process IP, expensive analytics, and fragmented pharmacovigilance (PV) reporting pipelines.
- Result: treatment inequity—especially in public systems and rural areas—despite high regional disease burden.

## Our Vision
A sovereign, AI-first workflow that reduces time and cost to design, compare, and monitor biosimilars tailored for the Latin American regulatory ecosystem.

## What SYMBIOSYS Does
Two integrated halves:
1) Biosimilar Designer (in silico)
- Input: reference sequence/structure.
- Generate candidate variants that preserve function/topology but are easier to manufacture.
- Predict manufacturability and risk: aggregation, PTMs/glycosylation hints, epitope similarity, binding-site conservation.

2) Pharmacovigilance & Monitoring
- Ingest spontaneous reports (SRS), de-identified EHR snippets, and public safety feeds.
- NLP for case triage/deduplication; dashboards for signal detection and batch traceability.
- Export reports aligned to WHO/VigiBase formats; interfaces in Spanish and Portuguese.

## MVP Flow (Hackathon Prototype)
- Input a protein sequence.
- Structure: ESMFold creates 3D predictions.
- Design: ProtGPT2 proposes biosimilar variants while preserving topology.
- Compare: TM-align → TM-score for structural similarity.
- Output: similarity + manufacturability heuristics as a “comparability dossier” preview.

Note: The live demo in this repo simulates these steps without running heavy scientific inference.

## Regional Relevance & Regulatory Fit
- Harmonizes with WHO/ICH comparability principles (structure/function, quality, safety).
- Ready to localize for LATAM agencies:
  - Brazil: ANVISA
  - Mexico: COFEPRIS
  - Colombia: INVIMA
  - Argentina: ANMAT
  - Chile: ISP
  - Peru: DIGEMID
- Produces bilingual (ES/PT) artifacts and audit trails.

## Potential Pilots (Public Manufacturers)
- Brazil: Fiocruz / Bio‑Manguinhos
- Mexico: Birmex
- Argentina: ANLIS–Malbrán
- Colombia: University–public consortia
- Regional: PAHO-aligned procurement and safety coordination

## Data Sources (Open/Reference)
- Design: UniProt, PDB; protein language models (e.g., ProtGPT2).
- Risk: aggregation and PTM predictors (research-grade), epitope similarity heuristics.
- PV: national SRS schemas, WHO/VigiBase export formats (no PHI in demo).

## Architecture (Prototype)
- Frontend: Next.js App Router with shadcn/ui, Tailwind CSS, slide deck UI with scroll-snap and keyboard nav.
- Demo: client-side simulator that mimics sequence → variant → similarity scoring (no real inference).
- Extensible to real pipelines: server actions calling ESMFold, constrained ProtGPT2 generation, TM-align, and PV ingestion/ETL.

## Demo
- Open the Preview and scroll the “slides” or use the deck navigation.
- “Try the similarity simulator” slide provides a safe, synthetic mock of the pipeline.

## Roadmap
- Integrate real ESMFold inference and pLDDT.
- Add constrained ProtGPT2 generation preserving topology and motifs.
- Server-side TM-align, glycosylation and aggregation predictors.
- PV ingestion pipelines with de‑identification, RLS and role-based access.
- Dossier generator per regulator, bilingual export, immutable audit logs.
- Pilots with public labs; measure price reduction (20–40%) and time-to-decision (6–12 months faster).

## Ethics & Safety
- No PHI in the demo; de‑identification required for any real clinical text.
- Transparent limitations; model outputs are research aids, not approvals.
- Regional data governance and sovereign cloud/on‑prem options.

## Getting Started
- Use the v0 preview to run the deck immediately. Publish to Vercel from the top-right “Publish” button.
- To export, use the version menu (Download ZIP). Printing the deck from the browser produces a shareable PDF.

## License
MIT — see LICENSE if provided. For pilots and regulatory integrations, contact the team.
