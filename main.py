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
    intersection, closest_pair, Poly


# read anchor points
anchors_raw = np.genfromtxt('anchors.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
anchors = [(x[1], x[2]) for x in anchors_raw]

# read vertices
vertices_raw = np.genfromtxt('nodes.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
vertices = [None for _ in range(0, len(vertices_raw))]
for V in vertices_raw:
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


cpp_data = np.genfromtxt('cpp_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)
python_data = np.genfromtxt('python_points_data.csv', delimiter=',', dtype=float, missing_values=0, skip_header=1)

fig, ax = plt.subplots()
patches = []

for p in polygons:
    poly = Polygon([ v.p for v in p.vertices[:-1] ])
    patches.append(poly)

np.random.seed(19680801)
colors = 100*np.random.rand(len(patches))
p = PatchCollection(patches, alpha=0.4)
p.set_array(np.array(colors))
ax.add_collection(p)
fig.colorbar(p, ax=ax)
ax.set_ylim([-1.5,1.5])
ax.set_xlim([-1.5,1.5])

plt.show()

