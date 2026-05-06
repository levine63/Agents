import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from scripts import check_readme


WORKSPACE_TMP_ROOT = Path(__file__).resolve().parents[2] / ".tmp_tests"


class WorkspaceTempDirTestCase(unittest.TestCase):
    def make_workspace_temp_dir(self) -> Path:
        WORKSPACE_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = WORKSPACE_TMP_ROOT / uuid4().hex
        path.mkdir(parents=True, exist_ok=False)
        return path

    def remove_workspace_temp_dir(self, path: Path) -> None:
        shutil.rmtree(path, ignore_errors=True)


class CheckReadmeTests(WorkspaceTempDirTestCase):
    def test_good_readme_has_no_blocking_findings(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            (root / "examples" / "minimal").mkdir(parents=True)
            (root / "uv.lock").write_text("", encoding="utf-8")
            (root / "README.md").write_text(
                "# Demo\n\n"
                "## Genre\n\n"
                "library / tooling\n\n"
                "## Summary\n\n"
                "Short summary.\n\n"
                "## Quick Start\n\n"
                "```bash\n"
                "python ./scripts/run.py ./examples/minimal\n"
                "```\n\n"
                "**Expected output**\n\n"
                "```text\n"
                "./outputs/minimal/result.json\n"
                "```\n\n"
                "## Environment\n\n"
                "Python 3.11.\n\n"
                "## Data and Inputs\n\n"
                "Minimal example in ./examples/minimal.\n\n"
                "## Outputs\n\n"
                "See ./outputs.\n\n"
                "## Reproducibility\n\n"
                "Deterministic.\n\n"
                "## Tests and Validation\n\n"
                "pytest -q\n\n"
                "## Limitations and Risks\n\n"
                "A small demo.\n\n"
                "## Common Issues\n\n"
                "**Error:** example\n"
                "**Context:** demo\n"
                "**Fix:** retry\n\n"
                "**Error:** second example\n"
                "**Context:** demo\n"
                "**Fix:** retry\n\n"
                "## File Structure\n\n"
                "See repo tree.\n\n"
                "## Contributing\n\n"
                "Use PRs.\n\n"
                "## License\n\n"
                "MIT\n\n"
                "## Contact\n\n"
                "Owner.\n",
                encoding="utf-8",
            )
            (root / "scripts").mkdir()
            (root / "scripts" / "run.py").write_text("print('ok')\n", encoding="utf-8")

            findings = check_readme.find_issues(root / "README.md")

            self.assertFalse(any(item.level == "BLOCKING" for item in findings))
        finally:
            self.remove_workspace_temp_dir(root)

    def test_missing_quick_start_is_blocking(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            target = root / "README.md"
            target.write_text("# Demo\n\n## Summary\n\nMissing quick start.\n", encoding="utf-8")

            findings = check_readme.find_issues(target)

            self.assertTrue(any(item.level == "BLOCKING" for item in findings))
        finally:
            self.remove_workspace_temp_dir(root)

    def test_llm_readme_warns_when_core_fields_missing(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            (root / "examples" / "minimal").mkdir(parents=True)
            target = root / "README.md"
            target.write_text(
                "# Demo\n\n"
                "## Genre\n\n"
                "mixed_or_llm_pipeline\n\n"
                "## Quick Start\n\n"
                "```bash\npython ./examples/minimal/run.py\n```\n\n"
                "**Expected output**\n\n"
                "```text\nok\n```\n",
                encoding="utf-8",
            )

            findings = check_readme.find_issues(target)
            messages = "\n".join(item.message for item in findings)

            self.assertIn("LLM pipeline README should mention model.", messages)
            self.assertIn("LLM pipeline README should mention temperature.", messages)
        finally:
            self.remove_workspace_temp_dir(root)


if __name__ == "__main__":
    unittest.main()
