from unittest.mock import patch
from unittest.mock import MagicMock
import test_setup
from app.reddit_helper import RedditHelper
import unittest

class FakeSubmissionComment:
    def __init__(self):
        pass

    def submissions(self, pause_after):
        pass

    def comments(self, pause_after):
        pass

class FakeSubreddit:
    def __init__(self, display_name):
        self.display_name = display_name
        self.stream = FakeSubmissionComment()


class TestRedditHelper(unittest.TestCase):

    def test_user_subreddits(self):
        rh = RedditHelper('abc', 'def', 'ghi', 'jkl', 'mno', {"exclude": {"subreddits": ['kjhfnjk']}})
        rh.reddit.user.subreddits = MagicMock(return_value=[FakeSubreddit("kjhfnjk")])
        self.assertEqual(rh.userSubreddits(), [])

    def test_start_posts_stream(self):
        rh = RedditHelper('abc', 'def', 'ghi', 'jkl', 'mno', {"exclude": {"subreddits": ['kjhfnjk']}})
        rh.reddit.subreddit = MagicMock(return_value=FakeSubreddit("kjhfnjk"))
        with patch.object(FakeSubmissionComment, 'submissions', return_value=None, auto_spec=True) as rs:
            rh.startPostsStream('some-subreddit')
            rs.assert_called_with(pause_after=-1)

    def test_start_comments_stream(self):
        rh = RedditHelper('abc', 'def', 'ghi', 'jkl', 'mno', {"exclude": {"subreddits": ['kjhfnjk']}})
        rh.reddit.subreddit = MagicMock(return_value=FakeSubreddit("kjhfnjk"))
        with patch.object(FakeSubmissionComment, 'comments', return_value=None, auto_spec=True) as rs:
            rh.startCommentsStream('some-subreddit')
            rs.assert_called_with(pause_after=-1)
















