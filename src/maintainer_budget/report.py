from __future__ import annotations

import json
from pathlib import Path

from .models import CandidateRule, ReviewComment


def render_markdown(
    repo: str,
    all_comments: list[ReviewComment],
    actionable: list[ReviewComment],
    candidates: list[CandidateRule],
) -> str:
    lines = [
        "# Maintainer Budget audit",
        "",
        f"Repository: `{repo}`",
        "",
        "## Summary",
        "",
        f"- Review comments collected: **{len(all_comments)}**",
        f"- Human actionable comments: **{len(actionable)}**",
        f"- Repeated candidate rules: **{len(candidates)}**",
        "",
        "> Candidates are evidence, not policy. A maintainer should accept, edit, or reject each one before exporting it to repository instructions.",
        "",
    ]
    if not candidates:
        lines += ["No repeated candidate rules passed the current threshold.", ""]
        return "\n".join(lines)

    for c in candidates:
        lines += [
            f"## {c.rule_id}",
            "",
            f"> {c.representative}",
            "",
            f"- Unique PRs: **{c.unique_prs}**",
            f"- Unique reviewers: **{c.unique_reviewers}**",
            f"- Cluster score: **{c.score:.2f}**",
            f"- Shared signals: `{', '.join(c.tokens[:8])}`" if c.tokens else "- Shared signals: _none_",
            "",
            "Evidence:",
            "",
        ]
        for e in c.comments[:12]:
            path = f" — `{e.path}`" if e.path else ""
            excerpt = " ".join(e.body.strip().split())
            if len(excerpt) > 180:
                excerpt = excerpt[:177] + "..."
            lines.append(f"- PR #{e.pr_number} by @{e.author}{path}: [{excerpt}]({e.url})")
        if len(c.comments) > 12:
            lines.append(f"- … {len(c.comments) - 12} more evidence comments")
        lines.append("")
    return "\n".join(lines)


def write_json(path: str | Path, repo: str, all_comments, actionable, candidates) -> None:
    payload = {
        "schema_version": 1,
        "repository": repo,
        "stats": {
            "review_comments_collected": len(all_comments),
            "human_actionable_comments": len(actionable),
            "candidate_rules": len(candidates),
        },
        "candidates": [c.to_dict() for c in candidates],
    }
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
