

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

from functools import partial

class BoundingBox:

    def __init__(self, points):
        ''' points must be a list of Point, or whatever has both an x and a y
        member '''

        if not isinstance(points, list):
            raise TypeError('points must be a list of Point')

        points.sort(key=lambda p: p.x)
        self.points = list(points)
        self.bounding_box = []
        self.x0 = None
        self.x1 = None
        self.y0 = None
        self.y1 = None

        self.left_half = None
        self.right_half = None

        self.complete = False

    def steps(self):
        ''' Return a generator with all the steps of the algorithm '''

        # If we are at a base case we return the solution
        if len(self.points) == 1:
            p = self.points[0]
            self.x0, self.y0 = p.x, p.y
            self.x1, self.y1 = p.x, p.y
            yield False
            return
        if len(self.points) == 2:
            p1 = self.points[0]
            p2 = self.points[1]
            self.x0, self.y0 = min(p1.x, p2.x), min(p1.y, p2.y)
            self.x1, self.y1 = max(p1.x, p2.x), max(p1.y, p2.y)
            yield False
            return

        left_points = self.points[:len(self.points)//2]
        right_points = self.points[len(self.points)//2:]
        self.left_half = BoundingBox(left_points)
        self.right_half = BoundingBox(right_points)

        for step in self.left_half.steps():
            yield False

        for step in self.right_half.steps():
            yield False

        # merge

        self.x0 = self.left_half.x0
        self.x1 = self.right_half.x1
        self.y0 = min(self.left_half.y0, self.right_half.y0)
        self.y1 = max(self.left_half.y1, self.right_half.y1)

        self.complete = True
        yield False

        yield True

    def is_complete(self):
        ''' Returns whether we are finished constructing the convex hull
            or not '''
        return self.complete

    def plot(self, axes, figure):
        ''' Plots our segments '''

        if not self.complete:
            if self.left_half is not None:
                self.left_half.plot(axes, figure)
            if self.right_half is not None:
                self.right_half.plot(axes, figure)
        else:
            x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
            p0, p1, p2, p3 = (x0, y0), (x1, y0), (x1, y1), (x0, y1)
            self.points_to_plot = [p0, p1, p2, p3, p0]
            # Plot the whole thing
            axes.plot(*zip(*self.points_to_plot), 'C0')
