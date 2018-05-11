from cmath import acos
from math import sqrt
from math import pi
from math import fabs

EPS = 0.0000001

PI = pi


# distance between 2D points p1 and p2
def distance(p1, p2):
    return sqrt(pow(p1[0] - p2[0], 2) + pow((p1[1] - p2[1]), 2))


# vector cross product
def cross(a, b):
    return a.p[0] * b.p[1] - a.p[1] * b.p[0]


# vector dot product
def dot(a, b):
    return a.p[0] * b.p[0] + a.p[1] * b.p[1]


class Vec:
    def __init__(self, p):
        self.p = p

    def norm_sq(self):
        return self.p[0] * self.p[0] + self.p[1] * self.p[1]

    def scale(self, s):
        self.p[0] *= s
        self.p[1] *= s


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


class Vertex:
    def __init__(self, _id, _p):
        self.id = _id
        self.p = _p


class Poly:
    def __init__(self, _id, _vertices):
        self.id = _id
        self.vertices = _vertices
        self.tags = set()

    def contains(self, vertex_a):
        res = self.contains_faster(vertex_a.p)
        if res:
            self.tags.add(vertex_a.p)
        return res

    def contains_wn(self, point):
        size = len(self.vertices)
        if size == 0:
            return False
        s = 0.0
        for i in range(0, size - 1):
            v1 = self.vertices[i].p
            if point == v1:
                return True
            v2 = self.vertices[i + 1].p
            if point == v2:
                return True
            if ccw(point, v1, v2):
                s += angle(v1, point, v2)
            else:
                s -= angle(v1, point, v2)
        s = s.real
        print(s)
        print(fabs(fabs(s) - 2 * PI))
        return fabs(fabs(s) - 2 * PI) < EPS

    def contains_faster(self, p):
        wn = 0  # the winding number counter
        size = len(self.vertices)
        for i in range(0, size - 1):  # edge from V[i] to  V[i+1]
            v1 = self.vertices[i].p
            v2 = self.vertices[i+1].p
            if p == v1:
                return True
            if p == v2:
                return True
            if v1[1] <= p[1] + EPS:  # start y <= P.y
                if v2[1] > p[1]:  # an upward crossing
                    le = is_left(v1, v2, p)
                    if fabs(le) < EPS:
                        return True
                    elif le > 0:  # P left of  edge
                        wn += 1  # have  a valid up intersect
            else:  # start y > P.y (no test needed)
                if v2[1] <= p[1] + EPS:  # a downward crossing
                    le = is_left(v1, v2, p)
                    if fabs(le) < EPS:
                        return True
                    elif le < 0:  # P right of  edge
                        wn -= 1  # have a valid down intersect
        return wn != 0


class Circle:
    def __init__(self, p, r):
        self.mid = p
        self.r = r


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
