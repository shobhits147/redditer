import unittest
import test_setup
from app.filters import BaseFilter


class FakeAuthor:
    def __init__(self, author):
        self.name = author

class FakeClass:
    def __init__(self, body, author, title="title", selftext="selftext"):
        self.body = body
        self.author = FakeAuthor(author)
        self.title = title
        self.selftext = selftext

class TestBaseFilter(unittest.TestCase):

    def test_keywordCheck(self):
        b = BaseFilter({"keywords": ["randomkeyword"]})
        self.assertEqual(b.keywordCheck("contains randomkeyword"), True)
        self.assertEqual(b.keywordCheck("does not contain keyword"), False)

    def test_ignoreAuthors(self):
        b = BaseFilter({"keywords": ["randomkeyword"], "exclude": {"authors": ["shobhit"]}})
        self.assertEqual(b.ignoreAuthors("shobhit"), True)
        self.assertEqual(b.ignoreAuthors("shekhar"), False)

    def test_basicCommentFilters(self):
        b = BaseFilter({"keywords": ["randomkeyword"], "exclude": {"authors": ["shobhit"]}})
        fake_object = FakeClass("randomkeyword", "shekhar")
        self.assertEqual(b.basicCommentFilters(fake_object), fake_object)
        fake_object = FakeClass("diffkeyword", "shekhar")
        self.assertEqual(b.basicCommentFilters(fake_object), None)

    def test_basicSubmissionFilters(self):
        b = BaseFilter({"keywords": ["randomkeyword"], "exclude": {"authors": ["shobhit"]}})
        fake_object = FakeClass("randomkeyword", "shekhar", "randomkeyword")
        self.assertEqual(b.basicSubmissionFilters(fake_object), fake_object)
        fake_object = FakeClass("diffkeyword", "shekhar", "diffkeyword")
        self.assertEqual(b.basicSubmissionFilters(fake_object), None)

