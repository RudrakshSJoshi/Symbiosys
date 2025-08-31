# SYMBIOSYS — Synthetic Yield‑driven Molecular Biosimilar Innovation & Optimization via Structural Yield Simulation

![SYMBIOSYS Logo](https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Screenshot%202025-08-31%20113422-aqdNwQ5sufPQTvf9BXLR0U4E0DrPiH.png)

AI-powered Biosimilar Designer & Pharmacovigilance Platform to enable affordable, local biologic manufacturing in Latin America.

## How We Solve It (TL;DR)
- Mixture of models: we orchestrate ESMFold (structure), a fine‑tuned ProtGPT2 (constrained sequence “rewrite”), and similarity/biophysics scoring to propose candidates that keep the same 3D shape and function but are cheaper and easier to manufacture—built for LATAM realities (cost, supply, facilities).
- ESMFold builds 3D structure from the input sequence for the reference and candidates (with pLDDT confidence).
- ProtGPT2 generates topology‑preserving variants optimized for manufacturability and stability.
- TM‑align computes TM‑score to quantify structural similarity; we layer on heuristics for aggregation, PTMs/glycosylation, and immunogenicity risk.
- Outputs: regulator‑friendly “comparability dossier” (alignments, scores, confidence plots, change tables) + manufacturability notes and an audit trail. Localized in ES/PT for ANVISA, COFEPRIS, INVIMA, ANMAT, ISP, DIGEMID.

## Our Solution — in human terms
Today, Latin America often waits and pays more for biologics made elsewhere. SYMBIOSYS changes the starting point: before anyone buys bioreactors or runs long wet‑lab series, we use AI to propose biosimilar candidates that already look, fold, and behave like the reference—while being simpler and cheaper to make locally.

Think of it like “paraphrasing” the protein. We keep the 3D shape (the topology that drives function), but we ask an AI model—fine‑tuned for manufacturability—to rewrite the amino‑acid sequence so it’s friendlier to express, purify, and scale on regional equipment. Then we score every candidate against the original with TM‑score and other safety/manufacturability checks. Only the closest matches move forward, packaged with regulator‑ready evidence in Spanish and Portuguese.

What this means for a public manufacturer in LATAM:
- Fewer expensive dead‑ends: triage candidates in days, not months, before wet‑lab spend.
- Locally feasible: variants prefer expression systems and process realities common in the region.
- Regulator‑friendly from day one: comparability artifacts that speak ANVISA/COFEPRIS/INVIMA language.
- Pragmatic sovereignty: shift from import dependence to local design and production capability.

Why this is unique:
- Model mixture + constraints: not just “generate a protein,” but generate one that preserves 3D shape and is manufacturable under cost and process constraints.
- Evidence out, not just sequences: we export a comparability dossier, not a black box.
- Built for LATAM: bilingual reports, PV integration, and pathways to pilots with public labs.

### Why this matters for Latin America
- Cuts early analytical iteration cost and time so public manufacturers can prioritize molecules tied to regional disease burden.
- Reduces dependence on imports by enabling in‑region design, triage, and evidence prep before wet‑lab spend.
- Bilingual artifacts and reporting formats aligned to LATAM agencies; sovereign cloud/on‑prem options.

### Key Differentiators
- LATAM‑first regulatory packaging (ES/PT) and PV integration.
- End‑to‑end: Designer + Pharmacovigilance, not just protein generation.
- Auditability and exportable dossiers tailored to regional submissions.

> Pitch in 30 seconds: SYMBIOSYS lets LATAM teams design biosimilar candidates in silico, quantify similarity with TM‑score, and ship regulator‑ready evidence and PV dashboards—lowering costs 20–40% and speeding go/no‑go by 6–12 months.

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
