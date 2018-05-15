class Vertex:
    def __init__(self, _id, _p):
        self.id = _id
        self.p = _p

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id
        return False
