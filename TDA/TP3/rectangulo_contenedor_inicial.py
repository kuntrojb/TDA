

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

from functools import partial

class BoundingBox:

    def __init__(self, points):
        ''' points must be a list of Point, or whatever has both an x and a y
        member '''

        if not isinstance(points, list):
            raise TypeError('points must be a list of Point')

        self.points = list(points)
        self.bounding_box = []
        self.x0 = min(points, key=lambda p: p.x)
        self.x1 = max(points, key=lambda p: p.x)
        self.y0 = min(points, key=lambda p: p.y)
        self.y1 = max(points, key=lambda p: p.y)

        self.area = float('inf')

        self.angle = 0

        self.complete = False

    def steps(self):
        ''' Return a generator with all the steps of the algorithm '''




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
