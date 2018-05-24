import numpy
import numpy.linalg as la

from centrality.algorithm import Algorithm
# TODO: needed?
from simulation.votematrix import VoteMatrix


class InDegreePositive(Algorithm):
    def __init__(self, norm=lambda x: la.norm(x, 1)):
        super(Algorithm, self).__init__()
        self.name = "InDegreePositive"
        self.norm = norm

    def apply(self, votes: VoteMatrix):
        votes = votes.positive
        votes = votes.transpose()

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
