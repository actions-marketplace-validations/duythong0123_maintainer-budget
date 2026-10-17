from __future__ import annotations

import re
from html import unescape

from .models import ReviewComment

BOT_SUFFIXES = ("[bot]", "-bot", "_bot")
TRUSTED_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR", "CONTRIBUTOR"}
DIRECTIVE_PATTERNS = (
    r"\bplease\b",
    r"\bprefer\b",
    r"\bshould\b",
    r"\bmust\b",
    r"\bavoid\b",
    r"\binstead\b",
    r"\bdo not\b",
    r"\bdon't\b",
    r"\bneeds? to\b",
    r"\bwe use\b",
    r"\bwe are using\b",
    r"\bwe should\b",
    r"\buse\b",
    r"\bkeep\b",
)
DIRECTIVE_RE = re.compile("|".join(DIRECTIVE_PATTERNS), re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
HTML_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

ACKS = {
    "thanks",
    "thank you",
    "looks good",
    "lgtm",
    "done",
    "fixed",
    "nice",
    "great",
    "approved",
}


def is_bot(comment: ReviewComment) -> bool:
    if (comment.author_type or "").lower() == "bot":
        return True
    login = comment.author.lower()
    return login.endswith(BOT_SUFFIXES) or "github-actions" in login


def is_trusted_human(comment: ReviewComment) -> bool:
    if is_bot(comment):
        return False
    association = (comment.author_association or "").upper()
    # Some historical API responses omit author_association. Keep those rather than
    # silently losing old review history; explicit NONE/first-time users are filtered.
    if not association:
        return True
    return association in TRUSTED_ASSOCIATIONS


def clean_text(text: str) -> str:
    text = unescape(text or "")
    text = FENCE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = HTML_RE.sub(" ", text)
    return WS_RE.sub(" ", text).strip()


def is_actionable(comment: ReviewComment) -> bool:
    if not is_trusted_human(comment):
        return False
    text = clean_text(comment.body)
    if len(text) < 18:
        return False
    if text.lower().strip(" .!:") in ACKS:
        return False
    if text.count("?") >= 2 and not DIRECTIVE_RE.search(text):
        return False
    return bool(DIRECTIVE_RE.search(text))


def filter_actionable(comments: list[ReviewComment]) -> list[ReviewComment]:
    return [c for c in comments if is_actionable(c)]
