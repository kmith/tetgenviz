import sys
from voronoi_mesh.voronoi_mesh import *

import numpy as np

if __name__ == "__main__":

    no_cells = 147
    v = VoronoiMesh.fromFiles(["ply/voronoi_%04i.ply" % cell_idx for cell_idx in range(0,no_cells)])

    # Bounds
    pt_lower, pt_upper = v.bounds

    # Buffer bounds by 50%
    widths = [1.0*(pt_upper[i] - pt_lower[i]) for i in range(0,3)]
    centers = [0.5*(pt_upper[i] + pt_lower[i]) for i in range(0,3)]
    pt_lower = [centers[i] - 0.5*widths[i] for i in range(0,3)]
    pt_upper = [centers[i] + 0.5*widths[i] for i in range(0,3)]

    # Test points inside the bounds
    pts = np.random.rand(10000,3)
    for i in range(0,3):
        pts[:,i] *= pt_upper[i] - pt_lower[i]
        pts[:,i] += pt_lower[i]

    # Assign points
    pts_outside = v.assign_points(pts)

    # Write out points
    f = open("test_mesh.txt","w")
    for element in v.element_dict.values():
        for pt in element.points_assigned:
            f.write("%f %f %f %i\n" % (tuple(pt) + tuple([element.idx])))

    # Write outside points
    for pt in pts_outside:
        f.write("%f %f %f -1\n" % tuple(pt))

    f.close()
