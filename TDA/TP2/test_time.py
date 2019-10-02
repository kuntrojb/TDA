#!/usr/bin/env python3

import time
import subprocess
import os

length = [1, 10, 100, 300, 500]

data = []

for n in length:

    print(n)
    subprocess.run(['python', 'generar_frecuencias.py', str(n)])
    subprocess.run(['python', 'generar_mensaje.py'])
    print('Se creo el mensaje')

    start = time.time()
    subprocess.run(['pypy3', 'comunicacion_satelital_comprimir.py', 'frecuencias.txt', 'mensaje.txt', 'generado.dat'])
    end = time.time()
    elapsed_comprimir = end - start

    print('Se comprimió')

    start = time.time()
    subprocess.run(['pypy3', 'comunicacion_satelital_descomprimir.py', 'frecuencias.txt', 'generado.dat', 'descomprimido.txt'])
    end = time.time()
    elapsed_descomprimir = end - start

    print('Se descomprimió')

    size = os.path.getsize('mensaje.txt')
    with open('generado.dat', 'rb') as f:
        bit_size = int.from_bytes(f.read(4), byteorder='big')

    data.append((n, size, bit_size//8, elapsed_comprimir, elapsed_descomprimir))
    print(data[-1])

for line in data:
    print(*line)

