#!/usr/bin/env python3

"""
Este programa se encarga de asociar donantes con pacientes de la mejor forma
posible
"""

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('pacientes', help='Cantidad de pacientes')
    parser.add_argument('donantes', help='Cantidad de donantes')
    parser.add_argument('solicitante', help='Solicitante puede ser "p" o "d"')

    # TODO: agregar mensajes de ayuda apropiados y chequear valores pertinentes

    args = parser.parse_args()
