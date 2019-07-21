# other
import numpy as np
import trimesh
import uuid

class VoronoiElement:

    def __init__(self, name, idx, mesh):

        # Logger for trimesh
        trimesh.util.attach_to_log(level=100)

        self.name = name
        self.idx = idx

        # uuid
        self._uuid = uuid.uuid4()

        # Make the mesh
        self.mesh = mesh

        # Points assigned
        self.points_assigned = np.array([]).astype(float)
        self.point_uuids_assigned = []

    @classmethod
    def fromList(cls, name, idx, vert_list, face_list):
        return cls(name, idx, trimesh.Trimesh(vertices=vert_list, faces=face_list))

    @classmethod
    def fromFile(cls, name, idx, fname):
        return cls(name, idx, trimesh.load(fname))

    @property
    def uuid(self):
        """Get uuid

        Returns:
        uuid: uuid
        """
        return self._uuid

    @property
    def bounds(self):
        return self.mesh.bounds

    # Check if a single point inside
    def check_contains_point(self, pt):
        return self.mesh.ray.contains_points([pt])[0]

    # Check for multiple points
    def check_contains_points(self, pts):
        return self.mesh.ray.contains_points(pts)

    # Assign a single point
    def assign_point(self, pt):
        if self.check_contains_point(pt):
            self.points_assigned = np.append(self.points_assigned,pt)
            return True
        else:
            return False

    # Assign multiple points
    def assign_points(self, pts):
        contains = self.check_contains_points(pts)

        # Assign
        if len(self.points_assigned) == 0:
            self.points_assigned = pts[contains]
        else:
            self.points_assigned = np.concatenate((self.points_assigned,pts[contains]),axis=0)

        # Return remaining points
        return pts[np.invert(contains)]

    # Clear assigned points
    def clear_assigned_points(self):
        self.points_assigned = np.array([]).astype(float)

    # Assign a point uuid
    def assign_point_uuid(self, pt, uuid):
        if self.check_contains_point(pt):
            self.point_uuids_assigned.append(uuid)
            return True
        else:
            return False

    # Assign multiple points uuids
    def assign_point_uuids(self, pts, uuids):
        contains = self.check_contains_points(pts)

        # Assign
        self.point_uuids_assigned += uuids[contains]

        # Return remaining uuids
        return uuids[np.invert(contains)]

    # Clear assigned points
    def clear_assigned_point_uuids(self):
        self.point_uuids_assigned = []
