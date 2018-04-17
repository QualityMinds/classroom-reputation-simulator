from reputation.power_iteration import power_iteration
import numpy as np
import numpy.linalg as la
from reputation.algorithm import Algorithm

class PageRank(Algorithm):
    def __init__(self, alpha = 0.15, norm = lambda x: la.norm(x, np.inf)):
        super(Algorithm, self).__init__()
        self.name = "PageRank"
        self.norm = norm
        self.alpha = alpha

    def row_stochastic(self, m):
        x, y = m.shape

        uniformProbability = 1.0 / x

        for i in range(0, y):
            totalRow = 0
            for j in range(0, x):
                totalRow += m[i,j]

            if totalRow > 0:
                for j in range(0, x):
                    m[i,j] /= totalRow
            else:
                for j in range(0, x):
                    m[i,j] = uniformProbability
        return m

    def get_raw_reputation(self, data):
        # G = alpha * S + (1 - alpha) * E 
        # where E is commonly doubly-stochastic
        votes = data.positiveVotes

        S = self.row_stochastic(votes)
        E = self.row_stochastic(np.ones(S.shape))
        G = self.alpha * S + (1 - self.alpha) * E
        
        _, cols = S.shape
        p0 = np.ones((1, cols)) / cols
        result, _, _ = power_iteration(G, p0, self.norm)
        
        return result.flat