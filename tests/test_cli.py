import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from maintainer_budget.cli import main
from maintainer_budget.models import ReviewComment


class CliTests(unittest.TestCase):
    def test_audit_prints_candidate_report(self):
        comments = [
            ReviewComment(
                "o/r", 1, "https://example.test/1", "alice",
                "Please use ConfigBuilder::default().build() for config loading.",
                path="src/a.rs", author_type="User", author_association="MEMBER",
            ),
            ReviewComment(
                "o/r", 2, "https://example.test/2", "bob",
                "Use ConfigBuilder::default().build() instead of custom config loading.",
                path="src/b.rs", author_type="User", author_association="MEMBER",
            ),
        ]
        out = io.StringIO()
        with patch("maintainer_budget.cli.GitHubClient.collect", return_value=comments):
            with redirect_stdout(out):
                code = main(["audit", "o/r", "--similarity", "0.2"])
        self.assertEqual(code, 0)
        self.assertIn("MB-001", out.getvalue())
        self.assertIn("PR #1", out.getvalue())


if __name__ == "__main__":
    unittest.main()
