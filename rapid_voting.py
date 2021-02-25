VOTE_DATA_FILE = "votes_data.txt"


class RapidVoting(object):
    """Class for finding result of election."""

    def __init__(self, file_name):
        """Initialize."""
        with open(VOTE_DATA_FILE, 'r') as vote_file:
            vote_data = vote_file.read().splitlines()

        # Set num of candidates
        self.num_candidate = int(vote_data[0])

        # Create a list of all votes by user
        self.all_votes = []
        for individual_vote in vote_data[1:]:
            vote = [int(x) for x in individual_vote.split(",")]
            self.all_votes.append(vote)

        # Set total number of votes
        self.num_votes = len(self.all_votes)
        # Flag to check if majority is established or not
        self.is_majority_established = False
        # Store votes according to the perferred candidate
        self.candidate_wise_ballot = None
        # Store majority_candidate and discarded candidates
        self.majority_candidate = None
        self.discarded_candidates = []

    def create_candidate_wise_ballot(self):
        """Create camdidate's priority wise grouped ballot."""
        # Intialize empty map with candidates as key
        candidate_vote_map = {}
        for candidate in range(1, self.num_candidate+1):
            candidate_vote_map[candidate] = []
        # Categorize votes according to preffered candidate
        for vote_idx in range(self.num_votes):
            preferred_candidate = self.all_votes[vote_idx][0]
            candidate_vote_map[preferred_candidate].append(vote_idx)

        return candidate_vote_map

    def check_candidate_majority(self):
        """Check if any candidate established a majority."""
        for candidate, candidate_vote_list in self.candidate_wise_ballot.items():
            if len(candidate_vote_list) > (self.num_votes/2.0):
                return True, candidate
        return False, None

    def get_candidate_votes(self):
        """Returns the count of individual candidates in a list."""
        votes_count = []
        for candidate, candidate_vote_list in self.candidate_wise_ballot.items():
            if candidate not in self.discarded_candidates:
                votes_count.append(len(candidate_vote_list))
        return votes_count

    def get_candidates_by_vote(self, vote):
        """Returns candidate whose vote count is equal to the vote parameter."""
        to_be_discarded = []
        for candidate, candidate_vote_list in self.candidate_wise_ballot.items():
            if candidate not in self.discarded_candidates and len(candidate_vote_list) == vote:
                to_be_discarded.append(candidate)

        return to_be_discarded

    def discard_candidate(self, round_number, candidate, candidates_to_discard):
        """Discard candidate passed from further condieration as winner."""
        candidate_vote_list = self.candidate_wise_ballot[candidate]
        unable_to_distribute = []
        while candidate_vote_list:
            voter_idx = candidate_vote_list.pop()
            next_candidate = self.all_votes[voter_idx][round_number+1]
            if next_candidate not in set(
                    candidates_to_discard + self.discarded_candidates):
                self.candidate_wise_ballot[next_candidate].append(
                    voter_idx)
            else:
                unable_to_distribute.append(voter_idx)
        candidate_vote_list.extend(unable_to_distribute)

    def candidate_can_get_eliminated(self):
        """Return true/false if any candidate can get eliminated."""
        votes_count = self.get_candidate_votes()
        min_candidate_vote, max_candidate_vote = min(
            votes_count), max(votes_count)
        # If maximum votes collected and minimun votes collected are different.
        if min_candidate_vote != max_candidate_vote:
            return True, min_candidate_vote
        # If all the candidates are equally preferred, return False
        return False, max_candidate_vote

    def check_majority_in_tie(self, tie_map, round_number):
        """
        Check if their is a majority using further preference in case of a tie.
        Returns true/flase with the count used to determine.
        """
        if min(tie_map.values()) == max(tie_map.values()):
            return False, None
        for candidate, count in tie_map.items():
            if count > (self.num_votes/2.0):
                return True, candidate
        return False, None

    def resolve_tie(self, round_number, votes):
        """Resolve tie among preferred candidates."""
        # fetch all the candidates still in race.
        non_eliminated_candidates = self.candidate_wise_ballot.keys() - \
            self.discarded_candidates
        # Create a temporary map to store lower preferences
        tie_count_map = {}

        # Intialize with the length of intial votes in favour
        for candidate in non_eliminated_candidates:
            tie_count_map[candidate] = len(
                self.candidate_wise_ballot[candidate])

        for i in range(1, self.num_candidate):
            for candidate_ballot, candidate_vote_list in self.candidate_wise_ballot.items():
                for preferred_candidate in non_eliminated_candidates:
                    # Check to ensure that candidate's own ballot is not consiered
                    if preferred_candidate != candidate_ballot:
                        # iterate over all the votes index
                        for user_vote_card_idx in candidate_vote_list:
                            # Fetch user's vote
                            user_vote_card = self.all_votes[user_vote_card_idx]

                            # If th next preference of user is in the preferred candidates,
                            # Increase it's counter by 1s
                            if user_vote_card[i] == preferred_candidate:
                                tie_count_map[preferred_candidate] += 1

            # print(tie_count_map)

            # Check if majority is acheieved by any candidate after
            # considering the lower preference votes.
            majority_reached, maj_candidate = self.check_majority_in_tie(
                tie_count_map, round_number)
            round_number += 1

            if majority_reached:
                self.is_tie_resolved = True
                self.is_majority_established = True
                self.majority_candidate = maj_candidate
                break

    def run(self):
        """Main function to run vote counting using RVP."""
        # Set preferred candidate wise ballot
        self.candidate_wise_ballot = self.create_candidate_wise_ballot()

        # Set the counter for counting round number.
        round_number = 0

        # Iterate till a majority is established or no winner is found.
        while not self.is_majority_established:
            # Check if a majority is establhised.
            self.is_majority_established, self.majority_candidate = self.check_candidate_majority()

            # If no majority, check if any candidate can be eliminated or it's a tie
            if not self.is_majority_established:
                can_eliminate, vote_count = self.candidate_can_get_eliminated()
                if can_eliminate:
                    print("Eliminating least preferred candidate")
                    # Get the candidates to be discaded
                    candidates_to_discard = self.get_candidates_by_vote(
                        vote_count)
                    for candidate in candidates_to_discard:
                        self.discard_candidate(
                            round_number, candidate, candidates_to_discard)
                        self.discarded_candidates.append(candidate)
                else:
                    print("There is tie. Resolving...")
                    self.resolve_tie(round_number, vote_count)
                    break

                # Increment round number
                round_number += 1

        if self.majority_candidate:
            print("Winner is candidate #", self.majority_candidate)
        else:
            print("No Winner found")


RapidVoting(VOTE_DATA_FILE).run()
