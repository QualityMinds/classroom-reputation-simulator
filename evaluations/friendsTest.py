from simulation.community import Community, VoteConstraints
from simulation.student import Student
from simulation.artifact import Quality
from reputation.algorithm import allAlgorithms
from output.chart import chart
from output.metrics import printMetrics, printStdDevMetrics

if __name__ == '__main__':
    testName = "Friends"
    community = Community()

    # Possible Actions
    postGoodArtefact = community.createPostAction(Quality.GOOD)
    postBadArtefact = community.createPostAction(Quality.BAD)
    voteBadNegative = community.createVoteAction(Quality.BAD, VoteConstraints.BADART)
    voteAnyNegative = community.createVoteAction(Quality.BAD, VoteConstraints.NONE)
    voteGoodPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.GOODART)
    voteAnyPositive = community.createVoteAction(Quality.GOOD, VoteConstraints.NONE)
    voteFriend = community.createVoteAction(Quality.GOOD, VoteConstraints.FRIEND)

    # Group unaffiliated
    unaff_num = 25;

    unaffiliated = Student("unaffiliated",
        [
            (0.27, postGoodArtefact),
            (0.03, postBadArtefact),
            (0.32, voteBadNegative),
            (0.03, voteAnyNegative),
            (0.32, voteGoodPositive),
            (0.03, voteAnyPositive),
        ])
    community.addStudents(unaffiliated, unaff_num)

    # Group friends
    friends = Student("f",
        [
            (0.06, postGoodArtefact),
            (0.24, postBadArtefact),
            (0.7, voteFriend),
        ])

    friends.addFriends([unaff_num, unaff_num+1]);

    community.addStudents(friends, 2)


    # Run
    groups = ('f', 'unaffiliated')
    colors = {'f': 'c', 'unaffiliated': 'b'}
    results = community.run(allAlgorithms(), 100, 100)
    for (name, result, intermediateResults) in results:
        c = chart(result, groups, colors, testName + " - " + name)
        path = testName + "-" + name +".png"
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        printMetrics(name, result, groups)
        printStdDevMetrics(name, intermediateResults, groups)