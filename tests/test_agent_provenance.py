import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / ".github/scripts/agent_provenance.py"
spec = importlib.util.spec_from_file_location("agent_provenance", SCRIPT)
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)


class LabelExtractionTest(unittest.TestCase):
    def test_pr_labels_only_from_exact_lines(self):
        event = {"pull_request": {"number": 12, "body": (
            "Summary\nAI-Authored-With: Claude Code\n"
            "AI-Authored-With: Codex\nAI-Authored-With: Codex\n"
            "AI-Authored-With: Something else\n"
        )}}
        self.assertEqual(
            provenance.labels_for_event("pull_request", event),
            (12, ["authored-with:claude-code", "authored-with:codex"]),
        )

    def test_review_reads_review_body_not_pr_body(self):
        event = {
            "pull_request": {"number": 12, "body": "AI-Authored-With: Claude Code"},
            "review": {"body": "Looks good.\nAI-Reviewed-With: Codex"},
        }
        self.assertEqual(
            provenance.labels_for_event("pull_request_review", event),
            (12, ["reviewed-with:codex"]),
        )

    def test_no_marker_changes_nothing(self):
        event = {"pull_request": {"number": 2, "body": None}}
        self.assertEqual(provenance.labels_for_event("pull_request", event), (2, []))


if __name__ == "__main__":
    unittest.main()
