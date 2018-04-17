import unittest
import sys
import numpy
sys.path.append('../')
from reputation.indegree import InDegree
from simulation.reputation_data import ReputationData


class Test_test_InDegree(unittest.TestCase):
    def test_InDegreeTrivial(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[1, 2] = 1
        repData.positiveVotes[2, 3] = 1
        repData.positiveVotes[3, 0] = 1

        inDegree = InDegree()

        m = inDegree.get_raw_reputation(repData)

        assert len(m) == 4
        for score in m:
            assert score == 0.25

    def test_InDegree(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[0, 2] = 1
        repData.positiveVotes[2, 1] = 1
        repData.positiveVotes[3, 0] = 1
        repData.positiveVotes[3, 2] = 4

        inDegree = InDegree()

        m = inDegree.get_raw_reputation(repData)

        assert numpy.abs(m[0] - 0.125) < 0.001
        assert numpy.abs(m[1] - 0.250) < 0.001
        assert numpy.abs(m[2] - 0.625) < 0.001
        assert numpy.abs(m[3] - 0.000) < 0.001


if __name__ == '__main__':
    unittest.main()
