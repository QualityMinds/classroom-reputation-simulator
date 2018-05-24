import unittest
import sys
import numpy
sys.path.append('../')
from centrality.pagerank import PageRank
from simulation.votematrix import VoteMatrix


class TestPageRank(unittest.TestCase):
    def test_pagerank_trivial(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[1, 2] = 1
        votes.positive[2, 3] = 1
        votes.positive[3, 0] = 1

        pagerank = PageRank()

        m = pagerank.apply(votes)

        assert len(m) == 4
        for score in m:
            assert 0.24 < score < 0.26

    def test_pagerank(self):
        votes = VoteMatrix(4)

        votes.positive[0, 1] = 1
        votes.positive[0, 2] = 1
        votes.positive[2, 1] = 1
        votes.positive[3, 0] = 1
        votes.positive[3, 2] = 4

        pagerank = PageRank()

        m = pagerank.apply(votes)

        assert numpy.abs(m[0] - 0.229) < 0.001
        assert numpy.abs(m[1] - 0.280) < 0.001
        assert numpy.abs(m[2] - 0.267) < 0.001
        assert numpy.abs(m[3] - 0.223) < 0.001


if __name__ == '__main__':
    unittest.main()
