#! usr/bin/env python3

# https://www.storybench.org/how-to-scrape-reddit-with-python/
# https://github.com/bag-man/newpost
# https://praw.readthedocs.io/en/v6.1.1/code_overview/models/multireddit.html?highlight=multi#praw.models.Multireddit.stream

import praw
import pandas as pd
import datetime as dt
import time
import sys
import logging
import threading
import csv

class RedditHelper:
    def __init__(self, client_id, client_secret, app_name, username, password):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=app_name,
            username=username,
            password=password
        )

    def userSubreddits(self):
        subreddits = self.reddit.user.subreddits(limit=None)
        retVal = []
        for s in subreddits:
            retVal.append(s.display_name)
        return retVal

    def printRedditObject(self):
        print(self.reddit)

    def startPostsStream(self, subreddits):
        submission_stream = self.reddit.subreddit(subreddits).stream.submissions(pause_after=-1)
        return submission_stream

    def startCommentsStream(self, subreddits):
        comments_stream = self.reddit.subreddit(subreddits).stream.comments(pause_after=-1)
        return comments_stream

class Dumper:
    submissionsFile = "/usr/local/share/filtered-submissions.csv"
    commentsFile = "/usr/local/share/filtered-comments.csv"

    @classmethod
    def dumpSubmission(cls, row):
        with open(cls.submissionsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])

    @classmethod
    def dumpComment(cls, row):
        with open(cls.commentsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])


class Aggregator:
    def __init__(self, redditHelper):
        self.redditHelper = redditHelper
        self.submissions = []
        self.comments = []
        self.filters = Filters()

    def submissionStream(self, subreddits):
        return self.redditHelper.startPostsStream("+".join(subreddits))

    def commentStream(self, subreddits):
        return self.redditHelper.startCommentsStream("+".join(subreddits))

    def aggregateSubmissions(self):
        subreddits = self.redditHelper.userSubreddits()
        submission_stream = self.submissionStream(subreddits)
        first = True
        while True:
            try:
                for submission in submission_stream:
                    if submission is None:
                        break
                    elif first is not True and self.filters.applyToSubmission(submission):
                        self.submissions.append(submission)
                        Dumper.dumpSubmission(submission.id)
                time.sleep(5)
                first = False
                print("submissions: %s" % self.submissions)
            except KeyboardInterrupt:
                print('\n')
                sys.exit(0)
            except Exception as e:
                print('Error:', e)
                time.sleep(30)
                submission_stream = self.submissionStream(subreddits)

    def aggregateComments(self):
        subreddits = self.redditHelper.userSubreddits()
        comment_stream = self.commentStream(subreddits)
        first = True
        while True:
            try:
                for comment in comment_stream:
                    if comment is None:
                        break
                    elif first is not True and self.filters.applyToComment(comment):
                        self.comments.append(comment)
                        Dumper.dumpComment(comment.id)
                time.sleep(5)
                first = False
                print("comments: %s" % self.comments)
            except KeyboardInterrupt:
                print('\n')
                sys.exit(0)
            except Exception as e:
                print('Error:', e)
                time.sleep(30)
                comment_stream = self.commentStream(subreddits)

class BaseFilter:
    def __init__(self):
        self.keywords = ["hbinvhuds", "funky-new-keyword"]

    def baseCommentFilters(self, object):
        for keyword in self.keywords:
            if keyword not in object.body:
                return None
        return object

    def baseSubmissionFilters(self, object):
        for keyword in self.keywords:
            if keyword not in (object.title + " " + object.selftext):
                return None
        return object

class PostMan:
    def __init__(self):
        pass

    def postComment(self):
        pass

    def postReply(self):
        pass

class Filters(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)

    def applyToComment(self, object):
        object = self.baseCommentFilters(object)
        # call other filters if required e.g.:
        # object = SomeNewFilterClass.someNewFilter(object) if object is not None else None
        return object

    def applyToSubmission(self, object):
        object = self.baseSubmissionFilters(object)
        # call other filters if required e.g.:
        # object = SomeNewFilterClass.someNewFilter(object) if object is not None else None
        return object

def main():
    # TODO: reset result files before execution
    # TODO: take creds as argument, take response as argument
    # TODO: take keywords as arguments
    redditHelper = RedditHelper('client-id', 'client-secret', 'app-name', 'username', 'password')
    aggregator = Aggregator(redditHelper)
    postman = PostMan()

    threads = []

    submissions = threading.Thread(target=aggregator.aggregateSubmissions)
    comments = threading.Thread(target=aggregator.aggregateComments)
    postcomment = threading.Thread(target=postman.postComment)
    postreply = threading.Thread(target=postman.postReply)

    threads.append(submissions)
    threads.append(comments)
    threads.append(postcomment)
    threads.append(postreply)

    submissions.start(), comments.start()
    for index, thread in enumerate(threads):
        thread.join()

if __name__ == "__main__":
    main()