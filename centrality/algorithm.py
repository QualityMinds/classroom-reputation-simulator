from abc import ABC, abstractmethod

from simulation.votematrix import VoteMatrix


class Algorithm(ABC):

    @abstractmethod
    def apply(self, votes: VoteMatrix):
        pass

    def notify_intermediary_result(self, step, data):
        pass
