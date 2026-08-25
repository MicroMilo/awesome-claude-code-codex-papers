# 2026 conference census and full-text audit

> Last audited: `2026-08-25T14:46:08+00:00`
>
> The main catalog is deliberately narrow: every record needs an official conference/proceedings/OpenReview/publisher acceptance source plus reviewed Claude Code or Codex CLI product evidence. Identity-verified open copies may supply content, but never venue identity.

The complete per-paper record is split by venue under [`data/audit/2026-conference-census/`](../data/audit/2026-conference-census/index.yaml). The checksum index maps every conference to its own YAML file. Every official-list record has an explicit `included`, `excluded`, `pending`, or `duplicate` disposition; no arXiv list is used as a conference census. Records may carry `full_text_scan: metadata-filtered` when an identity-bound abstract was screened and the PDF was intentionally not requested because it had no high-recall coding-agent signal.

## Conference totals

| Conference | Official source | Status | Total | Scanned | Metadata-screened | Included | Excluded | Pending | Duplicate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ASE | [official](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | accepted-list | 263 | 4 | 32 | 1 | 35 | 227 | 0 |
| FSE | [official](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | accepted-list | 211 | 38 | 102 | 0 | 140 | 71 | 0 |
| ISSTA | [official](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | accepted-list | 210 | 8 | 121 | 3 | 126 | 81 | 0 |
| ICSE | [official](https://conf.researchr.org/track/icse-2026/icse-2026-research-track) | accepted-list | 321 | 32 | 198 | 0 | 230 | 91 | 0 |
| ICML | [official](https://icml.cc/) | official-list | 6628 | 5 | 6428 | 5 | 6428 | 195 | 0 |
| ICLR | [official](https://iclr.cc/Downloads/2026) | official-proceedings | 5351 | 4180 | 1171 | 12 | 5339 | 0 | 0 |
| AAAI | [official](https://aaai.org/proceeding/aaai-40-2026/) | official-proceedings | 4920 | 64 | 4856 | 0 | 4920 | 0 | 0 |
| NeurIPS | [official](https://neurips.cc/) | pending | pending | 0 | 0 | 0 | 0 | 0 | 0 |
| IJCAI | [official](https://2026.ijcai.org/accepted-papers/) | accepted-list | 989 | 19 | 968 | 1 | 986 | 2 | 0 |
| KDD | [official](https://kdd2026.kdd.org/) | official-proceedings | 1415 | 10 | 1069 | 1 | 1078 | 329 | 7 |
| PLDI | [official](https://pldi26.sigplan.org/track/pldi-2026-papers) | accepted-list | 106 | 0 | 103 | 0 | 103 | 3 | 0 |
| POPL | [official](https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers) | accepted-list | 92 | 0 | 92 | 0 | 92 | 0 | 0 |
| OOPSLA | [official](https://conf.researchr.org/track/splash-2026/oopsla-2026) | accepted-list | 167 | 0 | 153 | 0 | 153 | 14 | 0 |

ICLR's official [Downloads/2026](https://iclr.cc/Downloads/2026) page exposed 5513 events; the main-paper census uses 5351 proceedings records after excluding tutorials, talks, workshops, and demonstrations from the paper total. The exported official list contains 5466 paper records.

## Official full-text refresh

The latest official-page refresh rechecked **479** metadata-selected Researchr records across AAAI, ASE, FSE, ICML, ICSE, ISSTA, OOPSLA, PLDI, POPL. It found **5** target-paper ACM DOI/PDF endpoints; **474** records still exposed no first-party full text. Of the discovered endpoints, **4** were recorded as publisher challenges and **0** were not requested because the official abstract was unavailable. Open repositories are never counted as acceptance sources, but an identity-verified copy may be used for content extraction.

## Identity-verified scholarly content

Official records below establish acceptance. OpenAlex, arXiv, or institutional repositories supply abstracts/full text only after an explicit DOI or title-and-author identity check.

| Conference | Canonical official DOI records | OpenAlex matches | Abstracts | Verified full text | Metadata candidates | Metadata exclusions |
|---|---:|---:|---:|---:|---:|---:|
| ASE | 10 | 1 | 1 | 1 | 0 | 1 |
| FSE | 39 | 38 | 38 | 12 | 15 | 23 |
| ISSTA | 0 | 0 | 0 | 3 | 0 | 0 |
| ICSE | 19 | 5 | 5 | 5 | 3 | 2 |
| ICML | 0 | 0 | 0 | 4 | 0 | 0 |
| KDD | 1408 | 1399 | 1099 | 349 | 30 | 1069 |
| PLDI | 106 | 105 | 105 | 36 | 3 | 102 |
| POPL | 92 | 90 | 90 | 31 | 0 | 90 |
| OOPSLA | 11 | 10 | 10 | 4 | 0 | 10 |

## Global disposition

- Official-list records: **20673**
- Included in the main catalog: **23**
- Explicitly excluded after full-text/source review: **19630**
- Pending because acceptance, identity-bound content, scanning, or product context is incomplete: **1013**
- Duplicate official records: **7**
- Main catalog records: **23**

## Included records

| Catalog ID | Conference | Paper | Official record | Evidence copy | Product / exact model | Evidence location |
|---|---|---|---|---|---|---|
| `llm2ltac-2026` | ASE | Mining Tactics for Automated Theorem Proving | [official](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | [content](https://arxiv.org/abs/2605.08694v1) | claude-code = Claude Sonnet 4.6 | Section 5 Evaluation; Section 5.3 RQ3; Table 4 in arXiv v1 |
| `red-teaming-coding-agents-2026` | ISSTA | Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment | [official](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [content](https://arxiv.org/abs/2509.05755v6) | claude-code = Claude-Sonnet 4; Claude-Sonnet 4.5; Claude-Sonnet 4.6; Claude-Opus-4.7 | Section 6.1 and Table 2; Sections 6.2-6.4; Tables 3-5; Section 7.2 in arXiv v6 |
| `execution-cost-effectiveness-2026` | ISSTA | To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair | [official](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [content](https://arxiv.org/abs/2606.26978v1) | claude-code = Anthropic claude-sonnet-4-5; codex-cli = OpenAI gpt-5.2 | Section 3.3 Models and Agents footnote 1; Section 3.5; Tables 2-7; Sections 4.2-4.3; Tables 8-13 in arXiv v1 |
| `evodev-2026` | ISSTA | Towards Iterative End-to-End Software Development: A Feature-Driven Multi-Agent Framework | [official](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | [content](https://arxiv.org/abs/2511.02399v3) | claude-code = claude-sonnet-4-20250514 | Sections 4.3.2-4.3.4; Section 5.1 and Table 3; Section 5.3 and Table 6; Section 5.5 and Figure 7 in arXiv v3 |
| `ape-bench-2026` | ICML | APE-Bench: Evaluating Automated Proof Engineering for Formal Math Libraries | [official](https://icml.cc/virtual/2026/poster/64323) | [content](https://arxiv.org/abs/2504.19110v3) | claude-code = Gemini 3 Flash; Gemini 3 Pro; GPT-5.2; codex-cli = Gemini 3 Flash; Gemini 3 Pro; GPT-5.2 | Section 6.1 Experimental Setup; Figure 3; Section 6.4 Scaffold Interchangeability; Figure 4 in arXiv v3 |
| `formact-2026` | ICML | FormAct: Agentic Source Editing for Rich-Format Document Generation | [official](https://icml.cc/virtual/2026/poster/61769) | official record | codex-cli = gpt-5.2-2025-12-11 | Section 5.1 Experimental Setup; Section 5.2; main comparison table; review-refinement ablation |
| `numina-lean-agent-2026` | ICML | Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal Mathematics | [official](https://icml.cc/virtual/2026/poster/66755) | [content](https://arxiv.org/abs/2601.14027v1) | claude-code = Claude Opus 4.5 | Section 2 Numina-Lean-Agent; Section 3.1 Performance; Tables 1-4; Section 4 in arXiv v1 |
| `posttrainbench-2026` | ICML | PostTrainBench: Can LLM Agents Automate LLM Post-Training? | [official](https://icml.cc/virtual/2026/poster/63667) | [content](https://arxiv.org/abs/2603.08640v1) | claude-code = Claude Opus 4.6; Claude Opus 4.5; Claude Sonnet 4.6; Claude Sonnet 4.5; Claude Haiku 4.5; Qwen3 Max; codex-cli = GPT-5.2; GPT 5.4 (High); GPT 5.1 Codex Max; GPT 5.3 Codex (High); GPT 5.3 Codex (Med); GPT 5.2 Codex | Section 2 PostTrainBench Setup; Figure 2; Section 3.1 and Table 1; Sections 4.1-4.4; Sections 5.3-5.5 in arXiv v1 |
| `swe-compass-2026` | ICML | SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities for Large Language Models | [official](https://icml.cc/virtual/2026/poster/64552) | [content](https://arxiv.org/abs/2511.05459v3) | claude-code = Claude-Sonnet-4-20250514; Qwen3-Coder-480B-A35B-Instruct; Qwen3-Coder-30B-A3B-Instruct; Qwen3-235B-A22B-Instruct-2507; DeepSeek-V3-0324 | Section 4.1 Evaluated LLMs and Frameworks; Table 2; Sections 4.2.1-4.2.2; Figure 7; Appendix A.2 and A.4 in arXiv v3 |
| `scaling-laws-2026` | ICLR | Can Language Models Discover Scaling Laws? | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/636d57c09a5baacd83722639265802f6-Abstract-Conference.html) | official record | claude-code = Claude-Haiku-4.5; Claude-Sonnet-4.5; codex-cli = o4-mini; GPT-5 | Section 4.1 Agent baselines; Table 3; Appendix B.5; Appendix D |
| `artemis-2026` | ICLR | Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0410c2ff9f872efe5a7c61a4323a5da3-Abstract-Conference.html) | official record | claude-code = Claude Sonnet 4; codex-cli = GPT-5 | Section 4.2 Agent Results; Table 1; Appendix A and J |
| `cybergym-2026` | ICLR | CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c876a2935a90aff21874e14c07dc3e33-Abstract-Conference.html) | official record | codex-cli = GPT-4.1 | Section 4 experimental evaluation; Figure 5; Appendix C Detailed Agent Settings |
| `deepscientist-2026` | ICLR | DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4f64494ecc3442f1c9261baa036378bc-Abstract-Conference.html) | official record | claude-code = Claude-4-opus | Section F Implementation Details; Section 4.2 Experimental Setup; Figure 4 |
| `devops-gym-2026` | ICLR | DevOps-Gym: Benchmarking AI Agents in Software DevOps Cycle | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/15e35461247bbd05fa890d384060c847-Abstract-Conference.html) | official record | claude-code = Claude-4-Sonnet | Section 4.1 Experimental Setup; Table 1; Appendix D.3 Table 4 |
| `featurebench-2026` | ICLR | FeatureBench: Benchmarking Agentic Coding for Complex Feature Development | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/25203d1cc8c58381eab578f4fcf9c4f8-Abstract-Conference.html) | official record | claude-code = Claude Opus 4.5; codex-cli = GPT-5.1-Codex | Section 4.1.1 Baseline; Table 2; Table 8; Appendix C Table 16 |
| `appforge-2026` | ICLR | From Assistant to Independent Developer — Are GPTs Ready for Software Development? | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a421e88bb7db67cd0401475a0ed4a17d-Abstract-Conference.html) | official record | claude-code = Qwen3-Coder | Section 4.3 Table 2; Appendix C.1 Setup; Appendix C.2 detailed statistics |
| `helmsman-2026` | ICLR | Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1c364d98a5cdc426fd8c76fbb2c10e34-Abstract-Conference.html) | official record | claude-code = Claude Sonnet 4.5; codex-cli = GPT-5.1-Codex | Section 4.2 Implementation Details; Appendix A.1 Tables 8-12; Appendix A.2 Table 12; PDF p. 15 |
| `innogym-2026` | ICLR | InnoGym: Benchmarking the Innovation Potential of AI Agents | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/743514dfa1ef705f378424bd1effb57b-Abstract-Conference.html) | official record | codex-cli = GPT-5 | Section 3.2 Novelty Evaluation; Section 4.1; Appendix F.1 |
| `qlcoder-2026` | ICLR | QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html) | official record | claude-code = Claude Sonnet 4; codex-cli = GPT-5 | Section 4.1 Experimental Setup; Table 2; Table 5; Appendix A |
| `rpg-zerorepo-2026` | ICLR | RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9482f45fdd89aba9130bb04c44f788a9-Abstract-Conference.html) | official record | claude-code = claude 4 sonnet; codex-cli = o3 pro | Section 3.3 Baselines; Section 4.3; RepoCraft main-results table |
| `terminal-bench-2-2026` | ICLR | Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html) | official record | claude-code = Claude Opus 4.5; Claude Sonnet 4.5; Claude Opus 4.1; Claude Haiku 4.5; codex-cli = GPT-5.2; GPT-5; GPT-5-Mini; GPT-5-Nano | Section 3.2 Agents; Section 3.3 Models; Table 2; Appendix B |
| `lean-refactor-2026` | IJCAI | Verifiable PDE Reasoning and Modeling with Neurosymbolics | [official](https://2026.ijcai.org/accepted-papers/?ijtrack=early-career-spotlight) | official record | claude-code = not-reported | Section 2.3 Formalizing Maintainable PDE Proofs in Lean; PDF page 3 |
| `swe-bench-mobile-2026` | KDD | SWE-Bench Mobile: Can Large Language Model Agents Develop Industry-Level Mobile Applications? | [official](https://doi.org/10.1145/3770855.3818488) | [content](https://arxiv.org/abs/2602.09540v1) | codex-cli = GLM-4.6; Claude Sonnet 4.5; GPT-5; Claude Opus 4.5; GPT-5.1; claude-code = GLM-4.6; Claude Sonnet 4.5; Claude Opus 4.5; Claude Haiku | Section 3.1-3.9; Appendix B Tables 5-6; Appendix E Reproducibility in arXiv v1 |

## Excluded and pending evidence

The per-conference YAML files retain the title, official URL, track, scan status, and reason for every excluded or pending record. The most common reasons in this run are:

- **14003** — No high-recall coding-agent, code, software-engineering, or language-model combination found in title or abstract. PDF download was not requested by the metadata-first policy.
- **4282** — Full-text scan found no Claude Code/Codex CLI product string; generic coding-agent or model/API mentions do not qualify for the main catalog.
- **1290** — No high-recall coding-agent, code, software-engineering, or language-model combination found in title or abstract. Decision used an identity-verified OpenAlex abstract for the official conference DOI; no PDF was requested.
- **470** — Official page did not expose a first-party PDF, ACM DOI, or OpenReview full-text link.
- **309** — Official record and full-text URL found; the full-text product/model scan has not been recorded yet.
- **201** — Official record and first-party full-text URL found; full-text product/model scan is pending.
- **50** — Full-text product-string hit reviewed as a reference/related-work mention, background discussion, or ancillary author code/writing assistance; no product-level baseline, evaluation, host configuration, or product-focused empirical analysis was found.
- **25** — Language-model and code/software-engineering signals found in title or abstract. Identity-verified full-text evidence is still required before catalog import.
- **4** — Agent and code/software-engineering signals found in title or abstract. Identity-verified full-text evidence is still required before catalog import.
- **2** — Official conference record found, but no official or identity-verified auxiliary full-text URL has been resolved yet.
- **2** — Direct coding-agent or software-engineering-agent signal found in title or abstract. Identity-verified full-text evidence is still required before catalog import.
- **1** — The only OpenAI Codex hit is an entry in the References section (the OpenAI Codex Developer Documentation citation on page 23); the paper does not run, evaluate, host, or compare Codex CLI.
- **1** — The only Claude Code hit is an Anthropic reference entry on page 8; the paper studies preference optimization for generated code and does not run, evaluate, host, or compare Claude Code.
- **1** — The only Claude Code hit is an Anthropic reference entry on page 8; the paper studies source-code unlearning and does not run, evaluate, host, or compare Claude Code.
- **1** — The only Claude Code hit is a citation in the References section on page 8; the paper evaluates temporal reasoning and does not run, evaluate, host, or compare Claude Code.
- **1** — Claude Code appears only as an example of result-oriented CLI tooling in Section 3.1. The evaluation compares the paper's 4D visualization with LangSmith linear traces and does not run or evaluate Claude Code.

## Priority pending queue

A product name in a title or identity-bound abstract is a prioritization signal, not inclusion evidence. These records remain pending until official or identity-verified full text and the exact product/model context can be reviewed.

- Pending paper records: **1013**
- High-priority direct-product candidates: **0**
- Included records using an auxiliary evidence copy: **9**

| Conference | Paper | Official record | Product signal | Current blocker |
|---|---|---|---|---|
| — | No direct-product pending candidates recorded | — | — | — |

### Conference-level pending

- **NeurIPS** — The official OpenReview group is registered, but public submissions and an accepted-paper list are not released. No preprint list is substituted. ([official](https://openreview.net/group?id=NeurIPS.cc%2F2026%2FConference))

## Audit artifacts

- [`data/audit/2026-conference-census/index.yaml`](../data/audit/2026-conference-census/index.yaml) — ordered per-conference file map with record counts and SHA-256 checksums.
- [`data/audit/current-catalog-audit.yaml`](../data/audit/current-catalog-audit.yaml) — field-by-field audit of the pre-migration 32-record catalog.
- [`data/audit/2026-scholarly-content.jsonl`](../data/audit/2026-scholarly-content.jsonl) — resumable DOI-resolution ledger for OpenAlex abstracts and open full-text locations.
- [`data/audit/content-source-overrides.yaml`](../data/audit/content-source-overrides.yaml) — reviewed title/author mappings for candidate-only auxiliary copies.
- [`data/audit/2026-fulltext-scan.jsonl`](../data/audit/2026-fulltext-scan.jsonl) — page-level snippets, extraction method, product hits, model candidates, selected source, and content SHA-256; PDFs are not committed.
- [`data/audit/2026-pending-summary.json`](../data/audit/2026-pending-summary.json) — compact blocker counts and the high-priority direct-product pending queue.
- [`data/papers.yaml`](../data/papers.yaml) — the 23 records promoted into the current official-source main catalog after this audit.

## Source policy

Conference pages, official proceedings, official OpenReview conference records, and official publisher pages establish acceptance and remain the primary paper URLs. ArXiv-only records are excluded. An arXiv or institutional copy may supply abstract/full-text evidence only when it is explicitly identity-matched to an official record and its version, URL, retrieval hash, and evidence location are retained.
