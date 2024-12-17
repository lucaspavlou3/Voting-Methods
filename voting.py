class Preference:
    def __init__(
        self, candidates: list[int], voters: list[int], prefs: dict[int, list[int]]
    ) -> None:
        self._candidates = candidates
        self._voters = voters
        self._prefs = prefs

    def candidates(self) -> list[int]:
        return self._candidates

    def voters(self) -> list[int]:
        return self._voters

    def get_preference(self, candidate: int, voter: int) -> int:
        return self._prefs[voter].index(candidate)


v_dict = {
    1: [2, 1, 3, 5, 6, 4],
    2: [1, 2, 3, 6, 5, 4],
    3: [1, 2, 3, 4, 5, 6],
    4: [6, 5, 4, 3, 2, 1],
    5: [2, 1, 3, 4, 6, 5],
    6: [5, 6, 3, 4, 1, 2]
}

pref_obj = Preference([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], v_dict)


def tie_breaker_winner(scoring_dict: dict[int:int], tie_break: int, preferences):
    """Input a scoring dictionary, a tie-breaking agent and a preference object.
    Resolve any ties using the tie-breaking agent's first choice."""
    ties = []  # all candidates who have the highest score

    # iterate through every candidate who has the equivalent highest score (from scoring_dict{})
    # any candidate with the min value (i.e. most preferred) gets added to the ties list
    for candidate in scoring_dict.keys():
        if scoring_dict.get(candidate) == max(scoring_dict.values()):
            ties.append(candidate)

    # if ties list only contains one candidate, this must be the winner
    if len(ties) == 1:
        return ties[0]
    # if there exists > 1 candidate in ties, order them in terms of tie breaker's preference, then select tie breaker's 1st choice
    else:
        return sorted(ties, key=lambda c: preferences.get_preference(c, tie_break))[0]


def dictatorship(preferences, agent: int) -> int:
    """Input a preference object and a tie-breaking voter.
    The winning candidate is always the voter's first choice."""
    # check if the given voter is in the given voters list
    # if not, raise an error
    if agent not in preferences.voters():
        raise ValueError("Voter not found.")

    # iterate through every given candidate and return the agent that the dictator has picked first
    for candidate in preferences.candidates():
        if preferences.get_preference(candidate, agent) == 0:
            return candidate


def scoring_rule(preferences, score_vector: list[int], tie_break: int) -> int:
    """Input a preference object, a list of scores and a tie-breaking voter.
    The winner is the candidate with the highest cumulative score."""
    candidate_score_dict = {i: 0 for i in preferences.candidates()}
    score_vector = sorted(score_vector, reverse=True)

    # if the number of candidates is not the same as the number of scores in the score vector, raise an error
    if len(score_vector) != len(preferences.candidates()):
        raise ValueError("The number of candidates requested is invalid.")

    # for every voter, assign each candidate the value of the preference that that voter chose for them
    for voter in preferences.voters():
        for candidate in preferences.candidates():
            candidate_score_dict[candidate] += score_vector[preferences.get_preference(candidate, voter)]

    return tie_breaker_winner(candidate_score_dict, tie_break, preferences)


def plurality(preferences, tie_break: int) -> int:
    """Input a preference object and a tie-breaking voter.
    The winner is the candidate who is most voters' first choice."""
    times_selected = {i: 0 for i in preferences.candidates()}  # how many times is a candidate picked first?

    # check if the given candidate is the preferred choice for each voter (value == 0)
    # if picked first, increase the times_selected count for that candidate by 1
    for voter in preferences.voters():
        for candidate in preferences.candidates():
            if preferences.get_preference(candidate, voter) == 0:
                times_selected[candidate] += 1

    return tie_breaker_winner(times_selected, tie_break, preferences)


def veto(preferences, tie_break: int) -> int:
    """Input a preference object and a tie-breaking voter.
    The winner is the candidate who is fewest voters' last choice."""
    candidate_points = {i: 0 for i in preferences.candidates()}

    # check if the candidate was voted last by each voter
    # if they were not voted last, increase their score by 1
    for voter in preferences.voters():
        for candidate in preferences.candidates():
            if (preferences.get_preference(candidate, voter) != len(preferences.candidates()) - 1):
                candidate_points[candidate] += 1

    return tie_breaker_winner(candidate_points, tie_break, preferences)


def borda(preferences, tie_break: int) -> int:
    """Input a preference object and a tie-breaking voter.
    The first choice of each candidate gets the highest score, etc. and the winner is the candidate with the highest score."""
    candidate_points = {i: 0 for i in preferences.candidates()}
    n = 0

    # iterate through every candidate and give them a larger score if they were preferred, and smaller if they were not
    while n <= len(candidate_points):
        for voter in preferences.voters():
            for candidate in preferences.candidates():
                candidate_points[candidate] += (len(candidate_points) - preferences.get_preference(candidate, voter)) - 1
                n += 1

    return tie_breaker_winner(candidate_points, tie_break, preferences)


def STV(preferences, tie_break: int) -> int:
    """Input a preference object and a tie-breaking voter.
    Each round, the candidate(s) who are voted the fewest times are eliminated. The last candidate standing is the winner."""
    candidates = []
    candidate_first = {i: 0 for i in preferences.candidates()}

    # makes a list containing all of the candidates so we can check its length
    for candidate in preferences.candidates():
        candidates.append(candidate)

    candidates_remaining = candidates.copy()  # which candidates make it through to the next round?

    while len(candidates_remaining) > 1:
        candidate_first = {i: 0 for i in candidates_remaining}
        # check every candidate to see if they have been voted first by any voter
        # if they have been, increase their value in candidate_first{} by 1
        for voter in preferences.voters():
            surviving_candidates = sorted(
                candidates_remaining,
                key=lambda candidate: preferences.get_preference(candidate, voter)
            )
            candidate_first[surviving_candidates[0]] += 1

        for candidate in candidate_first:
            # search the candidate_first dict for the candidate(s) with the lowest score and remove them
            # as long as that score is not also the minimum score (i.e. the last two candidates, who have the same score)
            if not min(candidate_first.values()) == max(candidate_first.values()):
                if candidate_first[candidate] == min(candidate_first.values()):
                    candidates_remaining.remove(candidate)
            # tie break - put the tying candidates in order of preference according to the tie-breaking agent
            # pick the first candidate in the list (the most preferred)
            else:
                candidates_remaining = [
                    sorted(
                        candidate_first,
                        key=lambda candidate: preferences.get_preference(
                            candidate, tie_break
                        ),
                    )[0]
                ]
    return candidates_remaining[0]


# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------

# print(tie_breaker_winner({1: 10, 2: 10}, 2, pref_obj))

# print("for dictator no.", 4, "the winning candidate is", dictatorship(pref_obj, 4))
# print("for dictator no.", 7, "the winning candidate is", dictatorship(pref_obj, 7))

# print(scoring_rule(pref_obj, [0,1,2,3,4,5], 2))

# print(plurality(pref_obj))

# print(borda(pref_obj))

# print(STV(pref_obj, 6))
