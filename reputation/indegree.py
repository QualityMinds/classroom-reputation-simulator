import numpy
import numpy.linalg as la
from reputation.algorithm import Algorithm


class InDegree(Algorithm):
    def __init__(self, norm = lambda x: la.norm(x, 1)):
        super(Algorithm, self).__init__()
        self.name = "InDegree"
        self.norm = norm

    def get_raw_reputation(self, reputationData):
        votes = numpy.subtract(reputationData.positiveVotes, reputationData.negativeVotes).T
        x, y = votes.shape
        aggregation = numpy.zeros(x)

        for i in range(0, x):
            total = 0
            for j in range(0, y):
                total += votes[i,j]
            aggregation[i] = total

        n = self.norm(aggregation)
        if n != 0:
            aggregation = aggregation / n
        return aggregation