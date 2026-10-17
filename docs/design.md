# Design

## Product thesis

Every repeated code review should become repository memory.

Maintainer Budget looks for recurring human review feedback in merged pull requests and surfaces **candidate rules with provenance**. It is intentionally not a general AI code reviewer.

## MVP pipeline

```text
merged pull requests
        ↓
human review comments
        ↓
actionability filter
        ↓
TF-IDF similarity clustering
        ↓
recurrence across distinct PRs
        ↓
evidence-backed candidate rules
        ↓
human accept / edit / reject (future UI)
```

## Safety / trust properties

- Contributor code is never executed.
- Bot comments are ignored by default.
- The deterministic core makes no network calls except read-only GitHub API requests.
- A candidate cannot be created from only one PR.
- Candidate wording is copied from a real review comment; the MVP does not synthesize policy.
- Evidence URLs remain attached to the candidate.

## Why no LLM in the core

Semantic models can improve paraphrase recall later, but starting with an LLM would make it hard to distinguish a valuable repository norm from a plausible hallucination. The deterministic baseline gives us an auditable precision benchmark first.

## Planned layers

1. **v0.1 alpha** — CLI audit, deterministic clustering, Markdown/JSON evidence report.
2. **v0.1 beta** — review/decision file and controlled export to `AGENTS.md`.
3. **v0.3** — historical backtesting and stale-rule detection.
4. **v0.4** — optional Codex semantic clustering/synthesis, always citation-bound and human-approved.
5. **v1.0** — stable rule schema, GitHub Action, adoption/precision telemetry that is opt-in and privacy-preserving.
