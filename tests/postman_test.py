import unittest
import test_setup
from app.postman import PostMan
from unittest.mock import MagicMock

class FakeComment:
    def __init__(self, id):
        self.id = id

    def reply(self):
        pass

class FakeSubmission:
    def __init__(self, id):
        self.id = id

    def reply(self):
        pass

class TestPostman(unittest.TestCase):

    def test_postComment(self):
        p = PostMan("My new response")
        fake_sub = FakeSubmission('hnauw6')
        fake_sub.reply = MagicMock()
        p.postComment(fake_sub)
        fake_sub.reply.assert_called_with("My new response")

    def test_postReply(self):
        p = PostMan("My new response")
        fake_sub = FakeComment('hnauw6')
        fake_sub.reply = MagicMock()
        p.postComment(fake_sub)
        fake_sub.reply.assert_called_with("My new response")