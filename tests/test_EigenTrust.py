import unittest
import sys
import numpy
import numpy.linalg as la
sys.path.append('../')
from reputation.eigentrust import EigenTrust
from simulation.reputation_data import ReputationData


class Test_test_EigenTrust(unittest.TestCase):
    def test_EigenTrustTrivial(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[1, 2] = 1
        repData.positiveVotes[2, 3] = 1
        repData.positiveVotes[3, 0] = 1

        eigentrust = EigenTrust()

        m = eigentrust.get_raw_reputation(repData)

        assert len(m) == 4
        for score in m:
            assert score == 0.25

    def test_EigenTrust(self):      
        repData = ReputationData(4)

        repData.positiveVotes[0, 1] = 1
        repData.positiveVotes[0, 2] = 1
        repData.positiveVotes[2, 1] = 1
        repData.positiveVotes[3, 0] = 1
        repData.positiveVotes[3, 2] = 4

        eigentrust = EigenTrust(lambda x: la.norm(x, numpy.inf))

        m = eigentrust.get_raw_reputation(repData)

        assert numpy.abs(m[0] - 0.139) < 0.001
        assert numpy.abs(m[1] - 0.465) < 0.001
        assert numpy.abs(m[2] - 0.279) < 0.001
        assert numpy.abs(m[3] - 0.117) < 0.001


if __name__ == '__main__':
    unittest.main()
