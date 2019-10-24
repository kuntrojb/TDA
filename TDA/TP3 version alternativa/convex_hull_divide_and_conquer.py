

from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

from functools import partial

def cutting_point(x_mid, l, r, i, j):
    i = i % len(l)
    j = j % len(r)
    p1, p2 = l[i], r[j]
    if p2.x - p1.x == 0:
        print(p2, p1)
    slope = (p2.y-p1.y)/(p2.x - p1.x)
    return p1.y + slope*(x_mid - p1.x)

def rotate_counterclockwise(points, start, stop):
    if len(points) == 1:
        return list(points)
    if len(points) == 0:
        raise Exception('No sé por qué pasa esto')

    if start == stop:
        return [points[start]]

    x_min = x_max = points[start].x
    i_min = i_max = 0

    stop = (stop + 1) % len(points)
    if start < stop:
        new_points = points[start:stop]
    elif start > stop or start == stop:
        new_points = points[start:] + points[:stop]

    return new_points

class DivideAndConquerHull:

    def __init__(self, points):
        ''' points must be a list of Point, or whatever has both an x and a y
        member '''

        if not isinstance(points, list):
            raise TypeError('points must be a list of Point')

        points.sort(key=lambda p: p.x)
        self.points = list(points)
        self.convex_hull = []

        self.left_half = None
        self.right_half = None

        self.down_i = None
        self.up_i = None

        self.complete = False

    def steps(self):
        ''' Return a generator with all the steps of the algorithm '''

        # If we are at a base case we return the solution
        if 0 < len(self.points) <= 2:
            self.convex_hull = list(self.points)
            self.rightmost = -1  # must be -1 to handle the case with 1 point
            self.leftmost = 0
            self.complete = True
            yield False
            return
        if len(self.points) == 0:
            raise Exception('This should not happen')

        left_points = self.points[:len(self.points)//2]
        right_points = self.points[len(self.points)//2:]
        self.left_half = DivideAndConquerHull(left_points)
        self.right_half = DivideAndConquerHull(right_points)

        for step in self.left_half.steps():
            yield False

        for step in self.right_half.steps():
            yield False

        # merge
        i = self.left_half.rightmost  # rightmost on the left side
        j = self.right_half.leftmost  # leftmost on the right side

        x_mid = (self.left_half.convex_hull[i].x + self.right_half.convex_hull[j].x)/2
        y = partial(cutting_point, x_mid,
                    self.left_half.convex_hull, self.right_half.convex_hull)

        self.up_i, self.up_j = i, j
        yield False
        while y(i, j-1) > y(i, j) or y(i+1, j) > y(i, j):
            if y(i, j-1) > y(i, j):
                j = (j-1) % len(self.right_half.convex_hull)
            else:
                i = (i+1) % len(self.left_half.convex_hull)
            self.up_i, self.up_j = i, j
            yield False

        i = self.left_half.rightmost  # rightmost on the left side
        j = self.right_half.leftmost  # leftmost on the right side

        self.down_i, self.down_j = i, j
        yield False
        while y(i, j+1) < y(i, j) or y(i-1, j) < y(i, j):
            if y(i, j+1) < y(i, j):
                j = (j+1) % len(self.right_half.convex_hull)
            else:
                i = (i-1) % len(self.left_half.convex_hull)
            self.down_i, self.down_j = i, j
            yield False

        left_hull = rotate_counterclockwise(self.left_half.convex_hull, self.up_i, self.down_i)
        right_hull = rotate_counterclockwise(self.right_half.convex_hull, self.down_j, self.up_j)

        self.convex_hull = left_hull + right_hull

        self.up_i = None
        self.down_i = None

        # can be made more efficient
        i_min = i_max = 0
        x_min = x_max = self.convex_hull[0].x
        for i, p in enumerate(self.convex_hull):
            if p.x < x_min:
                i_min, x_min = i, p.x
            if p.x > x_max:
                i_max, x_max = i, p.x

        self.leftmost = i_min
        self.rightmost = i_max

        self.complete = True
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

            if self.up_i is not None:
                up_line_points = [self.left_half.convex_hull[self.up_i],
                                  self.right_half.convex_hull[self.up_j]]
                axes.plot(*zip(*up_line_points), 'C1')
            if self.down_i is not None:
                down_line_points = [self.left_half.convex_hull[self.down_i],
                                    self.right_half.convex_hull[self.down_j]]
                axes.plot(*zip(*down_line_points), 'C2')
        else:
            self.points_to_plot = [*self.convex_hull, self.convex_hull[0]]
            # Plot the whole thing
            axes.plot(*zip(*self.points_to_plot), 'C0')
