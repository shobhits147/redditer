#! usr/bin/env python3

import time
import sys
import threading
import os
import yaml
import logging

import reddit_helper
import dumper
import postman
import filters

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Aggregator:
    def __init__(self, redditHelper, config):
        logging.info("Initializing aggregator...")
        self.redditHelper = redditHelper
        self.submissions = []
        self.comments = []
        self.subreddits = self.redditHelper.userSubreddits()
        self.filters = filters.Filters(config)
        self.postMan = postman.PostMan(config.get("response"))
        self.dumper = dumper.Dumper(config)

    def submissionStream(self, subreddits):
        return self.redditHelper.startPostsStream("+".join(subreddits))

    def commentStream(self, subreddits):
        return self.redditHelper.startCommentsStream("+".join(subreddits))

    def aggregateSubmissions(self):
        submission_stream = self.submissionStream(self.subreddits)
        first = True
        while True:
            try:
                for submission in submission_stream:
                    if submission is None:
                        break
                    elif first is not True and self.filters.applyToSubmission(submission):
                        self.submissions.append(submission)
                        self.dumper.dumpSubmission([submission.id, submission.author, submission.url])
                        self.postMan.postComment(submission)
                time.sleep(10)
                first = False
            except KeyboardInterrupt:
                print('\n')
                sys.exit(0)
            except Exception as e:
                print('Error:', e)
                time.sleep(30)
                submission_stream = self.submissionStream(self.subreddits)

    def aggregateComments(self):
        comment_stream = self.commentStream(self.subreddits)
        first = True
        while True:
            try:
                for comment in comment_stream:
                    if comment is None:
                        break
                    elif first is not True and self.filters.applyToComment(comment):
                        self.comments.append(comment)
                        self.dumper.dumpComment([comment.id, comment.author])
                        self.postMan.postReply(comment)
                time.sleep(10)
                first = False
            except KeyboardInterrupt:
                print('\n')
                sys.exit(0)
            except Exception as e:
                print('Error:', e)
                time.sleep(30)
                comment_stream = self.commentStream(self.subreddits)

def resetResultFiles(submissionsFile, commentsFile):
    logging.info("Resetting result files: " + submissionsFile + "and" + commentsFile)
    try:
        os.remove(submissionsFile)
        os.remove(commentsFile)
    except OSError:
        pass

def loadConfig(path):
    logging.info("Loadin configuration from: " + path)
    with open(path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

def loadCreds(path):
    logging.info("Loading credentials from: " + path)
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
        creds['password'],
        config
    )
    aggregator = Aggregator(redditHelper, config)

    threads = []

    logging.info("Spawning submission and comment aggregator threads...")
    submissions = threading.Thread(target=aggregator.aggregateSubmissions)
    comments = threading.Thread(target=aggregator.aggregateComments)

    threads.append(submissions)
    threads.append(comments)

    submissions.start(), comments.start()
    logging.info("Threads started!!")
    logging.info("Listening for posts and comments...")
    for index, thread in enumerate(threads):
        thread.join()

if __name__ == "__main__":
    main()