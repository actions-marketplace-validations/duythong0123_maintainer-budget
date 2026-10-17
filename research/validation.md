# Validation notes

This project starts from a falsifiable hypothesis:

> Maintainers repeatedly leave repository-specific review feedback that can be recovered from history and presented as evidence-backed candidate rules before it has to be repeated again.

## Initial public-data signals — 2026-10-17

These are **search-index signals, not acceptance-rate claims**. Keyword counts can include unrelated context, so every production candidate still requires evidence inspection and maintainer approval.

### openai/codex

A manual review of public PR discussions found the same app-server protocol convention in separate pull requests:

- PR #6467: reviewer notes that the V2 protocol uses `camelCase` and asks the change to follow suit.
- PR #8442: reviewer asks to use `#[serde(rename_all = "camelCase")]` rather than per-field aliases.

GitHub issue search with `in:comments` reported **15 PRs** whose comments contain both `camelCase` and `V2` at validation time.

### vercel/next.js

`nextTestSetup` is a repository-specific testing abstraction. In PR #93247, a maintainer repeatedly asks converted tests to move proxy setup into the isolated fixture so dependencies are declared through `nextTestSetup`.

GitHub issue search with `in:comments` reported **128 PRs** with `nextTestSetup` in comments at validation time.

### microsoft/vscode

VS Code has a strong disposable-registration idiom around `_register`. PR #81496 contains human review feedback requiring an old listener to be disposed. GitHub issue search with `in:comments` reported **493 PRs** with `this._register` in comments at validation time.

## What this validates

The data supports building a **discovery tool**. It does not yet prove that automatic synthesized rules are trustworthy. Therefore the MVP deliberately:

1. excludes bot feedback by default,
2. never invents a rule with an LLM,
3. uses a real human comment as the candidate text,
4. requires recurrence across different PRs,
5. keeps direct links to every evidence comment,
6. leaves policy approval to maintainers.

## Success metric

The key metric is **candidate acceptance rate**, not number of generated rules.

A future evaluation corpus should sample candidate clusters from multiple repositories and ask maintainers to label each as:

- accept as-is,
- useful after edit,
- reject/noise,
- stale/obsolete.

The project should not enable automatic `AGENTS.md` changes until accepted-or-useful-after-edit precision is high enough to justify maintainer attention.

## Focused regression fixture

The first deterministic baseline missed the two `openai/codex` `camelCase` comments because their surrounding prose was very different. That failure was useful: repository conventions are often paraphrased while one stable API/style identifier remains unchanged.

The alpha now extracts structured identifier anchors (for example `camelCase`, `nextTestSetup`, `_register`, or `ConfigBuilder::default`) and can use an exact shared anchor to bridge otherwise-low lexical similarity. Common manifest names such as `package.json` and `Cargo.toml` are excluded as generic anchors.

A regression test built from the real Codex PR #6467 and #8442 comments now detects one candidate spanning two distinct PRs. See [`demo-openai-codex.md`](demo-openai-codex.md).
