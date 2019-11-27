

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

        # indexes for left, right, bottom and top lines
        il = self.points.index(self.p_xmin)
        ir = self.points.index(self.p_xmax)
        ib = self.points.index(self.p_ymin)
        it = self.points.index(self.p_ymax)

        # four lines representing our caliper, going counterclockwise
        top    = Vector.from_points(p[it], p[it] + Vector(-10,  0))
        bottom = Vector.from_points(p[ib], p[ib] + Vector(+10,  0))
        left   = Vector.from_points(p[il], p[il] + Vector( 0, -10))
        right  = Vector.from_points(p[ir], p[ir] + Vector( 0, +10))

        self.bl = left.intersection(bottom).point
        self.br = bottom.intersection(right).point
        self.tr = right.intersection(top).point
        self.tl = top.intersection(left).point

        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        yield False

        # whichever segment has the minimum angle goes next
        angle_left   = Vector.from_points(p[il], p[(il + 1) % n])@left
        angle_right  = Vector.from_points(p[ir], p[(ir + 1) % n])@right
        angle_top    = Vector.from_points(p[it], p[(it + 1) % n])@top
        angle_bottom = Vector.from_points(p[ib], p[(ib + 1) % n])@bottom

        min_angle = min(angle_left, angle_right, angle_top, angle_bottom)

        print('Angle left', angle_left)
        print('Angle right', angle_right)
        print('Angle top', angle_top)
        print('Angle bottom', angle_bottom)
        print(min_angle)

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

        top.translate(p[it])
        bottom.translate(p[ib])
        left.translate(p[il])
        right.translate(p[ir])

        self.bl = left.intersection(bottom).point
        self.br = bottom.intersection(right).point
        self.tr = right.intersection(top).point
        self.tl = top.intersection(left).point

        yield False

        yield True

    def is_complete(self):
        ''' Returns whether we are finished constructing the convex hull
            or not '''
        return self.complete

    def plot(self, axes, figure):
        ''' Plots our segments '''
        bl, br, tr, tl = self.bl, self.br, self.tr, self.tl
        self.points_to_plot = [bl, br, tr, tl, bl]

        # Plot the whole thing
        axes.plot(*zip(*self.points_to_plot), 'C0')
        for i in [self.top, self.bottom, self.left, self.right]:
            axes.plot((i.origin.x, i.point.x), (i.origin.y, i.point.y), 'C1')
