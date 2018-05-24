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
    In this test it is investigated whether equally competent and productive students 
    are ranked higher when they contribute more actively, i.e. vote and post more than their 
    less active peers. It is expected that more avid contributors 
    """
    test_name = "Activity"
    community: OnlineDiscussionGroup = OnlineDiscussionGroup()

    ALL_CENTRALITY_SCORES = [
        PageRank(),
        EigenTrust(),
        InDegree(),
        InDegreePositive()
    ]

    # Possible Actions
    actions: ActionProfile = community.action_profile

    # Group low activity
    low_active_student = Member("low", [
            (0.028, actions.post_good_comment),
            (0.012, actions.post_bad_comment),
            (0.056, actions.vote_bad_comment_negative),
            (0.024, actions.vote_any_comment_negative),
            (0.056, actions.vote_good_comment_positive),
            (0.024, actions.vote_any_comment_positive),
            (0.8, actions.stay_idle)
        ])
    community.create_members_by_prototype(low_active_student, 10)

    # Group medium activity
    medium_active_student = Member("med", [
            (0.07, actions.post_good_comment),
            (0.03, actions.post_bad_comment),
            (0.14, actions.vote_bad_comment_negative),
            (0.06, actions.vote_any_comment_negative),
            (0.14, actions.vote_good_comment_positive),
            (0.06, actions.vote_any_comment_positive),
            (0.5, actions.stay_idle)
        ])
    community.create_members_by_prototype(medium_active_student, 10)

    # Group high activity
    high_active_student = Member("high", [
            (0.14, actions.post_good_comment),
            (0.06, actions.post_bad_comment),
            (0.28, actions.vote_bad_comment_negative),
            (0.12, actions.vote_any_comment_negative),
            (0.28, actions.vote_good_comment_positive),
            (0.12, actions.vote_any_comment_positive),
        ])
    community.create_members_by_prototype(high_active_student, 10)

    # Run
    groups = ('low', 'med', 'high')
    colors = {'low': 'r', 'med': 'yellow', 'high': 'g'}
    results = community.simulate(ALL_CENTRALITY_SCORES, 100, 100)
    for (name, result, intermediate_results) in results:
        c = chart(result, groups, colors, test_name + " - " + name)
        path = '{}-{}.png'.format(test_name, name)
        c.savefig(path, bbox_inches='tight', dpi=400)
        print("Saved " + path)

        print_metrics(name, result, groups)
        print_stddev_metrics(name, intermediate_results, groups)
