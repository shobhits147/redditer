import praw

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