
import math
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])

Point.__str__ = lambda p: str(p.x) + ', ' + str(p.y)

class Vector:

    @staticmethod
    def _intersection(l1, l2):
        ''' Finds the point in which two lines l1 and l2 intersect
            each line is a pair of points (x, y)
        '''

        (x1, y1), (x2, y2) = l1
        (x3, y3), (x4, y4) = l2

        num_x = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
        denom_x = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

        num_y = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)
        denom_y = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

        return Vector(num_x/denom_x, num_y/denom_y)

    def __init__(self, x, y, origin=Point(0, 0)):
        self.x = x
        self.y = y
        self.origin = origin

    @classmethod
    def from_points(cls, p1, p2):
        x = p2.x - p1.x
        y = p2.y - p1.y
        return cls(x, y, p1)

    @property
    def norm(self):
        return math.sqrt(self * self)

    def __matmul__(self, other):
        ''' Returns the angle between two vectors '''
        return math.acos((self*other)/(self.norm*other.norm))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

        return Vector(x, y, self.origin)

    def __mul__(self, other):
        return self.x*other.x + self.y*other.y

    def rotate(self, angle):

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x = cos_a*self.x - sin_a*self.y
        y = sin_a*self.x + cos_a*self.y

        self.x = x
        self.y = y

        return self

    def intersection(self, other):
        l1 = ((self.x, self.y), self.origin)
        l2 = ((other.x, other.y), other.origin)
        return Vector._intersection(l1, l2)
