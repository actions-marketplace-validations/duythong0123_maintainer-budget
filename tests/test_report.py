import unittest

from maintainer_budget.models import CandidateRule, ReviewComment
from maintainer_budget.report import render_markdown


class ReportTests(unittest.TestCase):
    def test_report_keeps_evidence_urls(self):
        comment = ReviewComment(
            "o/r", 42, "https://github.com/o/r/pull/42#discussion_r1", "alice",
            "Please use the service layer instead.", path="src/api/users.ts", author_type="User"
        )
        candidate = CandidateRule("MB-001", comment.body, [comment], 0.91, ["service", "layer"])
        text = render_markdown("o/r", [comment], [comment], [candidate])
        self.assertIn("MB-001", text)
        self.assertIn("PR #42", text)
        self.assertIn(comment.url, text)


if __name__ == "__main__":
    unittest.main()
