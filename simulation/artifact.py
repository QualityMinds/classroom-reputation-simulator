from enum import Enum


class Quality(Enum):
    BAD = 0
    GOOD = 1


class Artefact:
    def __init__(self, artefactOriginator: int, quality : Quality):
        self.originator = artefactOriginator
        self.quality = quality
        self.voters = list()

    def vote(self, voteOriginator : int):
        self.voters.append(voteOriginator)

    def hasVoted(self, voteOriginator : int):
        if voteOriginator in self.voters:
            return True
        else:
            return False

