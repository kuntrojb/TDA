#!/usr/bin/env python3

"""
Este programa se encarga de asociar donantes con pacientes de la mejor forma
posible
"""

import argparse
import csv


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


def read_preferences(filename):
    """
    Reads a file with preferences for a Subject
    The format expected is as follows:
    [subject index], [subjects on the other group ordered by preference]

    Yields a subject index and a list of preferences
    """
    with open(filename) as f:
        for row in csv.reader(f):
            # we need to substract 1 so the indexes start at 0
            subject = int(row[0]) - 1
            preferences = [i - 1 for i in map(int, row[1:])]
            yield subject, preferences


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('pacientes', type=int, help='Cantidad de pacientes')
    parser.add_argument('donantes', type=int, help='Cantidad de donantes')
    parser.add_argument('solicitante', help='Solicitante puede ser "p" o "d"')

    # TODO: agregar mensajes de ayuda apropiados y chequear valores pertinentes
    args = parser.parse_args()

    donors = [Subject(i, label='donor') for i in range(args.donantes)]
    patients = [Subject(i, label='patient') for i in range(args.pacientes)]

    for patient_index, preferences in read_preferences('compatibilidad.txt'):
        patients[patient_index].partners_by_preference = preferences

    for donor_index, preferences in read_preferences('factibilidad.txt'):
        donors[donor_index].partners_by_preference = preferences

    if args.solicitante == 'p':
        applicants, respondents = patients, donors
    else:
        applicants, respondents = donors, patients

    for r in respondents:
        r.build_preferences_by_partner()

    gale_shapley(applicants, respondents)

    matches = []
    for patient in patients:
        if patient.matched_with is not None:
            donor = patient.matched_with
            matches.append(','.join(map(str, (patient, donor))))

    with open('resultados.txt', 'w') as f:
        for match in matches:
            f.write(match + '\n')
