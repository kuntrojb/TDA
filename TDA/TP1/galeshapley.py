class Subject:
    def __init__(self, index, label=''):
        self.label = label
        self.index = index
        self.matched_with = None
        self.partners_by_preference = None
        self.preferences_by_partner = None

    def get_preferred(self):
        return self.partners_by_preference.pop(0)

    def build_preferences_by_partner(self):
        self.preferences_by_partner = list(self.partners_by_preference)
        for i, partner in enumerate(self.partners_by_preference):
            self.preferences_by_partner[partner] = i

    def preference(self, other):
        return self.preferences_by_partner[other.index]

    def __str__(self):
        return str(self.index + 1)


def rematch(applicant, respondent):
    """
    Produces a match between applicant and respondent  if possible.
    If a match is broken and another applicant is rejected, it returns that
    applicant.

    It has side effects on applicant and respondent.
    """
    a, r = applicant, respondent
    if r.matched_with is None:
        r.matched_with = applicant
        a.matched_with = respondent
        return
    if r.preference(a) < r.preference(r.matched_with):
        rejected = r.matched_with
        r.matched_with = a
        a.matched_with = r
        return rejected
    return None


def gale_shapley(applicants, respondents):
    """
    Applies the gale shapley algorithm between applicants and respondents.
    """

    # Since we don't want to change the list that was given to us
    applicants = list(applicants)

    while len(applicants) != 0:
        current_applicant = applicants.pop()

        while current_applicant.matched_with is None:
            current_respondent = respondents[current_applicant.get_preferred()]
            rejected = rematch(current_applicant, current_respondent)

            # if someone was rejected in the process
            if rejected is not None:
                applicants.append(rejected)
