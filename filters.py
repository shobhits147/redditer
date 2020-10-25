import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

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
            return False
        return True

    def basicCommentFilters(self, object):
        acceptable = self.keywordCheck(object.body) and self.ignoreAuthors(object.author.name)
        return object if acceptable else None

    def basicSubmissionFilters(self, object):
        acceptable = self.keywordCheck(object.title + " " + object.selftext) and self.ignoreAuthors(object.author.name)
        return object if acceptable else None

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