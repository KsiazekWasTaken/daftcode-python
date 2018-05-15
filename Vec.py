class Vec:
    def __init__(self, p):
        self.p = p

    def norm_sq(self):
        return self.p[0] * self.p[0] + self.p[1] * self.p[1]

    def scale(self, s):
        self.p[0] *= s
        self.p[1] *= s
