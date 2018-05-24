import numpy
import numpy.linalg as la
from centrality.algorithm import Algorithm
from simulation.votematrix import VoteMatrix


class InDegree(Algorithm):
    def __init__(self, norm=lambda x: la.norm(x, 1)):
        super(Algorithm, self).__init__()
        self.name = "InDegree"
        self.norm = norm

    def apply(self, votes: VoteMatrix):
        votes = numpy.subtract(votes.positive, votes.negative).T
        x, y = votes.shape
        aggregation = numpy.zeros(x)

        for i in range(0, x):
            total = 0
            for j in range(0, y):
                total += votes[i,j]
            aggregation[i] = total

        n = self.norm(aggregation)
        return aggregation / n if n != 0 else aggregation
