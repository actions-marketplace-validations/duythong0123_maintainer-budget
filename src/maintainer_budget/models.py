from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class ReviewComment:
    repo: str
    pr_number: int
    url: str
    author: str
    body: str
    path: str | None = None
    created_at: str | None = None
    author_type: str | None = None
    author_association: str | None = None


@dataclass
class CandidateRule:
    rule_id: str
    representative: str
    comments: list[ReviewComment] = field(default_factory=list)
    score: float = 0.0
    tokens: list[str] = field(default_factory=list)

    @property
    def unique_prs(self) -> int:
        return len({c.pr_number for c in self.comments})

    @property
    def unique_reviewers(self) -> int:
        return len({c.author for c in self.comments})

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.rule_id,
            "candidate_rule": self.representative,
            "score": round(self.score, 3),
            "unique_prs": self.unique_prs,
            "unique_reviewers": self.unique_reviewers,
            "evidence": [asdict(c) for c in self.comments],
            "tokens": self.tokens,
        }
