import numpy as np
import pandas as pd
from math import sqrt
from math import fabs
import numpy as np
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.patches import Circle as PlotCircle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from geometry import Circle, Vec, Vertex, EPS, PI, distance,\
    intersection, closest_pair, Poly, best_4, closest_non_intersecting


def average(x):
    sx = 0.0
    sy = 0.0
    c = 0
    for u in x:
        sx += u[0]
        sy += u[1]
        c += 1
    return sx/c, sy/c


EPS_2 = 0.001


def slow_midpoint(A):
    loss = np.empty(len(A))
    for i in range(0, len(A)):
        p = A[i]
        current_loss = 0
        for q in A:
            if q is not None and p is not None:
                current_loss += distance(p, q)
        loss[i] = current_loss
    return A[np.argmin(loss)]


# approximate by the following method:
#   determine intersection point in the measured distance from 2 neighboring anchors
#   each intersection provides 2 points
#   from each pair of points coming from neighboring circles select the closest two
#   save their average
#   return average over all saved results
def estimate(o):
    r = []
    for i in range(0, len(o)-1):
        o1 = o[i]
        o2 = o[i+1]
        p1, p2 = intersection(o1, o2)
        if p1 is not None:
            r.append((p1, p2))
    o1 = o[len(o)-1]
    o2 = o[0]
    p1, p2 = intersection(o1, o2)
    if p1 is not None:
        r.append((p1, p2))
    r.append(r[0])
    res = []
    for i in range (0, len(r)-1):
        aux = [r[i][0], r[i][1], r[i+1][0], r[i+1][1]]
        p1, p2 = closest_pair(aux)
        if p1 is not None and p2 is not None:
            res.append(average([p1, p2]))
    return average(res)

def estimate_more_experimental(o):
    r = []
    for i in range(0, len(o)-1):
        o1 = o[i]
        o2 = o[i+1]
        p1, p2 = intersection(o1, o2)
        if p1 is not None:
            r.append((p1, p2))
        else:
            # the idea is that, if the circles don't intersect
            # we're losing a lot of information
            # try to fake the information by returning the two closest points
            # on the circles
            # it is heavily biased towards the center however
            # and probably needs some adjustments
            # @TODO tomorrow
            r.append(closest_non_intersecting(o1, o2))
    o1 = o[len(o)-1]
    o2 = o[0]
    p1, p2 = intersection(o1, o2)
    if p1 is not None:
        r.append((p1, p2))
    else:
        r.append(closest_non_intersecting(o1, o2))
    r.append(r[0])
    res = []
    for i in range (0, len(r)-1):
        aux = [r[i][0], r[i][1], r[i+1][0], r[i+1][1]]
        p1, p2 = closest_pair(aux)
        if p1 is not None and p2 is not None:
            res.append(average([p1, p2]))
    print(len(res))
    return average(res)


def estimate_experimental(o):
# @TODO find out why this method doesn't work
    r = []
    for i in range(0, len(o)-1):
        o1 = o[i]
        o2 = o[i+1]
        p1, p2 = intersection(o1, o2)
        r.append(p1)
        r.append(p2)
        # r.append((p1, p2))
    o1 = o[len(o)-1]
    o2 = o[0]
    p1, p2 = intersection(o1, o2)
    r.append(p1)
    r.append(p2)
    # r.append((p1, p2))
    r.append(r[0])
    res = best_4(r)
    # for i in range (0, len(r)-1):
    #     aux = [r[i][0], r[i][1], r[i+1][0], r[i+1][1]]
    #     p1, p2 = closest_pair(aux)
    #     if p1 is not None and p2 is not None:
    #         res.append(average([p1, p2]))
    return average(closest_pair(res))


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
vertices = [None for _ in range(0, len(vertices_raw))]
for V in vertices_raw:
    # print(V)
    vertices[int(V[0])] = Vertex(int(V[0]), (V[1], V[2]))


# read polygons
polygons_raw = {}
with open('polygons.csv', 'r') as file:
    for line in file:
        a = np.array([int(v) for v in line.strip().split(",")])
        poly_id = a[0]
        poly_nodes = a[1:]
        polygons_raw[poly_id]= poly_nodes


polygons = []
for poly_id, poly_vertices_ids in polygons_raw.items():
    poly_vertices = [vertices[i] for i in poly_vertices_ids]
    polygons.append(Poly(poly_id, poly_vertices))


python_data = np.genfromtxt('python_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
cpp_data = np.genfromtxt('cpp_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
tags = []

tags_cpp = []
for row in cpp_data:
    tags_cpp.append(Vertex(int(row[0]), (row[1], row[2])))

max_loss = 0.0
max_error = 0.0
total_error = 0.0
total_loss = 0.0
for zz in range(0, len(python_data)):
    dists = python_data[zz][1:]
    answer = cpp_data[zz][1:]
    id = python_data[zz][0]
    id = int(id)
    Azz = [Circle(anchors[i], dists[i]) for i in range(0, len(dists))]
    res = estimate_more_experimental(Azz)
    tags.append(Vertex(id, res))
    # print(res)
    for j in range(0, 4):
        total_error += fabs(distance(anchors[j], answer) - dists[j])
        if distance(anchors[j], answer)-dists[j] > max_error:
            max_error = distance(anchors[j], answer) - dists[j]
    dx = res[0] - answer[0]
    total_loss += fabs(dx)
    dy = res[1] - answer[1]
    total_loss += fabs(dy)
    if dx > max_loss:
        max_loss = dx
    if dy > max_loss:
        max_loss = dy


print(max_loss)
print(max_error)
print(total_loss / (2 * (len(python_data))))
print(total_error / (4 * (len(python_data))))

for tag in tags:
    r = check_position(tag, polygons)
    if r:
        i = 1
        # print(str(tag.p) + " is in one of the polygons")


for p in polygons:
    print("Poly "+str(p.id)+" contains")
    for el in p.tags:
        print(el)


fig, ax = plt.subplots()
patches = []
#
# pp = polygons[2]
# for el in pp.tags:
#     print(el)

for p in polygons:
    if True:
        poly = Polygon([ v.p for v in p.vertices[:-1] ])
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

