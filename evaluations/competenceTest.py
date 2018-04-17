from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality
from reputation.algorithm import allAlgorithms
from output.chart import chart
from output.metrics import printMetrics, printStdDevMetrics

if __name__ == '__main__':
    testName = "Competence";
    community = Community()

    #Possible Actions
    postGoodArtefact = community.createPostAction(Quality.GOOD)
    postBadArtefact = community.createPostAction(Quality.BAD)
    voteBadNegative = community.createVoteAction(Quality.BAD, VoteConstraints.BADART)
    voteAnyNegative = community.createVoteAction(Quality.BAD, VoteConstraints.NONE)
    voteGoodPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)
    voteAnyPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.NONE)

    # Group low
    lowStudent = Student("low",
        [
            (0.1, postGoodArtefact),
            (0.1, postBadArtefact),
            (0.2, voteBadNegative),
            (0.2, voteAnyNegative),
            (0.2, voteGoodPositive),
            (0.2, voteAnyPositive),
        ])
    community.addStudents(lowStudent, 10)

    # Group average
    avgStudent = Student("avg",
        [
            (0.14, postGoodArtefact),
            (0.06, postBadArtefact),
            (0.28, voteBadNegative),
            (0.12, voteAnyNegative),
            (0.28, voteGoodPositive),
            (0.12, voteAnyPositive),
        ])
    community.addStudents(avgStudent, 10)

    # Group high
    highStudent = Student("high",
        [
            (0.18, postGoodArtefact),
            (0.02, postBadArtefact),
            (0.36, voteBadNegative),
            (0.04, voteAnyNegative),
            (0.36, voteGoodPositive),
            (0.04, voteAnyPositive),
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