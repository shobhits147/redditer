import csv

class Dumper:
    def __init__(self, config):
        self.submissionsFile = config["submissionsFile"]
        self.commentsFile = config["commentsFile"]

    def dumpSubmission(self, row):
        with open(self.submissionsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])

    def dumpComment(self, row):
        with open(self.commentsFile, 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([row])