import unittest
from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality


class Test_Community(unittest.TestCase):
    def test_Community(self):
        community = Community()

        postArtefactAction = community.createPostAction(Quality.GOOD)
        postVoteAction = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)

        student = Student("student", [(0.5, postArtefactAction), (0.5, postVoteAction)])
        community.addStudents(student, 10)


if __name__ == '__main__':
    unittest.main()
