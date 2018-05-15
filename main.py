import numpy as np
from matplotlib.patches import Polygon as PlotPolygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from geometry import intersection, closest_pair,\
    closest_non_intersecting, average
from Circle import Circle
from Vertex import Vertex
from Polygon import Polygon
from PointContainer import PointsContainer


EPS_2 = 0.001


# A proper explanation can be found in visualization.ipynb
# In short:
# approximate by the following method:
#   determine intersection point in the measured distance from 2 neighboring anchors
#   each intersection provides 2 points
#   from each pair of points coming from neighboring circles select the closest two
#   save their average
#   return average over all saved results
def estimate(o_):
    r = []
    o = list(o_)
    o.append(o[0])
    res = []
    for i in range(0, len(o) - 1):
        o1 = o[i]
        o2 = o[i + 1]
        p1, p2 = intersection(o1, o2)
        if p1 is not None:
            r.append((p1, p2))
        else:
            p1, p2 = closest_non_intersecting(o1, o2)
            res.append(average([p1, p2]))

    r.append(r[0])
    for i in range(0, int(len(o_)/2)):
        o1 = o[i]
        o2 = o[i + int(len(o_)/2)]
        p1, p2 = intersection(o1, o2)
        if p1 is not None:
            r.append((p1, p2))
        else:
            p1, p2 = closest_non_intersecting(o1, o2)
            res.append(average([p1, p2]))
    for i in range(0, len(r) - 1):
        aux = [r[i][0], r[i][1], r[i + 1][0], r[i + 1][1]]
        p1, p2 = closest_pair(aux)
        if p1 is not None and p2 is not None:
            res.append(average([p1, p2]))
    return average(res)


def check_position(vertex, polygons):
    result = False
    for polygon in polygons:
        tmp = polygon.contains(vertex)
        result = result or tmp
    return result


# read anchor points
anchors_raw = np.genfromtxt('anchors.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
anchors = [(x[1], x[2]) for x in anchors_raw]

# read vertices
vertices_raw = np.genfromtxt('nodes.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
vertices = {}
for V in vertices_raw:
    vertices[int(V[0])] = Vertex(int(V[0]), (V[1], V[2]))


# read polygons
polygons_raw = {}
with open('polygons.csv', 'r') as file:
    for line in file:
        a = np.array([int(v) for v in line.strip().split(",")])
        poly_id = a[0]
        poly_nodes = a[1:]
        polygons_raw[poly_id] = poly_nodes


polygons = []
for poly_id, poly_vertices_ids in polygons_raw.items():
    poly_vertices = [vertices[i] for i in poly_vertices_ids]
    polygons.append(Polygon(poly_id, poly_vertices))


python_data = np.genfromtxt('python_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
cpp_data = np.genfromtxt('cpp_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
tags = []

tags_cpp = []
for row in cpp_data:
    tags_cpp.append(Vertex(int(row[0]), (row[1], row[2])))

pts = PointsContainer(tags_cpp)
pts.test(polygons)

max_loss = 0.0
max_error = 0.0
total_error = 0.0
total_loss = 0.0
which = -1

tags_python = []

for data in python_data:
    dists = data[1:]
    id = int(data[0])
    Azz = [Circle(anchors[i], dists[i]) for i in range(0, len(dists))]
    res = estimate(Azz)
    tags.append(Vertex(id, res))

for p in polygons:
    print("Poly "+str(p.id)+" contains")
    for el in p.tags:
        print(el)

poly_1_set = polygons[1].tags
poly_2_set = polygons[2].tags
difference_set = poly_1_set - poly_2_set
print("In poly 1 but not in poly 2:")
for el in difference_set:
    print(el)

pts = PointsContainer(tags)
pts.test(polygons)

for p in polygons:
    print("Poly "+str(p.id)+" contains")
    for el in p.tags:
        print(el)

fig, ax = plt.subplots()
patches = []

for p in polygons:
    if True:
        poly = PlotPolygon([v.p for v in p.vertices[:-1]])
        patches.append(poly)

np.random.seed(19680801)
colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, alpha=0.4)
p.set_array(np.array(colors))
ax.add_collection(p)
fig.colorbar(p, ax=ax)
ax.set_ylim([-1.5, 1.5])
ax.set_xlim([-1.5, 1.5])

for tag in tags_cpp:
    plt.plot([tag.p[0]], [tag.p[1]], label='aa', marker='x', markersize=3, color="blue")
for tag in tags:
    plt.plot([tag.p[0]], [tag.p[1]], label='aa', marker='x', markersize=3, color="green")
plt.show()