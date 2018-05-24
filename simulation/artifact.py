from enum import Enum


class Quality(Enum):
    BAD = 0
    GOOD = 1


class Artifact:
    def __init__(self, creator: int, quality: Quality):
        self.creator = creator
        self.quality = quality
        self.voters = list()

    def vote(self, voter: int):
        self.voters.append(voter)

    def has_voted(self, voter: int):
        return voter in self.voters
