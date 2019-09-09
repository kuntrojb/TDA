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
        self.preferences = None

    def get_preferred(self):
        return self.preferences.pop(0)

    def __str__(self):
        return self.label + ' ' + str(self.index)


def read_preferences(filename):
    with open(filename) as f:
        for row in csv.reader(f):
            # we need to substract 1 so the indexes start at 0
            subject = int(row[0]) - 1
            preferences = [i - 1 for i in map(int, row[1:])]
            yield subject, preferences


def rematch(applicant, respondent):
    if respondent.matched_with is None:
        respondent.matched_with = applicant.index
        applicant.matched_with = respondent.index
        return
    # logica para destruir parejas
    return


def gale_shapley(applicants, respondents):
    matches = []
    while len(applicants) != 0:
        current_applicant = applicants.pop()
        while current_applicant.matched_with is None:
            respondent_index = current_applicant.get_preferred()
            current_respondent = respondents[respondent_index]
            rematch(current_applicant, respondent)



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
        patients[patient_index].preferences = preferences

    for donor_index, preferences in read_preferences('factibilidad.txt'):
        donors[donor_index].preferences = preferences

    gale_shapley(donors, patients)
