from simulation.community import Community
import numpy
import random

class Student:
    def __init__(self, label, actions):
        self.label = label
        self.actions = actions
        self.friends = list()
        actionSum = sum(tup[0] for tup in actions) 
        assert numpy.isclose(actionSum, 1)

    def setup(self, id, community:Community):
        self.community = community
        self.studentId = id

    def addFriends(self, friendList):
        self.friends = friendList

    def step(self):
        dice = random.uniform(0,1)
        acumulatedSums = [tup[0] for tup in self.actions]
        chances = numpy.cumsum(acumulatedSums)
        for idx, val in enumerate(chances):
            if val > dice:
                self.actions[idx][1](self)    
                break

    def copy(self):
        student = Student(self.label, self.actions)
        student.friends = self.friends
        return student