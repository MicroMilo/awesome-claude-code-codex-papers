# 2026 conference census and full-text audit

> Last audited: `2026-08-24T06:56:47+00:00`
>
> The main catalog is deliberately narrow: only 2026 records with a first-party conference/proceedings/OpenReview source and reviewed Claude Code or Codex CLI product evidence are imported.

The complete per-paper record is in [`data/audit/2026-conference-census.yaml`](../data/audit/2026-conference-census.yaml). Every official-list record has an explicit `included`, `excluded`, `pending`, or `duplicate` disposition; no arXiv list is used as a conference census. ICLR records may also carry `full_text_scan: metadata-filtered`: the official abstract was screened and the PDF was intentionally not requested because it had no high-recall coding-agent signal.

## Conference totals

| Conference | Official source | Status | Total | Scanned | Metadata-screened | Included | Excluded | Pending | Duplicate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ASE | [official](https://conf.researchr.org/track/ase-2026/ase-2026-research-track) | accepted-list | 263 | 3 | 32 | 0 | 35 | 228 | 0 |
| FSE | [official](https://conf.researchr.org/track/fse-2026/fse-2026-research-papers) | accepted-list | 211 | 32 | 102 | 0 | 134 | 77 | 0 |
| ISSTA | [official](https://conf.researchr.org/track/issta-2026/issta-2026-research-papers) | accepted-list | 210 | 5 | 121 | 0 | 126 | 84 | 0 |
| ICSE | [official](https://conf.researchr.org/track/icse-2026/icse-2026-research-track) | accepted-list | 321 | 29 | 198 | 0 | 227 | 94 | 0 |
| ICML | [official](https://icml.cc/) | official-list | 6628 | 0 | 6428 | 1 | 6428 | 199 | 0 |
| ICLR | [official](https://iclr.cc/Downloads/2026) | official-proceedings | 5351 | 4180 | 1171 | 12 | 5339 | 0 | 0 |
| AAAI | [official](https://aaai.org/proceeding/aaai-40-2026/) | official-proceedings | 4920 | 64 | 4856 | 0 | 4920 | 0 | 0 |
| NeurIPS | [official](https://neurips.cc/) | pending | pending | 0 | 0 | 0 | 0 | 0 | 0 |
| IJCAI | [official](https://2026.ijcai.org/) | pending | pending | 0 | 0 | 0 | 0 | 0 | 0 |
| KDD | [official](https://www.kdd.org/kdd2026/) | pending | pending | 0 | 0 | 0 | 0 | 0 | 0 |
| PLDI | [official](https://pldi26.sigplan.org/track/pldi-2026-papers) | accepted-list | 106 | 0 | 102 | 0 | 102 | 4 | 0 |
| POPL | [official](https://conf.researchr.org/track/POPL-2026/POPL-2026-popl-research-papers) | accepted-list | 92 | 0 | 91 | 0 | 91 | 1 | 0 |
| OOPSLA | [official](https://conf.researchr.org/track/splash-2026/oopsla-2026) | accepted-list | 167 | 0 | 153 | 0 | 153 | 14 | 0 |

ICLR's official [Downloads/2026](https://iclr.cc/Downloads/2026) page exposed 5513 events; the main-paper census uses 5351 proceedings records after excluding tutorials, talks, workshops, and demonstrations from the paper total. The exported official list contains 5466 paper records.

## Global disposition

- Official-list records: **18269**
- Included in the main catalog: **13**
- Explicitly excluded after full-text/source review: **17555**
- Pending because official full text, acceptance status, or product context is incomplete: **701**
- Duplicate official records: **0**
- Main catalog records: **13**

## Included records

| Catalog ID | Conference | Paper | Official record | Product / exact model | Evidence location |
|---|---|---|---|---|---|
| `formact-2026` | ICML | FormAct: Agentic Source Editing for Rich-Format Document Generation | [official](https://icml.cc/virtual/2026/poster/61769) | codex-cli = gpt-5.2-2025-12-11 | Section 5.1 Experimental Setup; Section 5.2; main comparison table; review-refinement ablation |
| `scaling-laws-2026` | ICLR | Can Language Models Discover Scaling Laws? | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/636d57c09a5baacd83722639265802f6-Abstract-Conference.html) | claude-code = Claude-Haiku-4.5; Claude-Sonnet-4.5; codex-cli = o4-mini; GPT-5 | Section 4.1 Agent baselines; Table 3; Appendix B.5; Appendix D |
| `artemis-2026` | ICLR | Comparing AI Agents to Cybersecurity Professionals in Real-World Penetration Testing | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/0410c2ff9f872efe5a7c61a4323a5da3-Abstract-Conference.html) | claude-code = Claude Sonnet 4; codex-cli = GPT-5 | Section 4.2 Agent Results; Table 1; Appendix A and J |
| `cybergym-2026` | ICLR | CyberGym: Evaluating AI Agents' Real-World Cybersecurity Capabilities at Scale | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c876a2935a90aff21874e14c07dc3e33-Abstract-Conference.html) | codex-cli = GPT-4.1 | Section 4 experimental evaluation; Figure 5; Appendix C Detailed Agent Settings |
| `deepscientist-2026` | ICLR | DeepScientist: Advancing Frontier-Pushing Scientific Findings Progressively | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/4f64494ecc3442f1c9261baa036378bc-Abstract-Conference.html) | claude-code = Claude-4-opus | Section F Implementation Details; Section 4.2 Experimental Setup; Figure 4 |
| `devops-gym-2026` | ICLR | DevOps-Gym: Benchmarking AI Agents in Software DevOps Cycle | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/15e35461247bbd05fa890d384060c847-Abstract-Conference.html) | claude-code = Claude-4-Sonnet | Section 4.1 Experimental Setup; Table 1; Appendix D.3 Table 4 |
| `featurebench-2026` | ICLR | FeatureBench: Benchmarking Agentic Coding for Complex Feature Development | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/25203d1cc8c58381eab578f4fcf9c4f8-Abstract-Conference.html) | claude-code = Claude Opus 4.5; codex-cli = GPT-5.1-Codex | Section 4.1.1 Baseline; Table 2; Table 8; Appendix C Table 16 |
| `appforge-2026` | ICLR | From Assistant to Independent Developer — Are GPTs Ready for Software Development? | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a421e88bb7db67cd0401475a0ed4a17d-Abstract-Conference.html) | claude-code = Qwen3-Coder | Section 4.3 Table 2; Appendix C.1 Setup; Appendix C.2 detailed statistics |
| `helmsman-2026` | ICLR | Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/1c364d98a5cdc426fd8c76fbb2c10e34-Abstract-Conference.html) | claude-code = Claude Sonnet 4.5; codex-cli = GPT-5.1-Codex | Section 4.2 Implementation Details; Appendix A.1 Tables 8-12; Appendix A.2 Table 12; PDF p. 15 |
| `innogym-2026` | ICLR | InnoGym: Benchmarking the Innovation Potential of AI Agents | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/743514dfa1ef705f378424bd1effb57b-Abstract-Conference.html) | codex-cli = GPT-5 | Section 3.2 Novelty Evaluation; Section 4.1; Appendix F.1 |
| `qlcoder-2026` | ICLR | QLCoder: A Query Synthesizer For Static Analysis of Security Vulnerabilities | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/2adf01ab15adde8820622f7f24bd516b-Abstract-Conference.html) | claude-code = Claude Sonnet 4; codex-cli = GPT-5 | Section 4.1 Experimental Setup; Table 2; Table 5; Appendix A |
| `rpg-zerorepo-2026` | ICLR | RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/9482f45fdd89aba9130bb04c44f788a9-Abstract-Conference.html) | claude-code = claude 4 sonnet; codex-cli = o3 pro | Section 3.3 Baselines; Section 4.3; RepoCraft main-results table |
| `terminal-bench-2-2026` | ICLR | Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces | [official](https://proceedings.iclr.cc/paper_files/paper/2026/hash/444a3737adaee10d86ad2ef5f74468e6-Abstract-Conference.html) | claude-code = Claude Opus 4.5; Claude Sonnet 4.5; Claude Opus 4.1; Claude Haiku 4.5; codex-cli = GPT-5.2; GPT-5; GPT-5-Mini; GPT-5-Nano | Section 3.2 Agents; Section 3.3 Models; Table 2; Appendix B |

## Excluded and pending evidence

The YAML report retains the title, official URL, track, scan status, and reason for every excluded or pending record. The most common reasons in this run are:

- **13254** — No high-recall coding-agent, code, software-engineering, or language-model combination found in title or abstract. PDF download was not requested by the metadata-first policy.
- **4247** — Full-text scan found no Claude Code/Codex CLI product string; generic coding-agent or model/API mentions do not qualify for the main catalog.
- **476** — Official conference record found, but no first-party full-text PDF URL was exposed by the source adapter; arXiv is not used as a substitute.
- **200** — Official record and first-party full-text URL found; full-text product/model scan is pending.
- **50** — Full-text product-string hit reviewed as a reference/related-work mention, background discussion, or ancillary author code/writing assistance; no product-level baseline, evaluation, host configuration, or product-focused empirical analysis was found.
- **14** — Official page did not expose a first-party PDF or OpenReview full-text link.
- **4** — High-priority product candidate from the official title/abstract. The official conference record does not yet expose a first-party full-text PDF URL. Remains pending until first-party full text can be reviewed; arXiv is not used as a substitute.
- **4** — High-priority product candidate from the official title/abstract. The first-party full-text endpoint returned an HTTP 403 browser-verification challenge. Remains pending until first-party full text can be reviewed; arXiv is not used as a substitute.
- **3** — Official record found, but no first-party full-text PDF URL was exposed; a GitHub-hosted copy was discovered but is not used as evidence; arXiv is not used as a substitute.
- **1** — The only OpenAI Codex hit is an entry in the References section (the OpenAI Codex Developer Documentation citation on page 23); the paper does not run, evaluate, host, or compare Codex CLI.
- **1** — The only Claude Code hit is an Anthropic reference entry on page 8; the paper studies preference optimization for generated code and does not run, evaluate, host, or compare Claude Code.
- **1** — The only Claude Code hit is an Anthropic reference entry on page 8; the paper studies source-code unlearning and does not run, evaluate, host, or compare Claude Code.
- **1** — The only Claude Code hit is a citation in the References section on page 8; the paper evaluates temporal reasoning and does not run, evaluate, host, or compare Claude Code.

## Priority pending queue

A product name in an official title or abstract is a prioritization signal, not inclusion evidence. These records remain pending until first-party full text and the exact product/model context can be reviewed.

- Pending paper records: **701**
- High-priority direct-product candidates: **8**
- arXiv fallbacks used: **0**

| Conference | Paper | Official record | Product signal | Current blocker |
|---|---|---|---|---|
| ASE | Mining Tactics for Automated Theorem Proving | [official](https://conf.researchr.org/details/ase-2026/ase-2026-research-track/232/Mining-Tactics-for-Automated-Theorem-Proving) | claude-code: Claude Code | The official conference record does not yet expose a first-party full-text PDF URL. |
| ICML | APE-Bench: Evaluating Automated Proof Engineering for Formal Math Libraries | [official](https://icml.cc/virtual/2026/poster/64323) | claude-code: Claude Code; codex-cli: Codex CLI | The first-party full-text endpoint returned an HTTP 403 browser-verification challenge. |
| ICML | Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal Mathematics | [official](https://icml.cc/virtual/2026/poster/66755) | claude-code: Claude Code | The first-party full-text endpoint returned an HTTP 403 browser-verification challenge. |
| ICML | PostTrainBench: Can LLM Agents Automate LLM Post-Training? | [official](https://icml.cc/virtual/2026/poster/63667) | claude-code: Claude Code; codex-cli: Codex Max | The first-party full-text endpoint returned an HTTP 403 browser-verification challenge. |
| ICML | SWE-Compass: Towards Unified Evaluation of Agentic Coding Abilities for Large Language Models | [official](https://icml.cc/virtual/2026/poster/64552) | claude-code: Claude Code | The first-party full-text endpoint returned an HTTP 403 browser-verification challenge. |
| ISSTA | Red-Teaming Coding Agents from a Tool-Invocation Perspective: An Empirical Security Assessment | [official](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/176/Red-Teaming-Coding-Agents-from-a-Tool-Invocation-Perspective-An-Empirical-Security-A) | claude-code: Claude Code | The official conference record does not yet expose a first-party full-text PDF URL. |
| ISSTA | To Run or Not to Run: Analyzing the Cost-Effectiveness of Code Execution in LLM-Based Program Repair | [official](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/22/To-Run-or-Not-to-Run-Analyzing-the-Cost-Effectiveness-of-Code-Execution-in-LLM-Based) | claude-code: Claude Code | The official conference record does not yet expose a first-party full-text PDF URL. |
| ISSTA | Towards Iterative End-to-End Software Development: A Feature-Driven Multi-Agent Framework | [official](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/207/Towards-Iterative-End-to-End-Software-Development-A-Feature-Driven-Multi-Agent-Frame) | claude-code: Claude Code | The official conference record does not yet expose a first-party full-text PDF URL. |

### Conference-level pending

- **NeurIPS** — The official OpenReview group exists, but an accepted-paper list/proceedings was not released at the audit time; no preprint list is substituted. ([official](https://openreview.net/group?id=NeurIPS.cc%2F2026%2FConference))
- **IJCAI** — Registered for the CCF-A extension pass; a complete first-party 2026 proceedings list was not imported in this run. ([official](https://2026.ijcai.org/))
- **KDD** — Registered for the CCF-A extension pass; the official proceedings list still needs a dedicated source adapter. ([official](https://www.kdd.org/kdd2026/))

## Audit artifacts

- [`data/audit/current-catalog-audit.yaml`](../data/audit/current-catalog-audit.yaml) — field-by-field audit of the pre-migration 32-record catalog.
- [`data/audit/2026-fulltext-scan.jsonl`](../data/audit/2026-fulltext-scan.jsonl) — page-level snippets, extraction method, product hits, and model candidates for official PDFs; PDFs are not committed.
- [`data/audit/2026-pending-summary.json`](../data/audit/2026-pending-summary.json) — compact blocker counts and the high-priority direct-product pending queue.
- [`data/papers.yaml`](../data/papers.yaml) — the 13 records promoted into the current official-source main catalog after this audit.

## Source policy

Conference pages, official proceedings, official OpenReview conference records, and official publisher pages are accepted as primary sources. ArXiv-only records are excluded from the main catalog; an arXiv URL can never satisfy the primary-source requirement.
