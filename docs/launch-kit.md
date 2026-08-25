# v0.3 Launch Kit

> Status: ready-to-post drafts. Nothing in this document has been posted automatically. Recheck the destination's current rules immediately before publishing.

[中文版本](launch-kit.zh-CN.md)

## Fact sheet

- Project: **Awesome Claude Code & Codex Papers** / **Agent Papers**
- Repository: https://github.com/MicroMilo/awesome-claude-code-codex-papers
- Website: https://micromilo.github.io/awesome-claude-code-codex-papers/
- Methods matrix: https://micromilo.github.io/awesome-claude-code-codex-papers/methods/
- Evidence-backed insights: https://micromilo.github.io/awesome-claude-code-codex-papers/insights/
- Reusable census skill: https://micromilo.github.io/awesome-claude-code-codex-papers/skill/
- Feed: https://micromilo.github.io/awesome-claude-code-codex-papers/feed.xml
- Current audited scope: **18,269 official-list records** across **13 registered conference series**; **13 papers** currently pass the strict product-level inclusion gate.
- Inclusion rule: a formally accepted 2026 paper must actually run Claude Code or Codex CLI as a product-level agent. Merely using a Claude or GPT model does not qualify.
- Audit rule: every official-list record remains `included`, `excluded`, `pending`, or `duplicate`; blocked full text remains pending.
- License: MIT.

Use these figures together. Never say “18,269 relevant papers” or imply that all 18,269 records were included.

## Launch principles

1. Lead with the research problem, not an appeal for stars.
2. Link to the most relevant page for the audience: insights for builders, methods for researchers, the skill for data/crawling discussions.
3. Ask one concrete question so the post can become a useful discussion.
4. Disclose that you maintain the project.
5. Do not coordinate votes, ask friends to upvote, or copy-paste the same post everywhere on one day.
6. Reply with evidence links, not leaderboard claims.

## Recommended order

| Day | Channel | Why this route | Call to action |
|---|---|---|---|
| 1 | openai/codex “Show and tell” | Highest product intent; the category explicitly invites things people made | Challenge the scope gate or suggest a missing paper |
| 2 | OpenAI Developer Community, Codex | Publish an educational synthesis, not a launch ad | Discuss which failure mode matters in practice |
| 3 | Hacker News regular submission | HN says lists and reading material are not eligible for Show HN | Inspect the catalog and discuss methodology |
| 4 | Paper-author outreach | The authors have the strongest reason to verify and share a precise record | Request corrections, then invite sharing |
| 5 | r/ChatGPTCoding weekly self-promotion thread | Current Rule 5 sends promotional project posts to the weekly thread | Ask for missing coding-agent papers |

Wait at least a day between broad public posts. Update the opening based on the questions people actually ask.

## 1. openai/codex Show and tell

Destination: https://github.com/openai/codex/discussions/categories/show-and-tell

The category describes itself as “Show off something you've made.” Use the repository's research and reusable skill as the concrete artifact.

### Title

```text
I audited 18,269 conference records for papers that actually run Codex CLI or Claude Code
```

### Body

```markdown
I maintain an open, evidence-first catalog of 2026 conference papers that actually run Codex CLI or Claude Code as products.

The scope gate is deliberately strict: a paper does not qualify just because it uses GPT or Claude. It must run the product as a baseline, evaluated system, host, wrapper, or product-level comparison target.

The current audit indexes 18,269 official-list records across 13 conference series. Thirteen papers pass the product-level gate; every other official record remains auditable as included, excluded, pending, or duplicate.

The part I find most useful is the methods matrix. It keeps the exact product model, intervention, reported result, same-model/same-budget controls, source location, and caveat on one page:

https://micromilo.github.io/awesome-claude-code-codex-papers/methods/

The cross-paper synthesis currently points to four recurring mechanisms: executable verification, persistent task state, domain-grounded context, and structured exploration. These are hypotheses from the reviewed evidence, not a vendor leaderboard.

Repository: https://github.com/MicroMilo/awesome-claude-code-codex-papers

What product-level Codex paper or experimental detail do you think this audit is still missing?
```

## 2. OpenAI Developer Community

Destination: https://community.openai.com/c/codex/

Posts in this channel should teach something. Lead with the evidence synthesis and link the repository only after the useful content.

### Title

```text
What 2026 conference papers suggest Codex still struggles with—and what methods help
```

### Body

```markdown
I audited the 2026 conference literature for papers that run Codex CLI or Claude Code as complete products rather than merely using an OpenAI or Anthropic model.

Across the 13 papers that currently pass the strict scope gate, the recurring pattern is not “the agent cannot write code.” The harder problems appear when work must preserve state across a repository, compose multiple operational stages, use domain-specific evidence, or independently verify completion.

Four mechanisms recur across the papers:

1. independent executable verification through tests, sandboxes, static analyzers, fuzzers, or render review;
2. persistent task state such as repository graphs or findings memory;
3. domain-grounded context from retrieval, AST/LSP signals, or repository instructions;
4. structured exploration through dependency-aware plans, search, or specialist parallelism.

Each inference is mapped to the exact paper result, model, evidence location, and comparison caveat here:
https://micromilo.github.io/awesome-claude-code-codex-papers/insights/

I maintain the catalog and would value counterexamples. Which of these failure modes best matches your real Codex work, and which one looks overstated?
```

## 3. Hacker News

Submit as a **regular HN story**, not a Show HN. The official Show HN rules explicitly classify lists and other reading material as off-topic for Show HN: https://news.ycombinator.com/showhn.html

### Title

```text
A catalog of papers that actually run Claude Code or Codex CLI
```

### URL

```text
https://micromilo.github.io/awesome-claude-code-codex-papers/
```

### First comment

```text
Author here. I built this because searches for “Codex papers” often mix together three different things: the historical Codex model, GPT-family API use, and the actual Codex CLI product.

The catalog uses a stricter gate: a formally accepted 2026 paper must run Codex CLI or Claude Code as a product-level agent. It currently indexes 18,269 official conference-list records, with 13 papers passing that gate. Every record keeps an explicit disposition, and failed access stays pending rather than becoming a silent exclusion.

The most surprising result for me was how rarely papers hold both model and budget constant. I would especially appreciate criticism of the inclusion rule, audit trail, or the evidence-backed synthesis.
```

Do not ask for votes or coordinate comments. The official HN guidelines prohibit voting manipulation: https://news.ycombinator.com/newsguidelines.html

## 4. r/ChatGPTCoding weekly self-promotion thread

Do not create a standalone launch post. Current moderation messages route project promotion, including free/open-source projects, to the weekly self-promotion thread and require affiliation disclosure.

```text
Disclosure: I maintain this free, MIT-licensed project.

I built a strict catalog of 2026 conference papers that actually run Claude Code or Codex CLI as products. It indexes 18,269 official-list records, keeps excluded and pending decisions auditable, and currently has 13 included papers with exact models, evidence locations, and caveats.

Catalog: https://micromilo.github.io/awesome-claude-code-codex-papers/
Reusable conference-census skill: https://micromilo.github.io/awesome-claude-code-codex-papers/skill/

I would value pointers to formally accepted 2026 papers that use either product and are missing from the catalog.
```

Do not post this to r/ClaudeAI unless you can truthfully satisfy its current Showcase rule, which requires Claude or Claude Code to be central to how the project was built and asks for a detailed, low-marketing explanation: https://www.reddit.com/r/ClaudeAI/comments/1qe5wtt/rule_7_is_getting_a_glowup_less_spam_more_how_the/

## 5. Paper-author outreach

This is often more valuable than a broad launch. Contact only authors whose paper has an included evidence page. Personalize the result, model, and evidence location; do not send a bulk blast.

### Subject

```text
Evidence record for your [Conference 2026] paper in an open coding-agent catalog
```

### Message

```text
Hello [Name],

I maintain an open catalog of formally accepted papers that evaluate Claude Code or Codex CLI as products. I added an evidence record for “[Paper title]” here:

[per-paper evidence URL]

The record currently captures [product/model], [reported result], and [source location]. It also states the comparison caveat rather than treating the result as a leaderboard entry.

Would you be willing to check the record for factual errors or missing configuration details? If it is accurate and useful, sharing it with readers of your paper would also help the catalog reach the right research community.

Thank you,
MicroMilo
```

## Measurement sheet

Record one row immediately before each post and again after 24 hours and seven days.

| Date | Channel | Exact URL used | GitHub unique visitors | Unique clones | Stars | Referrer visible | Useful corrections | Notes |
|---|---|---|---:|---:|---:|---|---:|---|
| | | | | | | | | |

Success is not only stars. Track paper corrections, author replies, qualified contributors, RSS subscribers where visible, and missing-paper reports.
