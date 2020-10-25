import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class PostMan:
    def __init__(self, response):
        self.response = response

    def postComment(self, submission):
        try:
            if self.response:
                logging.info("Adding response: " + self.response + " to submission: " + submission.id)
                submission.reply(self.response)
        except Exception as e:
            logging.error("Exception while adding comment to submission: " + str(e))

    def postReply(self, comment):
        try:
            if self.response:
                logging.info("Adding reply: " + self.response + " to comment: " + comment.id)
                comment.reply(self.response)
        except Exception as e:
            logging.error("Exception while adding reply to comment: " + str(e))