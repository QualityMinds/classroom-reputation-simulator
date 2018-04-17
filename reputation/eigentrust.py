from reputation.power_iteration import power_iteration
from reputation.algorithm import Algorithm
import numpy as np
import numpy.linalg as la


class EigenTrust(Algorithm):
    def __init__(self, norm = lambda x: la.norm(x, np.inf)):
        super(Algorithm, self).__init__()
        self.name = "EigenTrust"
        self.norm = norm

    def get_raw_reputation(self, reputationData):
        votes = np.subtract(reputationData.positiveVotes, reputationData.negativeVotes)
        x, y = votes.shape

        for i in range(0, x):
            total = 0
            for j in range(0, y):
                votes[i,j] = np.max([votes[i,j], 0])
        
        uniformProbability = 1.0 / x

        for i in range(0, x):
            totalColScore = 0
            for j in range(0, y):
                totalColScore += votes[i,j]

            if totalColScore > 0:
                for j in range(0, y):
                    votes[i,j] /= totalColScore
            else:
                for j in range(0, y):
                    votes[i,j] = uniformProbability

        trustVector = np.full([1, y], uniformProbability)
        trustVector, _, _ = power_iteration(votes, trustVector, self.norm, 0.02)
        return trustVector.flat