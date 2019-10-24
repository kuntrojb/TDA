#!/usr/bin/env python3

"""
Este programa calcula el mínimo rectángulo contenedor a partir de ciertos puntos

$./rectangulo_contenedor.py vértices método
vértices: Ruta al archivo de con los vertices
método: inicial o dyc
"""

import argparse
import csv
from vector import Point
from bounding_box import BoundingBoxDC, BoundingBox

output_filename = 'rectangulo.txt'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('vertices', type=str, help='Archivo de vértices')
    parser.add_argument('metodo', type=str, help='Método a usar')

    args = parser.parse_args()

    # Read the vertex file
    with open(args.vertices, 'r') as f:
        points = []
        for line in f.readlines():
            points.append(Point(*map(float, line.strip().split(','))))

    if args.metodo == 'inicial':
        box = BoundingBox(points)
    elif args.metodo == 'dyc':
        box = BoundingBoxDC(points)
    else:
        raise Exception('Método desconocido, los métodos pueden' \
                        'ser "inicial" o "dyc" ')

    with open(output_filename, 'w') as f:
        for point in box:
            f.write(str(point) + '\n')
