from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality
from reputation.algorithm import allAlgorithms
from output.chart import chart
from output.metrics import printMetrics, printStdDevMetrics

if __name__ == '__main__':
    testName = "Collusion"
    community = Community()

    # Possible Actions
    postGoodArtefact = community.createPostAction(Quality.GOOD)
    postBadArtefact = community.createPostAction(Quality.BAD)
    voteBadNegative = community.createVoteAction(Quality.BAD, VoteConstraints.BADART)
    voteAnyNegative = community.createVoteAction(Quality.BAD, VoteConstraints.NONE)
    voteGoodPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)
    voteAnyPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.NONE)
    voteFriend = community.createVoteAction(Quality.GOOD, VoteConstraints.FRIEND)

    # Group normal
    normal = Student("normal",
        [
            (0.24, postGoodArtefact),
            (0.06, postBadArtefact),
            (0.28, voteBadNegative),
            (0.07, voteAnyNegative),
            (0.28, voteGoodPositive),
            (0.07, voteAnyPositive),
        ])
    community.addStudents(normal, 15)

    # Group mal
    mal = Student("mal",
        [
            (1, voteAnyNegative)
        ])
    community.addStudents(mal, 15)


    # Run
    groups = ('mal', 'normal')
    colors = {'mal': 'r', 'normal': 'c'}
    results = community.run(allAlgorithms(), 100, 100)
    for (name, result, intermediateResults) in results:
        c = chart(result, groups, colors, testName + " - " + name)
        path = testName + "-" + name +".png"
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        printMetrics(name, result, groups)
        printStdDevMetrics(name, intermediateResults, groups)