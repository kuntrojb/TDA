#!/usr/bin/env python3

"""
Este programa comprime un mensaje utilizando el código de Huffman

$./comunicacion_satelital_comprimir.py frecuencias mensaje comprimido
frecuencias: Ruta al archivo de frecuencias
mensaje: Ruta al archivo que se desea comprimir
comprimido: Ruta al archivo comprimido generado
"""

import argparse
import csv
from huffman import Character
from bitarray import bitarray

ASCII_SIZE = 256

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('frecuencias', type=str, help='Archivo de frecuencias')
    parser.add_argument('mensaje', type=str, help='Archivo a codificar')
    parser.add_argument('generado', help='Archivo generado')

    args = parser.parse_args()

    # Build the huffman tree
    with open(args.frecuencias, 'r') as f:
        freq_list = [*map(int, f.read().strip().split(','))]

    freqs = {}
    for i, f in enumerate(freq_list):
        freqs[i] = f

    character_list = []
    for character, freq in freqs.items():
        character_list.append(Character(label=character,
                                        weight=freq,
                                        elemental=True))

    huffman_tree = Character.build_tree(character_list)

    # Read the message to compress
    with open(args.mensaje, 'rb') as f:
        message = f.read()

    # Compress the message
    coded = bitarray()
    for character in message:
        coded.extend(huffman_tree.code(character))

    with open(args.generado, 'wb') as f:
        coded_binary_data = coded.to_bytes()
        f.write(coded_binary_data)
