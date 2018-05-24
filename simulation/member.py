from simulation.community import Community
import numpy
import random


class Member:
    def __init__(self, label, actions, member_id=None, community: Community=None):
        self.label = label
        self.actions = actions
        self.friends = list()
        self.community = community
        self.member_id = member_id

        action_sum = sum(tup[0] for tup in actions)
        assert numpy.isclose(action_sum, 1)

    def setup(self, member_id, community: Community):
        self.community = community
        self.member_id = member_id

    def set_friends(self, friends):
        self.friends = friends

    def step(self):
        dice = random.uniform(0, 1)
        acc = [tup[0] for tup in self.actions]
        chances = numpy.cumsum(acc)
        for idx, val in enumerate(chances):
            if val > dice:
                self.actions[idx][1](self)    
                break

    def copy(self, member_id, community):
        student = Member(self.label, self.actions, member_id, community)
        student.friends = self.friends
        return student
