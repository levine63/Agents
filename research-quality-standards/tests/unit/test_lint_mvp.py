import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from scripts import lint_mvp
from scripts import list_lint_targets


WORKSPACE_TMP_ROOT = Path(__file__).resolve().parents[2] / ".tmp_tests"


class WorkspaceTempDirTestCase(unittest.TestCase):
    def make_workspace_temp_dir(self) -> Path:
        WORKSPACE_TMP_ROOT.mkdir(parents=True, exist_ok=True)
        path = WORKSPACE_TMP_ROOT / uuid4().hex
        path.mkdir(parents=True, exist_ok=False)
        return path

    def remove_workspace_temp_dir(self, path: Path) -> None:
        shutil.rmtree(path, ignore_errors=True)


class PythonLintTests(WorkspaceTempDirTestCase):
    def test_python_happy_path_has_no_errors(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            target = root / "good.py"
            target.write_text(
                '"""\n'
                "Author: Test\n"
                "Date: 2026-05-06\n"
                "Purpose: Demo\n"
                "Inputs: none\n"
                "Not Yet Done: none\n"
                '"""\n'
                "import random\n\n"
                "random.seed(1)\n\n"
                "def main():\n"
                '    """Run demo."""\n'
                "    return random.random()\n",
                encoding="utf-8",
            )

            issues = lint_mvp.lint_file(target)

            self.assertFalse(any(issue.severity == "error" for issue in issues))
        finally:
            self.remove_workspace_temp_dir(root)

    def test_python_failure_path_flags_bare_except_and_missing_seed(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            target = root / "bad.py"
            target.write_text(
                "import random\n\n"
                "try:\n"
                "    x = random.random()\n"
                "except:\n"
                "    pass\n",
                encoding="utf-8",
            )

            issues = lint_mvp.lint_file(target)
            rule_ids = {issue.rule_id for issue in issues}

            self.assertIn("bare_except_absent", rule_ids)
            self.assertIn("randomness_seeded", rule_ids)
        finally:
            self.remove_workspace_temp_dir(root)


class StataLintTests(WorkspaceTempDirTestCase):
    def test_stata_failure_path_flags_missing_version_and_seed(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            target = root / "bad.do"
            target.write_text(
                "* Author: Test\n"
                "* Date: 2026-05-06\n"
                "* Purpose: Demo\n"
                "* Inputs: sample\n"
                "* Not Yet Done: none\n"
                "simulate x=r(mean), reps(100): summarize income\n",
                encoding="utf-8",
            )

            issues = lint_mvp.lint_file(target)
            rule_ids = {issue.rule_id for issue in issues}

            self.assertIn("stata_version_present", rule_ids)
            self.assertIn("stata_randomness_seeded", rule_ids)
        finally:
            self.remove_workspace_temp_dir(root)


class WritingLintTests(WorkspaceTempDirTestCase):
    def test_writing_failure_path_flags_placeholders(self) -> None:
        root = self.make_workspace_temp_dir()
        try:
            target = root / "draft.md"
            target.write_text(
                "# Draft\n\n"
                "Author: Test\n"
                "Date: 2026-05-06\n"
                "Intent: Demo\n"
                "Inputs: notes\n"
                "Not Yet Done: fill refs\n\n"
                "TBD: insert citation here.\n",
                encoding="utf-8",
            )

            issues = lint_mvp.lint_file(target)
            rule_ids = {issue.rule_id for issue in issues}

            self.assertIn("placeholder_text_scan", rule_ids)
        finally:
            self.remove_workspace_temp_dir(root)


class ChangedTargetTests(unittest.TestCase):
    def test_normalize_changed_paths_keeps_supported_files_only(self) -> None:
        raw_paths = [
            "scripts/lint_mvp.py",
            "templates/example.md",
            "generated/lint/report.md",
            "notes.txt",
            "src/example.do",
        ]

        targets = list_lint_targets.normalize_changed_paths(raw_paths)

        self.assertEqual(
            targets,
            [
                "scripts/lint_mvp.py",
                "src/example.do",
                "templates/example.md",
            ],
        )

    def test_normalize_changed_paths_deduplicates_and_skips_tmp_paths(self) -> None:
        raw_paths = [
            ".tmp_tests/tmp1/bad.py",
            "scripts/lint_mvp.py",
            "scripts/lint_mvp.py",
            "scripts/__pycache__/cached.py",
        ]

        targets = list_lint_targets.normalize_changed_paths(raw_paths)

        self.assertEqual(targets, ["scripts/lint_mvp.py"])


if __name__ == "__main__":
    unittest.main()
