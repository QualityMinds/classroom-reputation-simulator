from enum import Enum
from simulation.reputation_data import ReputationData
from simulation.artifact import Artefact, Quality
import random
import numpy as np
import secrets


class VoteConstraints(Enum):
    NONE = 0
    GOODART = 1
    BADART = 2
    FRIEND = 3


class Community:
    def __init__(self):
        self.artefacts = list()
        self.students = list()

    def update_progress(self, progress):
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress * 50), progress * 100), end="", flush=True)


    def run(self, reputationAlgorithms, steps, samples):
        allResults = list()
        scoreVector = []
        intermediateResultList = []
        for algIdx in range(len(reputationAlgorithms)):
            scoreVector.insert(algIdx, np.zeros((1, len(self.students))))
            intermediateResultList.insert(algIdx, list())

        for sample in range(samples):
            self.artefacts = list()
            self.votings = ReputationData(len(self.students))
            for step in range(steps):
                self.step()
                for alg in reputationAlgorithms:
                    alg.receiveIntermediateReputationData(step, self.votings)

            self.update_progress((sample + 1) / samples)

            for algIdx, alg in enumerate(reputationAlgorithms):
                intermediateResult = alg.get_raw_reputation(self.votings)

                preparedIntermediateResult = list()
                for student in self.students:
                    preparedIntermediateResult.append((intermediateResult[student.studentId], student.label, student.studentId))
                    preparedIntermediateResult = sorted(preparedIntermediateResult, key=lambda x: x[0])
                intermediateResultList[algIdx].append(preparedIntermediateResult)
                scoreVector[algIdx] = scoreVector[algIdx] + intermediateResult

        for algIdx, alg in enumerate(reputationAlgorithms):
            scoreVector[algIdx] /= samples
            scoreVector[algIdx] = scoreVector[algIdx].flat
            results = list()
            for student in self.students:
                results.append((scoreVector[algIdx][student.studentId], student.label, student.studentId))
                results = sorted(results, key=lambda x: x[0])
            allResults.append((alg.name, results, intermediateResultList[algIdx]))
        return allResults


    def step(self):
        random.shuffle(self.students)
        for st in self.students:
            st.step()

    def addStudents(self, prototype, count):
        for i in range(0, count):
            student = prototype.copy()
            student.setup(len(self.students), self)
            self.students.append(student)

    def addArtefact(self, artefact):
        self.artefacts.append(artefact)

    def addVote(self, voter:int, artefact:Artefact, quality:Quality):
        if quality == quality.BAD:
            self.votings.negativeVotes[voter, artefact.originator] += 1
        else:
            self.votings.positiveVotes[voter, artefact.originator] += 1

    def getOtherArtefacts(self, myId):
        candidates = [artf for artf in self.artefacts if not artf.originator == myId and not artf.hasVoted(myId)]
        return candidates

    def getOtherArtefactsOfQuality(self, myId, quality):
        candidates = [artf for artf in self.getOtherArtefacts(myId) if artf.quality == quality]
        return candidates

    def getOtherArtefactsMatchingMemberIds(self, myId, otherIds):
        candidates = self.getOtherArtefacts(myId)
        return [artf for artf in candidates if (artf.originator in otherIds)]

    def createPostAction(self, quality:Quality):
        return lambda x: self.addArtefact(Artefact(x.studentId, quality))

    def createVoteAction(self, quality:Quality, constraint:VoteConstraints):
        voteActions = {
            VoteConstraints.NONE : self.voteAny,
            VoteConstraints.GOODART : self.voteGoodArtefact,
            VoteConstraints.BADART : self.voteBadArtefact,
            VoteConstraints.FRIEND : self.voteFriend
        }
        return lambda x: voteActions.get(constraint)(x, quality)

    def createIdleAction(self):
        return lambda x: None

    def vote(self, id, quality, artefacts):
        if(len(artefacts) > 0):
            self.addVote(id, secrets.choice(artefacts), quality)

    def voteAny(self, student, quality):
        self.vote(student.studentId, quality, self.getOtherArtefacts(student.studentId))

    def voteGoodArtefact(self, student, quality):
        self.vote(student.studentId, quality, self.getOtherArtefactsOfQuality(student.studentId, Quality.GOOD))

    def voteBadArtefact(self, student, quality):
        self.vote(student.studentId, quality, self.getOtherArtefactsOfQuality(student.studentId, Quality.BAD))

    def voteFriend(self, student, quality):
        self.vote(student.studentId, quality, self.getOtherArtefactsMatchingMemberIds(student.studentId, student.friends))