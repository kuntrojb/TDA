#!/usr/bin/env python3

import time
import tkinter as tk
from tkinter import Tk, Canvas, Frame

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


    def clear(self, fast=True):
        if fast:
            for item in self.to_clear:
                self.canvas.create_rectangle(*item,
                                             outline='#fff', fill='#fff')

    def draw(self):
        self.clear()

        for y, row in enumerate(deposito.split('\n')):
            for x, cell in enumerate(row):
                if cell != ' ':
                    self.to_clear.append(box(self.canvas,
                                             x, y,
                                             color='#AfA'))

        self.canvas.after(30, self.draw)


if __name__ == '__main__':
    root = Tk()
    root.geometry(str(WIDTH)+'x'+str(HEIGHT))
    window = MainWindow()
    window.draw()
    root.mainloop()
