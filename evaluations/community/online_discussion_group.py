import secrets
from enum import Enum

from simulation.action_profile import ActionProfile
from simulation.artifact import Quality, Artifact
from simulation.community import Community
from simulation.votematrix import VoteMatrix


class VoteConstraints(Enum):
    NONE = 0
    GOOD_ART = 1
    BAD_ART = 2
    FRIEND = 3


class OnlineDiscussionGroup(Community):

    def __init__(self):
        super().__init__()
        self.artifacts = []

    def reset_run(self):
        self.action_profile = self.setup_action_profile()
        self.artifacts = list()
        self.votes = VoteMatrix(len(self.members))

    def setup_action_profile(self):
        action_profile = ActionProfile()
        action_profile.add('post_good_comment', self.create_post_action(Quality.GOOD))
        action_profile.add('post_bad_comment', self.create_post_action(Quality.BAD))
        action_profile.add('vote_bad_comment_negative', self.create_vote_action(Quality.BAD, VoteConstraints.BAD_ART))
        action_profile.add('vote_any_comment_negative', self.create_vote_action(Quality.BAD, VoteConstraints.NONE))
        action_profile.add('vote_good_comment_positive', self.create_vote_action(Quality.GOOD, VoteConstraints.GOOD_ART))
        action_profile.add('vote_any_comment_positive', self.create_vote_action(Quality.GOOD, VoteConstraints.NONE))
        action_profile.add('vote_good_comment_by_friend_positive', self.create_vote_action(Quality.GOOD, VoteConstraints.FRIEND))
        action_profile.add('stay_idle', lambda x: None)
        return action_profile

    def add_artifact(self, artifact):
        self.artifacts.append(artifact)

    def add_vote(self, voter: int, comment: Artifact, quality: Quality):
        if quality == quality.BAD:
            self.votes.negative[voter, comment.creator] += 1
        else:
            self.votes.positive[voter, comment.creator] += 1

    def get_artifacts_for_voting(self, my_id):
        candidates = [a for a in self.artifacts if not a.creator == my_id and not a.has_voted(my_id)]
        return candidates

    def get_artifacts_for_voting_by_quality(self, my_id, quality):
        candidates = [a for a in self.get_artifacts_for_voting(my_id) if a.quality == quality]
        return candidates

    def get_artifacts_for_voting_by_member_ids(self, my_id, other_ids):
        candidates = self.get_artifacts_for_voting(my_id)
        return [a for a in candidates if a.creator in other_ids]

    def create_post_action(self, quality:Quality):
        return lambda x: self.add_artifact(Artifact(x.member_id, quality))

    def create_vote_action(self, quality: Quality, constraint: VoteConstraints):
        vote_actions = {
            VoteConstraints.NONE: self.vote_any,
            VoteConstraints.GOOD_ART: self.vote_good_artifact,
            VoteConstraints.BAD_ART: self.vote_bad_artifact,
            VoteConstraints.FRIEND: self.vote_friend
        }
        return lambda x: vote_actions.get(constraint)(x, quality)

    def vote(self, voter_id, quality, artifacts):
        if len(artifacts) > 0:
            self.add_vote(voter_id, secrets.choice(artifacts), quality)

    def vote_any(self, student, quality):
        self.vote(student.member_id,
                  quality,
                  self.get_artifacts_for_voting(student.member_id))

    def vote_good_artifact(self, student, quality):
        self.vote(student.member_id,
                  quality,
                  self.get_artifacts_for_voting_by_quality(student.member_id, Quality.GOOD))

    def vote_bad_artifact(self, student, quality):
        self.vote(student.member_id,
                  quality,
                  self.get_artifacts_for_voting_by_quality(student.member_id, Quality.BAD))

    def vote_friend(self, student, quality):
        self.vote(student.member_id,
                  quality,
                  self.get_artifacts_for_voting_by_member_ids(student.member_id, student.friends))
