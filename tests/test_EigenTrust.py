import unittest
import sys
import numpy
import numpy.linalg as la
sys.path.append('../')
from centrality.eigentrust import EigenTrust
from simulation.votematrix import VoteMatrix


class TestEigenTrust(unittest.TestCase):
    def test_eigentrust_trivial(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[1, 2] = 1
        votes.positive[2, 3] = 1
        votes.positive[3, 0] = 1

        eigentrust = EigenTrust()

        m = eigentrust.apply(votes)

        assert len(m) == 4
        for score in m:
            assert score == 0.25

    def test_eigentrust(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[0, 2] = 1
        votes.positive[2, 1] = 1
        votes.positive[3, 0] = 1
        votes.positive[3, 2] = 4

        eigentrust = EigenTrust(lambda x: la.norm(x, numpy.inf))

        m = eigentrust.apply(votes)

        assert numpy.abs(m[0] - 0.139) < 0.01
        assert numpy.abs(m[1] - 0.465) < 0.01
        assert numpy.abs(m[2] - 0.279) < 0.01
        assert numpy.abs(m[3] - 0.117) < 0.01


if __name__ == '__main__':
    unittest.main()
