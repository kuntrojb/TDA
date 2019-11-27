#!/usr/bin/env python

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.backend_bases import MouseButton, MouseEvent, KeyEvent

from collections import namedtuple
from graham import GrahamScan
from convex_hull_divide_and_conquer import DivideAndConquerHull
from rectangulo_contenedor_inicial import BoundingBox

from plot_utils import PlotData

import math
import time

WAIT = 0.05


convex_hull = []

def right_click_handler(event):
    global convex_hull

    scan = GrahamScan(data)
    for step in scan.steps():
        scan.plot(ax, fig)
        time.sleep(WAIT)
    convex_hull = list(scan.convex_hull[:-1])

def divide_and_conquer_hull_handler(event):
    hull = DivideAndConquerHull(data)
    for step in hull.steps():
        plot_data.clean_plot(which='lines')
        hull.plot(ax, fig)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(WAIT)

def bounding_box_handler(event):
    box = BoundingBox(convex_hull)
    for step in box.steps():
        plot_data.clean_plot(which='lines')
        box.plot(ax, fig)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(WAIT*20)


def plot_distance_in_points(p1, p2):
    x, y = abs(p1.x - p2.x), abs(p1.y - p2.y)
    x /= plot_data.xlim[1] - plot_data.xlim[0]
    y /= plot_data.ylim[1] - plot_data.ylim[0]
    x *= plot_data.width_in_points
    y *= plot_data.height_in_points
    return math.sqrt(x*x + y*y)


def left_click_handler(event):
    global data

    if event.xdata is None or event.ydata is None:
        return

    point = Point(x=event.xdata, y=event.ydata)
    for p in data:
        # check if we clicked over a point, so we need to delete it
        if plot_distance_in_points(point, p) < plot_data.marker_radius:
            data.remove(p)
            break
    else:  # if we didn't click over an existing point, we create a new one
        data.append(point)

    data.sort(key=lambda p: p.y, reverse=True)

    plot_data.clean_plot()

    if data:
        ax.scatter(*zip(*data), color='C0', zorder=10, linewidth=0)
        excluded = data[-1]
        ax.scatter(*excluded, color='C1', zorder=10, linewidth=0)


def button_press_handler(event):
    try:
        if isinstance(event, MouseEvent):
            handlers[event.button](event)
        elif isinstance(event, KeyEvent):
            handlers[event.key](event)
    except KeyError:
        pass


handlers = {MouseButton.RIGHT: right_click_handler,
            MouseButton.LEFT: left_click_handler,
            'd': divide_and_conquer_hull_handler,
            'r': bounding_box_handler}

Point = namedtuple('Point', ['x', 'y'])

scatter_data = []
data = []

fig, ax = plt.subplots(figsize=(10, 8))

plt.ion()

plot_data = PlotData(ax)

# Remove the bloody axis ticks
plot_data.ticks = []
# Work on the range 0, 1
plot_data.lim = (0, 100, 0, 100)
plot_data.axes_size = (0.9, 0.9)
# Make the containing box bigger
plot_data.center_axes()

# Connect user events to the plot
connection_ids = []
connection_ids.append(fig.canvas.mpl_connect('button_press_event',
                                             button_press_handler))
connection_ids.append(fig.canvas.mpl_connect('key_press_event',
                                             button_press_handler))

plt.show()
