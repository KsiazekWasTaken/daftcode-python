class PointsContainer:

    class DataPoint:

        def __init__(self):
            self.count = 0
            self.points = []

        def inc_count(self):
            self.count +=1

        def get_count(self):
            return self.count

        def add(self, p):
            self.points.append(p)

    def __init__(self, vertices):
        self.coordinates = {}
        self.add_collection(vertices)

    def add_collection(self, vertices):
        for v in vertices:
            self.add(v)

    def add(self, vertex):
        if vertex.id not in self.coordinates:
            self.coordinates[vertex.id] = self.DataPoint()

        self.coordinates[vertex.id].add(vertex.p)

    def test(self, polygons):
        best_index = -1
        best_count = -1
        in_none = []

        for key, coordinate in self.coordinates.items():
            for point in coordinate.points:
                for polygon in polygons:
                    res = polygon.contains_point(key, point)
                    if res:
                        coordinate.inc_count()

        for key, coordinate in self.coordinates.items():
            if coordinate.get_count() > best_count:
                best_count = coordinate.get_count()
                best_index = key

            if coordinate.get_count() == 0:
                in_none.append(key)

        print("Most often:")
        print(best_index)
        print("Don't belong to any:")
        for a in in_none:
            print(a)
