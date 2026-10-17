# Focused real-data demo: `openai/codex`

This is a deliberately small **regression fixture**, not a claim that Maintainer Budget has audited the whole Codex repository. It uses two public human review comments that express the same repository-specific naming convention with different prose.

## Evidence

1. [PR #6467 review comment](https://github.com/openai/codex/pull/6467#discussion_r2512444488) by `@bolinfest`:

   > FYI, we are using `"camelCase"` throughout the V2 protocol for `codex app-server`, so let's follow suit here.

2. [PR #8442 review comment](https://github.com/openai/codex/pull/8442#discussion_r2644310695) by `@bolinfest`:

   > instead of an individual `alias` for each, add `#[serde(rename_all = "camelCase")]` to the `struct` declaration.

The comments share little ordinary English vocabulary. The original TF-IDF baseline therefore missed the relationship. The current baseline recognizes `camelCase` as a structured repository-specific identifier anchor.

## Current alpha output

```text
MB-001

Candidate rule:
FYI, we are using "camelCase" throughout the V2 protocol for codex app-server,
so let's follow suit here.

Unique PRs: 2
Unique reviewers: 1
Shared signals: camelcase

Evidence:
- PR #6467 · codex-rs/execpolicy2/src/decision.rs
- PR #8442 · codex-rs/network-proxy/src/config.rs
```

The representative text is still a real maintainer comment; the tool does **not** synthesize a cleaner policy sentence yet. A maintainer would accept, edit, or reject the candidate before any export to `AGENTS.md`.

## Why this fixture matters

This example captures an important product requirement: repeated repository knowledge is often **semantically similar but lexically different**. The project should improve recall without giving up provenance or inventing rules.
