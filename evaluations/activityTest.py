from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality
from reputation.algorithm import allAlgorithms
from output.chart import chart
from output.metrics import printMetrics, printStdDevMetrics


if __name__ == '__main__':
    testName = "Activity"
    community = Community()

    # Possible Actions
    postGoodArtefact = community.createPostAction(Quality.GOOD)
    postBadArtefact = community.createPostAction(Quality.BAD)
    voteBadNegative = community.createVoteAction(Quality.BAD, VoteConstraints.BADART)
    voteAnyNegative = community.createVoteAction(Quality.BAD, VoteConstraints.NONE)
    voteGoodPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)
    voteAnyPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.NONE)
    idle = community.createIdleAction()

    # Group low activity
    lowActivityStudent = Student("low",
        [
            (0.028, postGoodArtefact),
            (0.012, postBadArtefact),
            (0.056, voteBadNegative),
            (0.024, voteAnyNegative),
            (0.056, voteGoodPositive),
            (0.024, voteAnyPositive),
            (0.8, idle)
        ])
    community.addStudents(lowActivityStudent, 10)

    # Group medium activity

    medActivityStudent = Student("med",
        [
            (0.07, postGoodArtefact),
            (0.03, postBadArtefact),
            (0.14, voteBadNegative),
            (0.06, voteAnyNegative),
            (0.14, voteGoodPositive),
            (0.06, voteAnyPositive),
            (0.5, idle)
        ])
    community.addStudents(medActivityStudent, 10)

    # Group high activity
    highActivityStudent = Student("high",
        [
            (0.14, postGoodArtefact),
            (0.06, postBadArtefact),
            (0.28, voteBadNegative),
            (0.12, voteAnyNegative),
            (0.28, voteGoodPositive),
            (0.12, voteAnyPositive),
        ])
    community.addStudents(highActivityStudent, 10)

    # Run
    groups = ('low', 'med', 'high')
    colors = {'low': 'r', 'med': 'yellow', 'high': 'g'}
    results = community.run(allAlgorithms(), 100, 100)
    for (name, result, intermediateResults) in results:
        c = chart(result, groups, colors, testName + " - " + name)
        path = testName + "-" + name +".png"
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        printMetrics(name, result, groups)
        printStdDevMetrics(name, intermediateResults, groups)
