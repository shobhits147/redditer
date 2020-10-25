import unittest
import test_setup
from app.dumper import Dumper
from unittest import mock
import json

class TestDumper(unittest.TestCase):

    def test_dump_submission(self):
        d = Dumper({'submissionsFile': '/a/b/c/d', "commentsFile": '/e/f/g/h'})
        mock_open = mock.mock_open(read_data=json.dumps({}))
        with mock.patch('builtins.open', mock_open):
            d.dumpSubmission(["abc", "def", "ghi"])
            mock_open.assert_called_with('/a/b/c/d', 'a')

    def test_dump_comment(self):
        d = Dumper({'submissionsFile': '/a/b/c/d', "commentsFile": '/e/f/g/h'})
        mock_open = mock.mock_open(read_data=json.dumps({}))
        with mock.patch('builtins.open', mock_open):
            d.dumpComment(["abc", "def"])
            mock_open.assert_called_with('/e/f/g/h', 'a')
