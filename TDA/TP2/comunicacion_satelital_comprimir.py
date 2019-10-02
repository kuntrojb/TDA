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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('frecuencias', type=str, help='Archivo de frecuencias')
    parser.add_argument('mensaje', type=str, help='Archivo a codificar')
    parser.add_argument('generado', help='Archivo generado')

    args = parser.parse_args()

    with open(args.frecuencias, 'r') as f:
        freq_list = [*map(int, f.read().strip().split(','))]
    freqs = {}
    for i, f in enumerate(freq_list):
        freqs[chr(i)] = f

    with open(args.mensaje, 'r') as f:
        message = f.read()

    character_list = []
    for character in message:
        character_list.append(Character(label=character,
                                        weight=freqs[character],
                                        elemental=True))

    huffman_tree = Character.build_tree(character_list)
    coded = bitarray()
    for character in message:
        coded.extend(huffman_tree.code(character))

    with open(args.generado, 'wb') as f:
        coded_binary_data = coded.to_bytes()
        f.write(coded_binary_data)
