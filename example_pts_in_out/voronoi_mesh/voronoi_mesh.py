# mcelllearn
from .voronoi_element import *

import os

class VoronoiMesh:

    def __init__(self, element_dict):

        # Store all the elements
        self.element_dict = element_dict

        # Keys
        self._element_uuids = list(self.element_dict.keys())

        # Compute bounds
        if len(self.element_dict) == 0:
            self._bounds = None
        else:
            self._bounds = self.element_dict[self._element_uuids[0]].bounds.copy()
            for uuid in self._element_uuids[1:]:
                bounds = self.element_dict[uuid].bounds.copy()
                self._bounds[0] = [min([bounds[0][i_dim],self._bounds[0][i_dim]]) for i_dim in range(0,3)]
                self._bounds[1] = [max([bounds[1][i_dim],self._bounds[1][i_dim]]) for i_dim in range(0,3)]

    @classmethod
    def fromElementDict(cls, element_dict):
        return cls(element_dict)

    @classmethod
    def fromElementList(cls, element_list):
        element_dict = {}
        for element in element_list:
            element_dict[element.uuid] = element
        return cls(element_dict)

    @classmethod
    def fromFiles(cls, fnames):
        element_dict = {}
        for idx, fname in enumerate(fnames):
            name = os.path.splitext(fname)[0]
            element = VoronoiElement.fromFile(name,idx,fname)
            element_dict[element.uuid] = element
        return cls(element_dict)

    @property
    def bounds(self):
        return self._bounds

    def clear_assigned_points(self):
        for element in self.element_dict.values():
            element.clear_assigned_points()

    def assign_points(self, pts):
        pts_copy = pts.copy()

        # Go through all elements
        for element in self.element_dict.values():
            pts_copy = element.assign_points(pts_copy)

            # Stop if all points assigned
            if len(pts_copy) == 0:
                break

        # Return remaining points
        return pts_copy
