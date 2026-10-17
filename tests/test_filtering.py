import unittest

from maintainer_budget.filtering import filter_actionable, is_actionable
from maintainer_budget.models import ReviewComment


def c(body, *, author="alice", author_type="User", association="MEMBER", pr=1):
    return ReviewComment(
        "o/r", pr, "https://example.test", author, body,
        author_type=author_type, author_association=association,
    )


class FilteringTests(unittest.TestCase):
    def test_filters_bots_acknowledgements_and_untrusted_users(self):
        comments = [
            c("Please use the service layer instead.", pr=1),
            c("Looks good", pr=2),
            c("Please add tests for this behavior.", author="ci[bot]", author_type="Bot", pr=3),
            c("Please rewrite the whole module.", association="NONE", pr=4),
        ]
        out = filter_actionable(comments)
        self.assertEqual([x.pr_number for x in out], [1])

    def test_accepts_repo_style_directive(self):
        self.assertTrue(is_actionable(c('FYI, we are using "camelCase" throughout the V2 protocol, so let\'s follow suit here.')))

    def test_keeps_historical_comment_when_association_missing(self):
        self.assertTrue(is_actionable(c("Please use the service layer instead.", association=None)))


if __name__ == "__main__":
    unittest.main()
