# Changelog

## 0.1.0a1 - Unreleased

- Read-only audit of recent merged GitHub pull requests.
- Filters bots and low-trust review authors by default.
- Finds likely actionable human review feedback.
- Deterministic TF-IDF/cosine clustering across distinct PRs.
- Structured identifier anchors bridge paraphrased feedback around stable repo-specific symbols such as `camelCase` or `nextTestSetup`.
- Regression fixture from real `openai/codex` review comments (#6467 and #8442).
- Evidence-backed Markdown and JSON candidate reports.
- No paid AI/API dependency and no automatic policy writes.
