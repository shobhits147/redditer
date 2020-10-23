#! usr/bin/env python3

import praw
import time
import sys
import threading
import csv
import os
import yaml
import logging

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
    def __init__(self, config):
        self.submissionsFile = config["submissionsFile"]
        self.commentsFile = config["commentsFile"]

    def dumpSubmission(self, row):
        with open(self.submissionsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])

    def dumpComment(self, row):
        with open(self.commentsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])


class Aggregator:
    def __init__(self, redditHelper, config):
        self.redditHelper = redditHelper
        self.submissions = []
        self.comments = []
        self.filters = Filters(config)
        self.postMan = PostMan(config.get("response"))
        self.dumper = Dumper(config)

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
                        self.dumper.dumpSubmission(submission.id)
                        self.postMan.postComment(submission)
                time.sleep(10)
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
                        self.dumper.dumpComment(comment.id)
                        self.postMan.postReply(comment)
                time.sleep(10)
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
    def __init__(self, config):
        self.keywords = config["keywords"]

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
    def __init__(self, response):
        self.response = response

    def postComment(self, submission):
        try:
            if self.response:
                submission.reply(self.response)
        except Exception as e:
            logging.error("Exception while adding comment to submission: " + str(e))

    def postReply(self, comment):
        try:
            if self.response:
                comment.reply(self.response)
        except Exception as e:
            logging.error("Exception while adding reply to comment: " + str(e))

class Filters(BaseFilter):
    def __init__(self, config):
        BaseFilter.__init__(self, config)

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

def resetResultFiles(submissionsFile, commentsFile):
    try:
        os.remove(submissionsFile)
        os.remove(commentsFile)
    except OSError:
        pass

def loadConfig(path):
    with open(path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

def loadCreds(path):
    with open(path) as file:
        creds = yaml.load(file, Loader=yaml.FullLoader)
    return creds

def main():
    config = loadConfig("./config.yml")
    creds = loadCreds(config["credsPath"])

    resetResultFiles(config["submissionsFile"], config["commentsFile"])

    redditHelper = RedditHelper(
        creds['client-id'],
        creds['client-secret'],
        creds['app-name'],
        creds['username'],
        creds['password']
    )
    aggregator = Aggregator(redditHelper, config)

    threads = []

    submissions = threading.Thread(target=aggregator.aggregateSubmissions)
    comments = threading.Thread(target=aggregator.aggregateComments)

    threads.append(submissions)
    threads.append(comments)

    submissions.start(), comments.start()
    for index, thread in enumerate(threads):
        thread.join()

if __name__ == "__main__":
    main()