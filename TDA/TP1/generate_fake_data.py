#!/usr/bin/env python3

import numpy as np
import random
import time

from galeshapley import Subject, gale_shapley

ns = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

data = []


for n in ns:

    donors_list = []
    patients_list = []

    print('Creating files of length', n)

    for i in range(n):
        preferences = random.sample(range(n), n)
        row = [i, preferences]
        patients_list.append(row)

    for i in range(n):
        preferences = random.sample(range(n), n)
        row = [i, preferences]
        donors_list.append(row)

    print('Finished creating files')
    print('Running algorithm')
    start = time.time()

    donors = [Subject(i, label='donor') for i in range(n)]
    patients = [Subject(i, label='patient') for i in range(n)]

    for patient_index, preferences in patients_list:
        patients[patient_index].partners_by_preference = preferences

    for donor_index, preferences in donors_list:
        donors[donor_index].partners_by_preference = preferences

    applicants, respondents = patients, donors

    for r in respondents:
        r.build_preferences_by_partner()

    gale_shapley(applicants, respondents)

    matches = []
    for patient in patients:
        if patient.matched_with is not None:
            donor = patient.matched_with
            matches.append(','.join(map(str, (patient, donor))))

    end = time.time()
    elapsed = end - start
    data.append((n, elapsed))
    print('Finished running algorithm')

for line in data:
    print(*line)
