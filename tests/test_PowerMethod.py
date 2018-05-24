import unittest
import numpy as np
from centrality import power_iteration as pow


class TestPowerMethod(unittest.TestCase):
    def test_powermethod(self):
        m = np.matrix([
            [ 1/60,  7/15, 7/15,  1/60,  1/60, 1/60],
            [ 1/6 ,  1/6 , 1/6 ,  1/6 ,  1/6 , 1/6 ],
            [19/60, 19/60, 1/60,  1/60, 19/60, 1/60],
            [ 1/60,  1/60, 1/60,  1/60,  7/15, 7/15],
            [ 1/60,  1/60, 1/60,  7/15,  1/60, 7/15],
            [ 1/60,  1/60, 1/60, 11/12,  1/60, 1/60]])
        p0 = np.ones((1, 6)) / 6
        p, _, _ = pow.power_iteration(m, p0)
    
        solution = [.03721, .05369, .04151, .3751, .206, .2862]
    
        check = np.all(np.around(p - solution, decimals=3) == 0)
        assert check


if __name__ == '__main__':
    unittest.main()
