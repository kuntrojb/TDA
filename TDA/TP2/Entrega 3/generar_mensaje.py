#!/usr/bin/env python3

# Este programa genera un mensaje falso para realizar pruebas
# La frecuencia con la que aparecen los caracteres del mensaje se obtiene del
# archivo de frecuencias

import random

with open('frecuencias.txt', 'r') as f:
    freqs = [*map(int, f.read().strip().split(','))]

printable_start_index = 32
printable_stop_index = 126

freqs = freqs[printable_start_index:printable_stop_index + 1]

characters = []

for i, times in enumerate(freqs):
    character = [chr(printable_start_index + i)]*times
    characters.extend(character)

random.shuffle(characters)

mensaje = ''.join(characters)

with open('mensaje.txt', 'w') as f:
    f.write(mensaje)
