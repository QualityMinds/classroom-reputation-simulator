from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality
from reputation.algorithm import allAlgorithms
from output.chart import chart
from output.metrics import printMetrics, printStdDevMetrics

if __name__ == '__main__':
    testName = "Productivity-low"
    community = Community()

    # Possible Actions
    postGoodArtefact = community.createPostAction(Quality.GOOD)
    postBadArtefact = community.createPostAction(Quality.BAD)
    voteBadNegative = community.createVoteAction(Quality.BAD, VoteConstraints.BADART)
    voteAnyNegative = community.createVoteAction(Quality.BAD, VoteConstraints.NONE)
    voteGoodPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)
    voteAnyPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.NONE)

    # Group low
    lowStudent = Student("low",
        [
            (0.02, postGoodArtefact),
            (0.18, postBadArtefact),
            (0.04, voteBadNegative),
            (0.36, voteAnyNegative),
            (0.04, voteGoodPositive),
            (0.36, voteAnyPositive),
        ])
    community.addStudents(lowStudent, 10)

    # Group average
    avgStudent = Student("avg",
        [
            (0.05, postGoodArtefact),
            (0.45, postBadArtefact),
            (0.025, voteBadNegative),
            (0.225, voteAnyNegative),
            (0.025, voteGoodPositive),
            (0.225, voteAnyPositive),
        ])
    community.addStudents(avgStudent, 10)

    # Group high
    highStudent = Student("high",
        [
            (0.08, postGoodArtefact),
            (0.72, postBadArtefact),
            (0.01, voteBadNegative),
            (0.09, voteAnyNegative),
            (0.01, voteGoodPositive),
            (0.09, voteAnyPositive),
        ])

    community.addStudents(highStudent, 10)

    # Run
    groups = ('low', 'avg', 'high')
    colors = {'low': 'r', 'avg': 'yellow', 'high': 'g'}
    results = community.run(allAlgorithms(), 100, 100)
    for (name, result, intermediateResults) in results:
        c = chart(result, groups, colors, testName + " - " + name)
        path = testName + "-" + name +".png"
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        printMetrics(name, result, groups)
        printStdDevMetrics(name, intermediateResults, groups)