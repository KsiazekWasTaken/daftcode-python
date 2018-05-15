from cmath import acos
from math import sqrt
from math import pi
from math import fabs
from math import cos, sin, atan2
from Vec import Vec

EPS = 0.0000001

PI = pi


def average(points):
    sx = 0.0
    sy = 0.0
    count = 0
    for point in points:
        sx += point[0]
        sy += point[1]
        count += 1
    return sx/count, sy/count


# distance between 2D points p1 and p2
def distance(p1, p2):
    return sqrt(pow(p1[0] - p2[0], 2) + pow((p1[1] - p2[1]), 2))


# vector cross product
def cross(a, b):
    return a.p[0] * b.p[1] - a.p[1] * b.p[0]


# vector dot product
def dot(a, b):
    return a.p[0] * b.p[0] + a.p[1] * b.p[1]


def points_to_vec(a, b):
    return Vec((a[0] - b[0], a[1] - b[1]))


# angle AOB in rad
def angle(a, o, b):
    oa = points_to_vec(o, a)
    ob = points_to_vec(o, b)
    return acos(dot(oa, ob) / sqrt(oa.norm_sq() * ob.norm_sq()))


# check if a is left to line going through b1, b2
def is_left(p0, p1, p2):
    return ((p1[0] - p0[0]) * (p2[1] - p0[1])
            - (p2[0] - p0[0]) * (p1[1] - p0[1]))


# check if clockwise (for wn algorithm)
def ccw(a, b, c):
    ab = points_to_vec(a, b)
    ac = points_to_vec(a, c)
    return cross(ab, ac) > 0


# return p1, p2 - intersections of circle o1, o2 (it is possible that p1==p2)
def intersection(o1, o2):
    d = distance(o1.mid, o2.mid)
    d = d
    if d > o1.r + o2.r:
        return None, None
    elif d < fabs(o1.r-o2.r):
        return None, None
    elif d == 0 and fabs(o1.r-o2.r) < EPS:
        return None, None
    else:
        a = pow(o1.r, 2) - pow(o2.r, 2) + pow(d, 2)
        a /= 2*d
        h = sqrt(pow(o1.r, 2)-pow(a, 2))
        s = ((o1.mid[0] + a*(o2.mid[0]-o1.mid[0])/d), (o1.mid[1] + a*(o2.mid[1]-o1.mid[1])/d))
        p1 = (
            s[0] + h * (o2.mid[1] - o1.mid[1])/d,
            s[1] - h * (o2.mid[0] - o1.mid[0])/d
        )
        p2 = (
            s[0] - h * (o2.mid[1] - o1.mid[1])/d,
            s[1] + h * (o2.mid[0] - o1.mid[0])/d
        )
        return p1, p2


# return a pair of closest points from collection x
def closest_pair(x):
    min_d = float("inf")
    res = None, None
    if len(x) < 2:
        return None, None
    for i in range(0, len(x)-1):
        p = x[i]
        for j in range(i+1, len(x)):
            q = x[j]
            if distance(p, q) < min_d:
                min_d = distance(p, q)
                res = p, q
    return res


def closest_non_intersecting(o1, o2):
    p0 = o1.mid
    p1 = o2.mid
    r1 = o1.r
    r2 = o2.r

    theta = atan2(p1[1]-p0[1], p1[0]-p0[0])
    p2 = [0.0, 0.0]
    p3 = [0.0, 0.0]
    p4 = [0.0, 0.0]
    p5 = [0.0, 0.0]
    p3[0] = p0[0] - r1 * cos(theta)
    p3[1] = p0[1] - r1 * sin(theta)
    p2[0] = p0[0] + r1 * cos(theta)
    p2[1] = p0[1] + r1 * sin(theta)
    first2 = [p2, p3]
    theta = atan2(p0[1]-p1[1], p0[0]-p1[0])
    p4[0] = p1[0] - r2 * cos(theta)
    p4[1] = p1[1] - r2 * sin(theta)
    p5[0] = p1[0] + r2 * cos(theta)
    p5[1] = p1[1] + r2 * sin(theta)
    second2 = [p4, p5]
    res = None, None
    best = float("inf")
    for i in range(0, len(first2)):
        pp1 = first2[i]
        for j in range(0, len(second2)):
            pp2 = second2[j]
            if distance(pp1, pp2) < best:
                best = distance(pp1, pp2)
                res = [pp1, pp2]
    return res