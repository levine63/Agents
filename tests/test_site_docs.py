import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"


def read_doc(name: str) -> str:
    return (DOCS_DIR / name).read_text(encoding="utf-8")


def nav_labels(html: str) -> list[str]:
    match = re.search(r'<nav class="nav">(.*?)</nav>', html, re.DOTALL)
    if not match:
        raise AssertionError("Navigation block not found")
    return re.findall(r"<a [^>]*>([^<]+)</a>", match.group(1))


class SiteDocsTests(unittest.TestCase):
    def test_top_navigation_is_consistent(self) -> None:
        expected = ["Home", "Publications", "Teaching & Materials", "CV"]

        for name in ("index.html", "levine-publications.html", "levine-teaching.html"):
            with self.subTest(page=name):
                self.assertEqual(nav_labels(read_doc(name)), expected)

    def test_home_current_areas_use_real_bullet_lists(self) -> None:
        html = read_doc("index.html")

        self.assertIn('class="topic-list"', html)
        self.assertNotIn(
            'Reducing lead exposure from consumer-product hazards during pregnancy and early childhood</a><br>',
            html,
        )
        self.assertNotIn(
            'Improving school handwashing</a><br>',
            html,
        )

    def test_publications_page_normalizes_reviewer_spot_checks(self) -> None:
        html = read_doc("levine-publications.html")

        self.assertIn(
            "<strong>Do Race, Age, and Gender Differences Affect Manager-Employee Relations?",
            html,
        )
        self.assertLess(
            html.index("Daddies, Devotion, and Dollars: How Do They Matter for Youth?"),
            html.index("Do Birds of a Feather Shop Together?"),
        )

    def test_teaching_card_summaries_use_full_contrast(self) -> None:
        html = read_doc("levine-teaching.html")

        self.assertRegex(
            html,
            r"\.card-summary\s*\{\s*color:\s*var\(--ink\);\s*\}",
        )
        self.assertEqual(html.count('class="card-summary"'), 4)

    def test_global_text_links_are_underlined(self) -> None:
        for name in ("index.html", "levine-publications.html", "levine-teaching.html"):
            with self.subTest(page=name):
                html = read_doc(name)
                self.assertRegex(
                    html,
                    r"a\s*\{\s*color:\s*inherit;\s*text-decoration:\s*underline;",
                )

    def test_small_labels_use_full_contrast_text(self) -> None:
        for name in ("index.html", "levine-publications.html", "levine-teaching.html"):
            with self.subTest(page=name):
                html = read_doc(name)
                self.assertRegex(
                    html,
                    r"\.section-label\s*\{\s*color:\s*var\(--ink\);",
                )

        index_html = read_doc("index.html")
        publications_html = read_doc("levine-publications.html")

        self.assertRegex(
            index_html,
            r"\.pub-meta\s*\{\s*color:\s*var\(--ink\);",
        )
        self.assertRegex(
            publications_html,
            r"\.pub-meta\s*\{\s*color:\s*var\(--ink\);",
        )

    def test_emerging_markets_links_use_local_docx_copy(self) -> None:
        expected_href = 'href="site_assets/syllabus257-2004.docx"'

        for name in ("index.html", "levine-teaching.html"):
            with self.subTest(page=name):
                html = read_doc(name)
                self.assertIn(expected_href, html)
                self.assertNotIn("syllabus257%202004.doc", html)

        self.assertTrue((DOCS_DIR / "site_assets" / "syllabus257-2004.docx").exists())


if __name__ == "__main__":
    unittest.main()
