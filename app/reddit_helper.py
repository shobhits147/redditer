import praw
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class RedditHelper:
    def __init__(self, client_id, client_secret, app_name, username, password, config):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=app_name,
            username=username,
            password=password
        )
        self.config = config

    def userSubreddits(self):
        subreddits = self.reddit.user.subreddits(limit=None)
        retVal = []
        blacklisted = self.config.get("exclude").get("subreddits")
        if blacklisted:
            logging.info("Ignoring blacklisted subreddits: " + str(blacklisted))
        for s in subreddits:
            if s.display_name not in blacklisted:
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