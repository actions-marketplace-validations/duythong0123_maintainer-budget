import unittest

from maintainer_budget.cluster import cluster_comments
from maintainer_budget.models import ReviewComment


def c(pr, body, author="alice", path="src/config.rs"):
    return ReviewComment("o/r", pr, f"https://example.test/{pr}", author, body, path=path, author_type="User")


class ClusterTests(unittest.TestCase):
    def test_clusters_repeated_feedback_across_prs(self):
        comments = [
            c(10, "Please use ConfigBuilder::default().build() for config loading."),
            c(20, "Use ConfigBuilder::default().build() instead of custom config loading."),
            c(30, "We should use ConfigBuilder::default().build() here.", author="bob"),
            c(40, "Please add a regression test for the parser.", path="tests/parser.rs"),
        ]
        candidates = cluster_comments(comments, similarity_threshold=0.25, min_unique_prs=2)
        self.assertTrue(candidates)
        top = candidates[0]
        self.assertEqual(top.unique_prs, 3)
        self.assertEqual(top.unique_reviewers, 2)
        self.assertIn("configbuilder::default", " ".join(top.tokens))

    def test_does_not_cluster_same_pr_only(self):
        comments = [
            c(10, "Please use nextTestSetup for this fixture."),
            c(10, "Please use nextTestSetup here too."),
        ]
        self.assertEqual(cluster_comments(comments, similarity_threshold=0.2, min_unique_prs=2), [])


if __name__ == "__main__":
    unittest.main()
