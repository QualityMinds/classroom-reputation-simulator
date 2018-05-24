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
    The collusion test investigates the impact of agents that vote other
    peers negatively without contributing themselves, so that they gain a better reputation
    score relative to their peers. 
    """

    test_name = "Collusion"
    community = OnlineDiscussionGroup()

    ALL_CENTRALITY_SCORES = [
        PageRank(),
        EigenTrust(),
        InDegree(),
        InDegreePositive()
    ]

    # Possible Actions
    actions = community.action_profile

    # Group normal
    normal = Member("normal", [
            (0.24, actions.post_good_comment),
            (0.06, actions.post_bad_comment),
            (0.28, actions.vote_bad_comment_negative),
            (0.07, actions.vote_any_comment_negative),
            (0.28, actions.vote_good_comment_positive),
            (0.07, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(normal, 15)

    # Group mal
    mal = Member("mal", [(1, actions.vote_any_comment_negative)])
    community.create_members_by_prototype(mal, 15)

    # Run
    groups = ('mal', 'normal')
    colors = {'mal': 'r', 'normal': 'c'}
    results = community.simulate(ALL_CENTRALITY_SCORES, 100, 100)
    for (name, result, intermediate_results) in results:
        c = chart(result, groups, colors, test_name + " - " + name)
        path = '{}-{}.png'.format(test_name, name)
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        print_metrics(name, result, groups)
        print_stddev_metrics(name, intermediate_results, groups)