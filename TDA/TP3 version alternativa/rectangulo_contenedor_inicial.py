

from vector import Vector
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

from functools import partial

import math

class BoundingBox:

    def __init__(self, points):
        ''' points must be a list of Point, or whatever has both an x and a y
        member '''

        if not isinstance(points, list):
            raise TypeError('points must be a list of Point')

        self.points = list(points)
        self.bounding_box = []
        self.p_xmin = min(points, key=lambda p: p.x)
        self.p_xmax = max(points, key=lambda p: p.x)
        self.p_ymin = min(points, key=lambda p: p.y)
        self.p_ymax = max(points, key=lambda p: p.y)

        self.area = float('inf')

        self.complete = False

    def steps(self):
        ''' Return a generator with all the steps of the algorithm '''

        # some shorthands
        n = len(self.points)
        p = self.points

        # four lines representing our caliper, going counterclockwise
        top    = Vector.from_points(self.p_ymax, Point(self.p_ymax.x - 1, self.p_ymax.y))
        bottom = Vector.from_points(self.p_ymin, Point(self.p_ymin.x + 1, self.p_ymin.y))
        left   = Vector.from_points(self.p_xmin, Point(self.p_xmin.x, self.p_xmin.y + 1))
        right  = Vector.from_points(self.p_xmax, Point(self.p_xmax.x, self.p_xmax.y - 1))

        # indexes for left, right, bottom and top lines
        il = self.points.index(self.p_xmin)
        ir = self.points.index(self.p_xmax)
        ib = self.points.index(self.p_ymin)
        it = self.points.index(self.p_ymax)

        # whichever segment has the minimum angle goes next
        angle_left   = Vector.from_points(p[il], p[(il + 1) % n])@left
        angle_right  = Vector.from_points(p[ir], p[(ir + 1) % n])@right
        angle_top    = Vector.from_points(p[it], p[(it + 1) % n])@top
        angle_bottom = Vector.from_points(p[ib], p[(ib + 1) % n])@bottom

        min_angle = min(angle_left, angle_right, angle_top, angle_bottom)

        left = left.rotate(min_angle)
        right = right.rotate(min_angle)
        top = top.rotate(min_angle)
        bottom = bottom.rotate(min_angle)

        # TODO: replace if-else
        if min_angle == angle_left:
            il = (il + 1) % n
        elif min_angle == angle_right:
            ir = (ir + 1) % n
        elif min_angle == angle_top:
            it = (it + 1) % n
        elif min_angle == angle_bottom:
            ib = (ib + 1) % n
        else:
            raise Exception('min function didn\'t return an expected minimum')


        # rotating counterclockwise
        a = angle(vector(top), vector(left))


        yield True

    def is_complete(self):
        ''' Returns whether we are finished constructing the convex hull
            or not '''
        return self.complete

    def plot(self, axes, figure):
        ''' Plots our segments '''

        x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
        p0, p1, p2, p3 = (x0, y0), (x1, y0), (x1, y1), (x0, y1)
        self.points_to_plot = [p0, p1, p2, p3, p0]
        # Plot the whole thing
        axes.plot(*zip(*self.points_to_plot), 'C0')
