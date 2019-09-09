#!/usr/bin/env python3

import numpy as np
import csv
import random
import os
import time

ns = [*map(int, np.logspace(1, 4, num=10))]

data = []

for n in ns:
    print('Creating files of length', n)

    with open('compatibilidad.txt', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(n):
            preferences = [*range(1, n + 1)]
            random.shuffle(preferences)
            row = [i + 1, *preferences]
            writer.writerow(row)

    with open('factibilidad.txt', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(n):
            preferences = [*range(1, n + 1)]
            random.shuffle(preferences)
            row = [i + 1, *preferences]
            writer.writerow(row)

    print('Finished creating files')
    print('Running algorithm')
    start = time.time()
    os.system('./donantes.py ' + str(n) + ' ' + str(n) + ' p')
    end = time.time()
    elapsed = end - start
    data.append((n, elapsed))
    print('Finished running algorithm')

for line in data:
    print(*line)
