
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

def graham_angle(p1, p2):
    ''' Not exactly the angle of the vector P₁P₂ but something that preserves
    the order (actually it flips it backwards but that's a good thing):
        if ∠P₁P₂ < ∠P₁P₃ then graham_angle(p1, p2) > graham_angle(p1, p3)
    '''
    if p1 is p2:  # this can only happen if p1 and p2 is self.min_point
        return -1.01  # just to guarantee the starting point is the last one
    v = Point(p2.x - p1.x, p2.y - p1.y)
    # monotonic with the angle, and faster to compute
    return (v.x*abs(v.x))/squared_norm(v)


def squared_norm(p):
    return p.x*p.x + p.y*p.y


def cross(p1, p2, p3):
    # Cross product, returns a positive number if the segments P₁P₂ P₂P₃ rotate
    # counterclockwise
    return (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)


class GrahamScan:

    def __init__(self, points):
        ''' points must be a list of Point, or whatever has both an x and a y
        member '''

        if not isinstance(points, list):
            raise TypeError('points must be a list of Point')
        elif len(points) < 3:
            raise ValueError('Expected a list with at least 3 points')

        self.min_point = min(points, key=lambda p: p.y)
        points.sort(key=lambda p: graham_angle(self.min_point, p))
        self.points = list(points)
        self.convex_hull = [self.min_point]

        # Just to save lines and things we need to delete later on
        self.plot_data = []

    def steps(self):
        ''' Runs the algorithm '''

        while not self.is_complete():
            # if we don't have enough points or our points are fine up until now
            if len(self.convex_hull) < 3 or self.rotates_counterclockwise():
                self.convex_hull.append(self.points.pop())
            else:  # if the last two segments rotate clockwise
                self.convex_hull.pop(-2)  # remove the middle point
            yield False

        yield True

    def is_complete(self):
        ''' Returns whether we are finished constructing the convex hull
            or not '''
        if self.convex_hull[0] is self.convex_hull[-1]:
            if len(self.convex_hull) < 3:
                return False
            return True
        return False

    def rotates_counterclockwise(self):
        ''' Returns true if the last two segments of our shape rotate
         counterclockwise. '''
        if cross(*self.convex_hull[-3:]) > 0:
            return True
        return False

    def plot(self, axes, figure):
        ''' Plots our segments '''

        # Remove any line we already have
        for i in self.plot_data:
            i.remove()
            del i

        # Plot the whole thing
        self.plot_data = axes.plot(*zip(*self.convex_hull), 'C0')
        # Plot the line segment we are working on
        if not self.is_complete():
            self.plot_data.extend(axes.plot(*zip(*self.convex_hull[-2:]), 'C1'))

        figure.canvas.draw()
        figure.canvas.flush_events()
