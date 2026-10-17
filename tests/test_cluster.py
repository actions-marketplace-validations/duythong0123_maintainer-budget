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

    def test_clusters_real_codex_camelcase_reviews_by_identifier_anchor(self):
        comments = [
            ReviewComment(
                "openai/codex",
                6467,
                "https://github.com/openai/codex/pull/6467#discussion_r2512444488",
                "bolinfest",
                'FYI, we are using "camelCase" throughout the V2 protocol for codex app-server, so let\'s follow suit here.',
                path="codex-rs/execpolicy2/src/decision.rs",
                author_type="User",
                author_association="COLLABORATOR",
            ),
            ReviewComment(
                "openai/codex",
                8442,
                "https://github.com/openai/codex/pull/8442#discussion_r2644310695",
                "bolinfest",
                'instead of an individual alias for each, add #[serde(rename_all = "camelCase")] to the struct declaration. Is there any reason we should support two names for each field?',
                path="codex-rs/network-proxy/src/config.rs",
                author_type="User",
                author_association="COLLABORATOR",
            ),
        ]
        candidates = cluster_comments(comments, min_unique_prs=2)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].unique_prs, 2)
        self.assertIn("camelcase", candidates[0].tokens)

    def test_common_manifest_name_is_not_a_strong_anchor(self):
        comments = [
            c(10, "Please update package.json for the release metadata."),
            c(20, "The package.json dependency range needs changing."),
        ]
        self.assertEqual(cluster_comments(comments, similarity_threshold=0.5, min_unique_prs=2), [])

    def test_does_not_cluster_same_pr_only(self):
        comments = [
            c(10, "Please use nextTestSetup for this fixture."),
            c(10, "Please use nextTestSetup here too."),
        ]
        self.assertEqual(cluster_comments(comments, similarity_threshold=0.2, min_unique_prs=2), [])


if __name__ == "__main__":
    unittest.main()
