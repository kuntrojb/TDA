#!/usr/bin/env python3

"""
Este programa se encarga de asociar donantes con pacientes de la mejor forma
posible

$./donantes.py [cantidad de pacientes] [cantidad de donantes] [pd]
"""

import argparse
import csv
from galeshapley import Subject, gale_shapley


def read_preferences(filename, max_lines=None):
    """
    Reads a file with preferences for a Subject
    The format expected is as follows:
    [subject index], [subjects on the other group ordered by preference]

    Yields a subject index and a list of preferences
    """
    with open(filename) as f:
        for i, row in enumerate(csv.reader(f)):

            # prevents reading more lines than necessary
            if max_lines is not None and max_lines <= i:
                break

            # we need to substract 1 so the indexes start at 0
            subject = int(row[0]) - 1
            preferences = [i - 1 for i in map(int, row[1:])]
            yield subject, preferences


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('pacientes', type=int, help='Cantidad de pacientes')
    parser.add_argument('donantes', type=int, help='Cantidad de donantes')
    parser.add_argument('solicitante', help='Solicitante puede ser "p" o "d"')

    args = parser.parse_args()

    donors = [Subject(i, label='donor') for i in range(args.donantes)]
    patients = [Subject(i, label='patient') for i in range(args.pacientes)]

    for patient_index, preferences in read_preferences('compatibilidad.txt',
                                                       max_lines=args.pacientes):
        preferences = [*filter(lambda x: x < args.donantes, preferences)]
        patients[patient_index].partners_by_preference = preferences

    for donor_index, preferences in read_preferences('factibilidad.txt',
                                                     max_lines=args.donantes):
        preferences = [*filter(lambda x: x < args.pacientes, preferences)]
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
