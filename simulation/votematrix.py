import numpy as np


class VoteMatrix:
    def __init__(self, num_voters):
        self.num_voters = num_voters
        self.positive = np.zeros([num_voters, num_voters])
        self.negative = np.zeros([num_voters, num_voters])