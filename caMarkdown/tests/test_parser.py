import unittest
import caMarkdown

class TestRecord(unittest.TestCase):
    def setUp(self):
        pass
    def test_one(self):
        caMarkdown.fileParse("caMarkdown/tests/RecordTarget.md", "caMarkdown/tests/RecordMaster.md")
