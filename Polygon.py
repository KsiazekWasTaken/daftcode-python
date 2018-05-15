from geometry import angle, ccw, is_left, EPS, PI
from math import fabs


class Polygon:
    def __init__(self, _id, _vertices):
        self.id = _id
        self.vertices = _vertices
        self.tags = set()

    def reset(self):
        self.tags = set()

    def contains(self, vertex_a):
        res = self.contains_wn_improved(vertex_a.p)
        if res:
            self.tags.add(vertex_a.id)
        return res

    def contains_point(self, id, point):
        res = self.contains_wn_improved(point)
        if res:
            self.tags.add(id)
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

    def contains_wn_improved(self, p):
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