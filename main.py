#! usr/bin/env python3

import time
import sys
import threading
import os
import yaml

import reddit_helper
import dumper
import postman
import filters

class Aggregator:
    def __init__(self, redditHelper, config):
        self.redditHelper = redditHelper
        self.submissions = []
        self.comments = []
        self.filters = filters.Filters(config)
        self.postMan = postman.PostMan(config.get("response"))
        self.dumper = dumper.Dumper(config)

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
            except KeyboardInterrupt:
                print('\n')
                sys.exit(0)
            except Exception as e:
                print('Error:', e)
                time.sleep(30)
                comment_stream = self.commentStream(subreddits)

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

    redditHelper = reddit_helper.RedditHelper(
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