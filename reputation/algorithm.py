class Algorithm(object):
    def get_raw_reputation(self, reputation_data):
        raise Exception("--- NEEDS TO BE OVERRIDDEN BY SUB TYPE ---")

    def receiveIntermediateReputationData(self, step, reputationData):
        return


from reputation.eigentrust import EigenTrust
from reputation.indegree import InDegree
from reputation.indegree_positive import InDegreePositive
from reputation.pagerank import PageRank

def allAlgorithms():
    return [InDegree(), InDegreePositive(), EigenTrust(), PageRank()]