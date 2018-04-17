import unittest
import sys
import numpy
sys.path.append('../')
from reputation.pagerank import PageRank
from simulation.reputation_data import ReputationData


class Test_test_PageRank(unittest.TestCase):
    def test_PageRankTrivial(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[1, 2] = 1
        repData.positiveVotes[2, 3] = 1
        repData.positiveVotes[3, 0] = 1

        pagerank = PageRank()

        m = pagerank.get_raw_reputation(repData).T

        assert len(m) == 4
        for score in m:
            assert 0.24 < score < 0.26

    def test_PageRank(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[0, 2] = 1
        repData.positiveVotes[2, 1] = 1
        repData.positiveVotes[3, 0] = 1
        repData.positiveVotes[3, 2] = 4

        pagerank = PageRank()

        m = pagerank.get_raw_reputation(repData).T

        assert numpy.abs(m[0] - 0.229) < 0.001
        assert numpy.abs(m[1] - 0.280) < 0.001
        assert numpy.abs(m[2] - 0.267) < 0.001
        assert numpy.abs(m[3] - 0.223) < 0.001


if __name__ == '__main__':
    unittest.main()
