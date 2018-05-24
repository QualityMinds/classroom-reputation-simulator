from centrality.power_iteration import power_iteration
from centrality.algorithm import Algorithm
import numpy as np
import numpy.linalg as la

from simulation.votematrix import VoteMatrix


class EigenTrust(Algorithm):
    def __init__(self, norm=lambda x: la.norm(x, np.inf)):
        super(Algorithm, self).__init__()
        self.name = "EigenTrust"
        self.norm = norm

    def apply(self, votes: VoteMatrix):
        votes = np.subtract(votes.positive, votes.negative)
        x, y = votes.shape

        for i in range(0, x):
            for j in range(0, y):
                votes[i,j] = np.max([votes[i,j], 0])
        
        uniform_prob = 1.0 / x

        for i in range(0, x):
            total_col = 0
            for j in range(0, y):
                total_col += votes[i,j]

            if total_col > 0:
                for j in range(0, y):
                    votes[i,j] /= total_col
            else:
                for j in range(0, y):
                    votes[i,j] = uniform_prob

        trust_vector = np.full([1, y], uniform_prob)
        trust_vector, _, _ = power_iteration(votes, trust_vector, self.norm, 0.02)
        return trust_vector.flat
