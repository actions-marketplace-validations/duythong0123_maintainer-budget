# Maintainer Budget

> **Stop reviewing the same mistake twice.**

Maintainer Budget turns repeated **human code-review feedback** into **evidence-backed repository rule candidates** that maintainers can inspect before adding them to `AGENTS.md` or other agent instructions.

It is built around one problem: important project conventions often live in maintainer heads and old PR threads. New contributors — and coding agents — miss those conventions, so maintainers spend attention repeating the same review.

```text
PR #142  “Use the service layer here.”
PR #181  “API handlers should not call the DB directly.”
PR #247  “Please route this through UserService.”
                         ↓
                Maintainer Budget
                         ↓
Candidate MB-001
“API handlers should use the service layer for database access.”

Evidence: #142 · #181 · #247
Status: candidate — human approval required
```

## Why this is different

Maintainer Budget is **not** another AI code reviewer and it does not try to detect “AI code”. The alpha is deliberately conservative:

- no paid API required;
- bot comments are ignored by default;
- no contributor code is executed;
- a candidate must recur across different PRs;
- the candidate text comes from real human review feedback;
- every candidate keeps direct links to its evidence;
- nothing becomes repository policy automatically.

The goal is repository memory with provenance, not plausible-sounding rules.

## Alpha CLI

```bash
python -m pip install -e .
export GITHUB_TOKEN=...   # optional for public repos, recommended for rate limits
maintainer-budget audit openai/codex --max-prs 100
```

Write Markdown and JSON reports:

```bash
maintainer-budget audit owner/repo \
  --max-prs 200 \
  --output maintainer-budget.md \
  --json maintainer-budget.json
```

The output contains candidate rules plus the PR, reviewer, path, comment excerpt, and source URL for each piece of evidence.

## How it works

```text
GitHub merged PR history
        ↓
review comments from humans
        ↓
filter likely actionable feedback
        ↓
deterministic similarity clustering
        ↓
require recurrence across distinct PRs
        ↓
rank candidates + preserve provenance
```

The alpha uses a small TF-IDF/cosine baseline from the Python standard library. That is intentionally less “smart” than an LLM: it gives the project an auditable benchmark before an optional semantic layer is added.

## Example candidate

```text
MB-003

Candidate rule
──────────────
FYI, we are using "camelCase" throughout the V2 protocol,
so let's follow suit here.

Observed in: 4 PRs
Reviewers: 2
Evidence:
- PR #6467 · src/... · @reviewer · link
- PR #8442 · src/... · @reviewer · link
- ...
```

A maintainer should **accept, edit, or reject** the candidate. Automatic `AGENTS.md` modification is intentionally not part of the first alpha.

## Validation so far

Initial public-data checks found promising recurring repository-specific signals in `openai/codex`, `vercel/next.js`, and `microsoft/vscode`. The notes and limitations are documented in [`research/validation.md`](research/validation.md).

The metric that matters next is **candidate acceptance rate**, not stars or number of generated rules.

## Roadmap

- **0.1 alpha** — read-only GitHub audit + deterministic candidate clustering.
- **0.1 beta** — explicit accept/edit/reject decisions and controlled `AGENTS.md` export.
- **0.3** — backtest candidate rules against historical PRs; detect stale rules.
- **0.4** — optional Codex semantic layer for paraphrases, always evidence-bound and human-approved.
- **1.0** — stable rule schema + GitHub Action + documented evaluation corpus.

See [`docs/design.md`](docs/design.md).

## Contributing

The most valuable contribution is a real example of a candidate that is useful, misleading, duplicated, or stale. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Security

Maintainer Budget only reads GitHub metadata/comments in the alpha and never executes code from the target repository. See [`SECURITY.md`](SECURITY.md).

## License

MIT.
