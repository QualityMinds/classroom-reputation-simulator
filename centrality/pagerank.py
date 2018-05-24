from centrality.power_iteration import power_iteration
import numpy as np
import numpy.linalg as la
from centrality.algorithm import Algorithm


class PageRank(Algorithm):
    def __init__(self, alpha=0.15, norm=lambda x: la.norm(x, np.inf)):
        super(Algorithm, self).__init__()
        self.name = "PageRank"
        self.norm = norm
        self.alpha = alpha

    @staticmethod
    def row_stochastic(m):
        x, y = m.shape

        uniform_probability = 1.0 / x

        for i in range(0, y):
            total_row = 0
            for j in range(0, x):
                total_row += m[i,j]

            if total_row > 0:
                for j in range(0, x):
                    m[i,j] /= total_row
            else:
                for j in range(0, x):
                    m[i,j] = uniform_probability
        return m

    def apply(self, votes):
        # G = alpha * S + (1 - alpha) * E 
        # where E is commonly doubly-stochastic
        votes = votes.positive

        S = self.row_stochastic(votes)
        E = self.row_stochastic(np.ones(S.shape))
        G = self.alpha * S + (1 - self.alpha) * E
        
        _, cols = S.shape
        p0 = np.ones((1, cols)) / cols
        result, _, _ = power_iteration(G, p0, self.norm)
        
        return result.flat
