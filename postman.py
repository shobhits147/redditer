import logging

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