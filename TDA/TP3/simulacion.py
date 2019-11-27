#!/usr/bin/env python3

import time
import tkinter as tk
from tkinter import Tk, Canvas, Frame, Button
from collections import namedtuple

WIDTH = 700
HEIGHT = 500
BOX_SIZE = 50

X_MARGIN = 50
Y_MARGIN = 50

deposito = '  ·  ' '\n' \
           ' ··  ' '\n' \
           ' ··  ' '\n' \
           ' ····' '\n' \
           '     ' '\n' \
           '     '

deposito = deposito.split('\n')
deposito = [[True if cell == '·' else False for cell in row] for row in deposito]


class Position:

    STANDING = 0
    HORIZONTAL = 1
    VERTICAL = 2

    def __init__(self, row, col, orientation=STANDING, index=None):
        self.row = row
        self.col = col
        self.orientation = orientation
        self.index = index
        self._neighbors = None
        self.reachable = [self]

    @property
    def neighbors(self):
        if self._neighbors is not None:
            return self._neighbors
        return self._get_neighbors()

    def _get_neighbors(self):
        if self.orientation == Position.STANDING:
            neighbors = [Position(self.row-1, self.col, orientation=Position.VERTICAL),
                         Position(self.row+2, self.col, orientation=Position.VERTICAL),
                         Position(self.row, self.col-2, orientation=Position.HORIZONTAL),
                         Position(self.row, self.col+1, orientation=Position.HORIZONTAL)]
        elif self.orientation == Position.HORIZONTAL:
            neighbors = [Position(self.row-1, self.col, orientation=Position.HORIZONTAL),
                         Position(self.row+1, self.col, orientation=Position.HORIZONTAL),
                         Position(self.row, self.col-1, orientation=Position.STANDING),
                         Position(self.row, self.col+2, orientation=Position.STANDING)]
        elif self.orientation == Position.VERTICAL:
            neighbors = [Position(self.row, self.col-1, orientation=Position.VERTICAL),
                         Position(self.row, self.col+1, orientation=Position.VERTICAL),
                         Position(self.row-2, self.col, orientation=Position.STANDING),
                         Position(self.row+1, self.col, orientation=Position.STANDING)]
        self._neighbors = [neighbor for neighbor in neighbors if neighbor.is_valid()]
        return self._neighbors

    @property
    def cells(self):
        cells = [(self.row, self.col)]
        if self.orientation == Position.HORIZONTAL:
            cells.append((self.row, self.col+1))
        elif self.orientation == Position.VERTICAL:
            cells.append((self.row-1, self.col))
        return cells

    def is_valid(self):
        global deposito, max_cols, max_rows

        if self.row < 0 or self.row >= max_rows:
            return False
        if self.col < 0 or self.col >= max_cols:
            return False
        if not deposito[self.row][self.col]:
            return False
        if self.orientation == Position.HORIZONTAL:
            if self.col+1 >= max_cols or not deposito[self.row][self.col+1]:
                return False
        elif self.orientation == Position.VERTICAL:
            if self.row-1 < 0 or not deposito[self.row-1][self.col]:
                return False
        return True

    @property
    def distance(self):
        global positions_cache
        return positions_cache[self.orientation][self.row][self.col][0]

    @property
    def path(self):
        global positions_cache
        return positions_cache[self.orientation][self.row][self.col][1]

    @path.setter
    def path(self, value):
        global positions_cache
        positions_cache[self.orientation][self.row][self.col] = [len(value), value]

    def __repr__(self):
        string = 'Position('
        string += str(self.row) + ','
        string += str(self.col) + ','
        if self.orientation == Position.STANDING:
            string += 'STANDING' + ')'
        elif self.orientation == Position.HORIZONTAL:
            string += 'HORIZONTAL' + ')'
        elif self.orientation == Position.VERTICAL:
            string += 'VERTICAL' + ')'
        return string


    def __eq__(self, other):
        if self.row == other.row and \
           self.col == other.col and \
           self.orientation == other.orientation:
           return True
        return False

max_rows = len(deposito)
max_cols = len(deposito[0])

INITIAL_STATE = [float('inf'), None]
positions_cache = [[[INITIAL_STATE for col in range(max_cols)]
                     for row in range(max_rows)]
                     for i in range(3)]

# posicion inicial
posicion_inicial = Position(row=3, col=4, orientation=Position.STANDING)
posicion_inicial.path = []
continuar = True
while continuar:
    continuar = False
    for a in posicion_inicial.reachable:
        for neighbor in a.neighbors:
            if a.distance + 1 < neighbor.distance:
                if neighbor.distance == float('inf'):
                    posicion_inicial.reachable.append(neighbor)
                neighbor.path = a.path + [neighbor]
                continuar = True

posicion_destino = Position(row=3, col=2)
indice_actual = 0
posicion_actual = posicion_inicial

def siguiente():
    global indice_actual, posicion_actual
    posicion_actual = posicion_destino.path[indice_actual]
    indice_actual += 1
    indice_actual = indice_actual % len(posicion_destino.path)

def box(canvas, x, y, color='#fAA'):
    x = X_MARGIN + x*BOX_SIZE
    y = Y_MARGIN + y*BOX_SIZE
    p0 = [x, y]
    p1 = [x + BOX_SIZE, y]
    p2 = [x + BOX_SIZE, y + BOX_SIZE]
    p3 = [x, y + BOX_SIZE]
    canvas.create_rectangle(*p0, *p2,
                            outline="#000", fill=color)

    return [*p0, *p2]


class MainWindow(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()

        self.to_clear = []

    def initUI(self):
        self.master.title('Simulación caja')
        self.pack(fill=tk.BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=1)

        self.x = 20

        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill='#fff')
        box(self.canvas, 10, 10)

        self.boton_siguiente = Button(self, text='siguiente', command=siguiente)
        print(self.winfo_width())
        self.boton_siguiente.place(x=500, y=50)


    def clear(self, fast=True):
        if fast:
            for item in self.to_clear:
                self.canvas.create_rectangle(*item,
                                             outline='#fff', fill='#fff')

    def draw(self):
        self.clear()

        for i_row, row in enumerate(deposito):
            for i_col, cell in enumerate(row):
                if cell == True:
                    posicion = Position(row=i_row, col=i_col)
                    c = (i_row, i_col)
                    if posicion == posicion_inicial:
                        cell_image = box(self.canvas,
                                         i_col, i_row,
                                         color='#FAA')
                    elif c in posicion_actual.cells:
                        cell_image = box(self.canvas,
                                         i_col, i_row,
                                         color='#FFA')
                    elif c in posicion_destino.cells:
                        cell_image = box(self.canvas,
                                         i_col, i_row,
                                         color='#AFA')
                    else:
                        cell_image = box(self.canvas,
                                         i_col, i_row,
                                         color='#AAf')
                    self.to_clear.append(cell_image)

        self.canvas.after(30, self.draw)


if __name__ == '__main__':
    root = Tk()
    root.geometry(str(WIDTH)+'x'+str(HEIGHT))
    window = MainWindow()
    window.draw()
    root.mainloop()
