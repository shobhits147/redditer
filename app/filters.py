import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

'''
1. It extracts only those posts or comments that include all of the keywords specified in `redditer/config.yml`
2. Subreddits mentioned in `exclude` section of `redditer/config.yml` are ignored even if the user is subscribed to it
3. Posts or comments made by authors mentioned in `exclude` section of `redditer/config.yml` are ignored.
'''
class BaseFilter:
    def __init__(self, config):
        self.keywords = config["keywords"]
        self.config = config

    def keywordCheck(self, body):
        for keyword in self.keywords:
            if keyword not in body:
                return False
        return True

    def ignoreAuthors(self, author):
        if author in self.config.get("exclude").get("authors"):
            logging.info("Ignoring post/comment from author " + author)
            return True
        return False

    def basicCommentFilters(self, object):
        acceptable = self.keywordCheck(object.body) and not self.ignoreAuthors(object.author.name)
        return object if acceptable else None

    def basicSubmissionFilters(self, object):
        acceptable = self.keywordCheck(object.title + " " + object.selftext) and not self.ignoreAuthors(object.author.name)
        return object if acceptable else None

'''
Driver class for all filters to be applied to the stream of data
'''
class Filters(BaseFilter):
    def __init__(self, config):
        BaseFilter.__init__(self, config)

    def applyToComment(self, object):
        object = self.basicCommentFilters(object)
        # call other filters if required e.g.:
        # object = SomeNewFilterClass.someNewFilter(object) if object is not None else None
        return object

    def applyToSubmission(self, object):
        object = self.basicSubmissionFilters(object)
        # call other filters if required e.g.:
        # object = SomeNewFilterClass.someNewFilter(object) if object is not None else None
        return object