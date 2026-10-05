import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from multi_doc_compare.compare import DocComparator, jaccard
from multi_doc_compare.tokenize import tokenize, shingles


DOC_A = """Python 是一门通用编程语言。
Python 的 GIL 是全局解释器锁。
Python 主要用于数据科学。
这款产品售价 199 元。"""

DOC_B = """Python 是一门通用编程语言。
Python 的 GIL 不是全局解释器锁。
Python 还可以用于 Web 开发。
这款产品售价 299 元。"""


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "a.txt").write_text(DOC_A, encoding="utf-8")
        (self.root / "b.txt").write_text(DOC_B, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_tokenize(self):
        self.assertIn("python", tokenize("Python GIL"))

    def test_jaccard(self):
        self.assertEqual(jaccard({1, 2, 3}, {2, 3, 4}), 2 / 4)

    def test_consensus_found(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        rep = cmp.compare()
        texts = [c["a_text"] for c in rep.consensus] + [c["b_text"] for c in rep.consensus]
        self.assertTrue(any("通用编程语言" in t for t in texts))

    def test_contradiction_polarity(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        rep = cmp.compare()
        reasons = [c["reason"] for c in rep.contradictions]
        self.assertIn("肯否关系相反", reasons)

    def test_contradiction_number(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        rep = cmp.compare()
        reasons = [c["reason"] for c in rep.contradictions]
        self.assertIn("数字不一致", reasons)

    def test_unique_points(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        rep = cmp.compare()
        joined = " ".join(rep.unique_points.get("b.txt", []))
        self.assertIn("Web", joined)

    def test_answer(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        out = cmp.answer("GIL 是什么")
        self.assertIn("a.txt", out)
        self.assertGreater(len(out["a.txt"]), 0)

    def test_render(self):
        cmp = DocComparator([self.root / "a.txt", self.root / "b.txt"])
        rep = cmp.compare()
        out = rep.render()
        self.assertIn("共识", out)
        self.assertIn("矛盾", out)


if __name__ == "__main__":
    unittest.main()
