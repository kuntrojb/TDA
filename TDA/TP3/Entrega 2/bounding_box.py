from vector import Point
from vector import Vector

# Standard directions
LEFT = Vector(-1, 0)
RIGHT = Vector(1, 0)
UP = Vector(0, 1)
DOWN = Vector(0, -1)

def extremaDC(points, direction, i=0, j=-1):
    ''' Given a list of points representing a convex polygon in counterclockwise
        order, it returns the point with the maximum coordinate in the given
        direction.

        points: list of Point representing the bounds of a convex polygon
        listed counterclockwise

        direction: Vector

        i, j: indexes representing the starting and ending points of the segment
        where the extrema is located
        '''

    i %= len(points)
    j %= len(points)

    # The total number of points we have in the segment i--j
    n_points = (j - i) % len(points) + 1

    if n_points == 1:  # If we have just one point, we are done
        return points[i]
    if n_points == 2:  # If we have two points, we check between those two
        if Vector.from_point(points[i])*direction > \
           Vector.from_point(points[j])*direction:
           return points[i]
        return points[j]

    n = (i + n_points//2) % len(points)
    a, c = Vector.from_point(points[i]), Vector.from_point(points[n])
    va = Vector.from_points(points[i], points[(i + 1) % len(points)])
    vc = Vector.from_points(points[n], points[(n + 1) % len(points)])

    if va*direction > 0:  # If va points "upwards"
        # If vc points "downwards" or c is below a
        if vc*direction < 0 or c*direction < a*direction:
            return extremaDC(points, direction=direction, i=i, j=n)
        else:  # If c is above a
            return extremaDC(points, direction=direction, i=n, j=j)
    else:  # If va points "downwards"
        # If vc points "upwards" or c is below a
        if vc*direction > 0 or c*direction < a*direction:
            return extremaDC(points, direction=direction, i=n, j=j)
        else:  # If c is above a
            return extremaDC(points, direction=direction, i=i, j=n)


def BoundingBoxDC(points):
    ''' points must be a list of Point, or whatever has both an x and a y
    member '''

    if not isinstance(points, list):
        raise TypeError('points must be a list of Point')

    # We need to add the first point to the end
    points.append(points[0])

    # We use a divide and conquer algorithm to find the extrema
    p_xmax = extremaDC(points, RIGHT)
    p_xmin = extremaDC(points, LEFT)
    p_ymax = extremaDC(points, UP)
    p_ymin = extremaDC(points, DOWN)

    xmin, xmax, ymin, ymax = p_xmin.x, p_xmax.x, p_ymin.y, p_ymax.y

    return [Point(xmin, ymin), Point(xmin, ymax),
            Point(xmax, ymax), Point(xmax, ymin)]

def BoundingBox(points):
    xmin, ymin = points[0].x, points[0].y
    xmax, ymax = xmin, ymin

    for p in points:
        if p.x < xmin:
            xmin = p.x
        elif p.x > xmax:
            xmax = p.x
        if p.y < ymin:
            ymin = p.y
        elif p.y > ymax:
            ymax = p.y

    return [Point(xmin, ymin), Point(xmin, ymax),
            Point(xmax, ymax), Point(xmax, ymin)]
