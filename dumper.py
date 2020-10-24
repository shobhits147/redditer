import csv
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Dumper:
    def __init__(self, config):
        self.submissionsFile = config["submissionsFile"]
        self.commentsFile = config["commentsFile"]

    def dumpSubmission(self, row):
        logging.info("Appending row: " + str(row) + " to " + self.submissionsFile)
        with open(self.submissionsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(row)

    def dumpComment(self, row):
        logging.info("Appending row: " + str(row) + " to " + self.commentsFile)
        with open(self.commentsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(row)