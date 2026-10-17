---
name: maintainer-budget
summary: Review evidence-backed repository rule candidates produced from recurring human code review feedback.
---

# Maintainer Budget candidate review skill

Use this skill when a Maintainer Budget audit has produced candidate repository rules.

## Inputs
- Maintainer Budget Markdown/JSON audit output
- the linked source review comments
- existing repository instructions such as `AGENTS.md`

## Workflow
1. Treat every candidate as a proposal, not policy.
2. Verify that evidence comes from trusted human reviewers and spans multiple PRs.
3. Check whether the feedback is repository-specific and reusable, not a one-off request.
4. Check for contradictory or newer evidence that makes the candidate stale.
5. Prefer the smallest scoped rule that captures the repeated convention.
6. Preserve evidence links in any proposed instruction change.
7. Never auto-approve or silently write a candidate into repository policy.

## Output
For each candidate, return exactly one recommendation:
- **Accept** — reusable, current, and well-supported.
- **Edit** — useful but needs narrower wording/scope.
- **Reject** — one-off, noisy, generic, contradictory, or stale.

Include the evidence that supports the recommendation.
