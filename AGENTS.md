# AGENTS.md

## Project purpose

Maintainer Budget discovers repeated human code-review feedback and presents it as evidence-backed repository rule candidates.

## Non-negotiable product rules

- Do not classify whether code was written by AI or a human.
- Do not execute contributor code while auditing review history.
- Do not turn one review comment into repository policy.
- Do not synthesize rules without preserving source evidence.
- Bot comments are excluded from the default learning corpus.
- Human approval is required before exporting a candidate into repository instructions.

## Development

```bash
python -m unittest discover -s tests -v
```

The core must remain usable without a paid AI/API provider. Optional semantic providers may be added only as a second layer.
