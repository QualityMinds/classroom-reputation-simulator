import unittest
import sys
import numpy
sys.path.append('../')
from centrality.indegree import InDegree
from simulation.votematrix import VoteMatrix


class TestInDegree(unittest.TestCase):
    def test_indegree_trivial(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[1, 2] = 1
        votes.positive[2, 3] = 1
        votes.positive[3, 0] = 1

        in_degree = InDegree()

        m = in_degree.apply(votes)

        assert len(m) == 4
        for score in m:
            assert score == 0.25

    def test_indegree(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[0, 2] = 1
        votes.positive[2, 1] = 1
        votes.positive[3, 0] = 1
        votes.positive[3, 2] = 4

        in_degree = InDegree()

        m = in_degree.apply(votes)

        assert numpy.abs(m[0] - 0.125) < 0.001
        assert numpy.abs(m[1] - 0.250) < 0.001
        assert numpy.abs(m[2] - 0.625) < 0.001
        assert numpy.abs(m[3] - 0.000) < 0.001


if __name__ == '__main__':
    unittest.main()
