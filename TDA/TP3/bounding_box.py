
from vector import Point

def BoundingBoxDC(points):
    ''' points must be a list of Point, or whatever has both an x and a y
    member '''

    if not isinstance(points, list):
        raise TypeError('points must be a list of Point')

    # If we are at a base case we return the solution
    if len(points) == 1:
        p = points[0]
        return [p, p, p, p]
    if len(points) == 2:
        p1 = points[0]
        p2 = points[1]
        xmin, ymin = min(p1.x, p2.x), min(p1.y, p2.y)
        xmax, ymax = max(p1.x, p2.x), max(p1.y, p2.y)
        return [Point(xmin, ymin), Point(xmin, ymax),
                Point(xmax, ymax), Point(xmax, ymin)]

    # just in case we sort the points
    points.sort(key=lambda p: p.x)

    left_points = self.points[:len(self.points)//2]
    right_points = self.points[len(self.points)//2:]
    left_box = BoundingBoxDC(left_points)
    right_box = BoundingBoxDC(right_points)

    # merge
    xmin = left_box[0].x
    xmax = right_box[-1].x
    ymin = min(left_box[0].y, right_box[0].y)
    ymax = max(left_box[1].y, right_box[1].y)

    return [Point(xmin, ymin), Point(xmin, ymax),
            Point(xmax, ymax), Point(xmax, ymin)]

def BoundingBox(points):
    xmin = min(points, key=lambda p: p.x).x
    ymin = min(points, key=lambda p: p.y).y
    xmax = max(points, key=lambda p: p.x).x
    ymax = max(points, key=lambda p: p.y).y

    return [Point(xmin, ymin), Point(xmin, ymax),
            Point(xmax, ymax), Point(xmax, ymin)]
