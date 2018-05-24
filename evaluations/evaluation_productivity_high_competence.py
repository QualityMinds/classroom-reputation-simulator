from centrality.eigentrust import EigenTrust
from centrality.indegree import InDegree
from centrality.indegree_positive import InDegreePositive
from centrality.pagerank import PageRank
from evaluations.community.online_discussion_group import OnlineDiscussionGroup
from output.chart import chart
from output.metrics import print_metrics, print_stddev_metrics
from simulation.member import Member

if __name__ == '__main__':
    """
    The more basic tests are concluded with the Productivity Test, which investigates
    what kind of effect different levels of productivity, all other parameters being equal,
    have on the reputation score.
    """

    test_name = "Productivity-high"
    community = OnlineDiscussionGroup()

    ALL_CENTRALITY_SCORES = [
        PageRank(),
        EigenTrust(),
        InDegree(),
        InDegreePositive()
    ]

    # Possible Actions
    actions = community.action_profile

    # Group low
    low_student = Member("low", [
            (0.19, actions.post_good_comment),
            (0.01, actions.post_bad_comment),
            (0.38, actions.vote_bad_comment_negative),
            (0.02, actions.vote_any_comment_negative),
            (0.38, actions.vote_good_comment_positive),
            (0.02, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(low_student, 10)

    # Group average
    avg_student = Member("avg", [
            (0.475, actions.post_good_comment),
            (0.025, actions.post_bad_comment),
            (0.2375, actions.vote_bad_comment_negative),
            (0.0125, actions.vote_any_comment_negative),
            (0.2375, actions.vote_good_comment_positive),
            (0.0125, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(avg_student, 10)

    # Group high
    high_student = Member("high", [
            (0.76, actions.post_good_comment),
            (0.04, actions.post_bad_comment),
            (0.095, actions.vote_bad_comment_negative),
            (0.005, actions.vote_any_comment_negative),
            (0.095, actions.vote_good_comment_positive),
            (0.005, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(high_student, 10)

    # Run
    groups = ('low', 'avg', 'high')
    colors = {'low': 'r', 'avg': 'yellow', 'high': 'g'}
    results = community.simulate(ALL_CENTRALITY_SCORES, 100, 100)
    for (name, result, intermediate_results) in results:
        c = chart(result, groups, colors, test_name + " - " + name)
        path = '{}-{}.png'.format(test_name, name)
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        print_metrics(name, result, groups)
        print_stddev_metrics(name, intermediate_results, groups)