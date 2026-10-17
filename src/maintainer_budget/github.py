from __future__ import annotations

import json
import os
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import ReviewComment

API_ROOT = "https://api.github.com"


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str | None = None, *, timeout: int = 30):
        self.token = token or os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        self.timeout = timeout

    def _get(self, path: str, params: dict[str, object] | None = None):
        url = f"{API_ROOT}{path}"
        if params:
            url += "?" + urlencode(params)
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "maintainer-budget/0.1",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GitHubError(f"GitHub API {exc.code}: {body[:500]}") from exc
        except URLError as exc:
            raise GitHubError(f"GitHub API connection failed: {exc.reason}") from exc

    def _paged(self, path: str, *, max_pages: int = 10, extra: dict[str, object] | None = None):
        items = []
        for page in range(1, max_pages + 1):
            params = {"per_page": 100, "page": page}
            if extra:
                params.update(extra)
            batch = self._get(path, params)
            if not isinstance(batch, list):
                raise GitHubError(f"Expected list from {path}")
            items.extend(batch)
            if len(batch) < 100:
                break
            time.sleep(0.05)
        return items

    def merged_pull_requests(self, repo: str, *, max_prs: int = 100) -> list[dict]:
        pulls: list[dict] = []
        page = 1
        while len(pulls) < max_prs:
            batch = self._get(
                f"/repos/{repo}/pulls",
                {
                    "state": "closed",
                    "sort": "updated",
                    "direction": "desc",
                    "per_page": 100,
                    "page": page,
                },
            )
            if not batch:
                break
            pulls.extend(p for p in batch if p.get("merged_at"))
            if len(batch) < 100:
                break
            page += 1
        return pulls[:max_prs]

    def review_comments(self, repo: str, pr_number: int) -> list[ReviewComment]:
        raw = self._paged(f"/repos/{repo}/pulls/{pr_number}/comments", max_pages=5)
        comments: list[ReviewComment] = []
        for item in raw:
            user = item.get("user") or {}
            comments.append(
                ReviewComment(
                    repo=repo,
                    pr_number=pr_number,
                    url=item.get("html_url") or item.get("url") or "",
                    author=user.get("login") or "unknown",
                    author_type=user.get("type"),
                    body=item.get("body") or "",
                    path=item.get("path"),
                    created_at=item.get("created_at"),
                    author_association=item.get("author_association"),
                )
            )
        return comments

    def issue_comments(self, repo: str, pr_number: int) -> list[ReviewComment]:
        raw = self._paged(f"/repos/{repo}/issues/{pr_number}/comments", max_pages=5)
        comments: list[ReviewComment] = []
        for item in raw:
            user = item.get("user") or {}
            comments.append(
                ReviewComment(
                    repo=repo,
                    pr_number=pr_number,
                    url=item.get("html_url") or item.get("url") or "",
                    author=user.get("login") or "unknown",
                    author_type=user.get("type"),
                    body=item.get("body") or "",
                    path=None,
                    created_at=item.get("created_at"),
                    author_association=item.get("author_association"),
                )
            )
        return comments

    def collect(self, repo: str, *, max_prs: int = 100, include_issue_comments: bool = False) -> list[ReviewComment]:
        comments: list[ReviewComment] = []
        for pull in self.merged_pull_requests(repo, max_prs=max_prs):
            number = int(pull["number"])
            comments.extend(self.review_comments(repo, number))
            if include_issue_comments:
                comments.extend(self.issue_comments(repo, number))
        return comments
