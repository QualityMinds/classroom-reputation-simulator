import numpy

class ReputationData:

    def __init__(self, numStudents):
        self.numStudents = numStudents;
        self.positiveVotes = numpy.zeros([numStudents, numStudents])
        self.negativeVotes = numpy.zeros([numStudents, numStudents])