from abc import ABC, abstractmethod
from simulation.action_profile import ActionProfile
from simulation.votematrix import VoteMatrix
import random
import numpy as np


class Community(ABC):
    def __init__(self):
        self.action_profile: ActionProfile = self.setup_action_profile()
        self.members = list()
        self.votes: VoteMatrix = None

    @abstractmethod
    def setup_action_profile(self):
        return None

    @abstractmethod
    def reset_run(self):
        pass

    @staticmethod
    def update_progress(progress):
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100), end="", flush=True)

    def step(self):
        random.shuffle(self.members)
        for st in self.members:
            st.step()

    def create_members_by_prototype(self, prototype, count):
        for i in range(0, count):
            member = prototype.copy(len(self.members), self)
            self.members.append(member)

    def simulate(self, algorithms, num_steps, num_runs):
        all_results = list()
        score_vector = []

        intermediate_results = []
        for alg_idx in range(len(algorithms)):
            score_vector.insert(alg_idx, np.zeros((1, len(self.members))))
            intermediate_results.insert(alg_idx, list())

        for run in range(num_runs):
            self.reset_run()
            for step in range(num_steps):
                self.step()
                for alg in algorithms:
                    # for stateful algorithms: feedback intermediate result
                    alg.notify_intermediary_result(step, self.votes)

            for alg_idx, alg in enumerate(algorithms):
                intermediate_result = alg.apply(self.votes)
                prepared_intermediate_result = sorted(
                    [(intermediate_result[m.member_id], m.label, m.member_id) for m in self.members],
                    key=lambda x: x[0])
                intermediate_results[alg_idx].append(prepared_intermediate_result)
                score_vector[alg_idx] = score_vector[alg_idx] + intermediate_result

            self.update_progress((run + 1) / num_runs)

        for alg_idx, alg in enumerate(algorithms):
            score_vector[alg_idx] /= num_runs
            score_vector[alg_idx] = score_vector[alg_idx].flat
            results = list()
            for member in self.members:
                results.append((score_vector[alg_idx][member.member_id], member.label, member.member_id))
                results = sorted(results, key=lambda x: x[0])
            all_results.append((alg.name, results, intermediate_results[alg_idx]))

        return all_results

