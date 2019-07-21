import sys
from voronoi_mesh.voronoi_element import *

import numpy as np
import os

if __name__ == "__main__":

    cell_idx = 11
    v = VoronoiElement.fromFile("example element", cell_idx, "ply/voronoi_%04i.ply" % cell_idx)

    # Bounds
    pt_lower, pt_upper = v.bounds

    # Buffer bounds by 50%
    widths = [1.5*(pt_upper[i] - pt_lower[i]) for i in range(0,3)]
    centers = [0.5*(pt_upper[i] + pt_lower[i]) for i in range(0,3)]
    pt_lower = [centers[i] - 0.5*widths[i] for i in range(0,3)]
    pt_upper = [centers[i] + 0.5*widths[i] for i in range(0,3)]

    # Test points inside the bounds
    pts = np.random.rand(1000,3)
    for i in range(0,3):
        pts[:,i] *= pt_upper[i] - pt_lower[i]
        pts[:,i] += pt_lower[i]

    # Check if contained
    contains = v.check_contains_points(pts)

    # Write to file
    f = open("test_element_%04i.txt" % cell_idx,"w")
    for i_pt in range(0,len(pts)):
        if contains[i_pt]:
            f.write("%f %f %f 1\n" % tuple(pts[i_pt]))
        else:
            f.write("%f %f %f 0\n" % tuple(pts[i_pt]))
    f.close()
