#!/usr/bin/env python3

# Este programa genera frecuencias falsas para realizar pruebas
# Estas frecuencias estan distribuidas de forma normal logarítmica
# Representando así caracteres significativamente más frecuentes que otros
import numpy as np
import random

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('scale', type=float, default=10, help='Scale factor')
args = parser.parse_args()

printable_start_index, printable_stop_index = 32, 126
printable_count = printable_stop_index - printable_start_index + 1

freqs = sorted(map(int, np.random.lognormal(mean=0.0, sigma=1.5, size=256)*args.scale),
               reverse=True)
printable_freqs = freqs[:printable_count]
non_printable_freqs =  freqs[printable_count + 1:]

random.shuffle(printable_freqs)
random.shuffle(non_printable_freqs)

freqs = non_printable_freqs[:printable_start_index] + \
        printable_freqs + \
        non_printable_freqs[printable_stop_index + 1:]

freqs = map(str, freqs)

with open('frecuencias.txt', 'w') as f:
    f.write(','.join(freqs))
