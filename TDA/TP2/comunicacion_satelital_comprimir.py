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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('frecuencias', type=int, help='Archivo de frecuencias')
    parser.add_argument('mensaje', type=int, help='Archivo a codificar')
    parser.add_argument('generado', help='Archivo generado')

    args = parser.parse_args()
