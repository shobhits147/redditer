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