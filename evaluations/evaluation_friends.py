from centrality.eigentrust import EigenTrust
from centrality.indegree import InDegree
from centrality.indegree_positive import InDegreePositive
from centrality.pagerank import PageRank
from evaluations.community.online_discussion_group import OnlineDiscussionGroup
from output.chart import chart
from output.metrics import print_metrics, print_stddev_metrics
from simulation.community import ActionProfile
from simulation.member import Member

if __name__ == '__main__':
    """
    In this test, it is evaluated how many friends who are significantly less competent
    than their peers are required to trick the system so that they reach top position
    in the reputation ranking.
    """

    test_name = "Friends"
    community = OnlineDiscussionGroup()

    ALL_CENTRALITY_SCORES = [
        PageRank(),
        EigenTrust(),
        InDegree(),
        InDegreePositive()
    ]

    # Possible Actions
    actions: ActionProfile = community.action_profile

    # Group unaffiliated
    num_unaffiliated = 25

    unaffiliated = Member("unaffiliated", [
            (0.27, actions.post_good_comment),
            (0.03, actions.post_bad_comment),
            (0.32, actions.vote_bad_comment_negative),
            (0.03, actions.vote_any_comment_negative),
            (0.32, actions.vote_good_comment_positive),
            (0.03, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(unaffiliated, num_unaffiliated)

    # Group friends
    friends = Member("f", [
            (0.06, actions.post_good_comment),
            (0.24, actions.post_bad_comment),
            (0.7, actions.vote_good_comment_by_friend_positive),
        ])

    friends.set_friends([num_unaffiliated, num_unaffiliated + 1])
    community.create_members_by_prototype(friends, 2)

    # Run
    groups = ('f', 'unaffiliated')
    colors = {'f': 'c', 'unaffiliated': 'b'}
    results = community.simulate(ALL_CENTRALITY_SCORES, 100, 100)
    for (name, result, intermediate_results) in results:
        c = chart(result, groups, colors, test_name + " - " + name)
        path = '{}-{}.png'.format(test_name, name)
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        print_metrics(name, result, groups)
        print_stddev_metrics(name, intermediate_results, groups)