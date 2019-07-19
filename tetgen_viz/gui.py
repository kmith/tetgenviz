import bpy
# from bpy.app.handlers import persistent
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils

from . import gui_tetgen_delaunay_objs
from . import gui_tetgen_voronoi_objs
from . import gui_tetgen_voronoi_operators

# Register
def register():
    bpy.utils.register_module(__name__)

# Unregister
def unregister():
    bpy.utils.unregister_module(__name__)

# Main panel class
class TVizPanel(bpy.types.Panel):
    bl_label = "TetGen Viz" # Panel name
    bl_space_type = "VIEW_3D" # where to put panel
    bl_region_type = "TOOLS" # sub location
    bl_category = "TetGen viz"

    @classmethod
    def poll(cls, context):
        return (context.scene is not None)

    def draw(self, context):
        context.scene.tviz.draw ( self.layout )

#######################################################
#######################################################
# Main GUI property group
#######################################################
#######################################################

# Class for context that contains all the functions
class TVizPropGroup(bpy.types.PropertyGroup):

    # List of Delaunay objects (from tetgen)
    delaunay_obj_list = CollectionProperty(type=gui_tetgen_delaunay_objs.Delaunay_Obj_Mesh, name="Delaunay Object List")
    active_delaunay_obj_idx = IntProperty(name="Active Delaunay Object Index", default=0)

    # List of Voronoi objects (from tetgen)
    voronoi_obj_list = CollectionProperty(type=gui_tetgen_voronoi_objs.Voronoi_Obj_Mesh, name="Voronoi Object List")
    active_voronoi_obj_idx = IntProperty(name="Active Voronoi Object Index", default=0)

    # Draw
    def draw(self,layout):

        # TETGEN

        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'LEFT'

        row = box.row()
        row.label("Visualize TetGen Meshes", icon='SURFACE_DATA')

        # Delaunay

        row = box.row()
        row.label("Delaunay meshes")

        row = box.row()
        col = row.column()

        col.template_list("Delaunay_Obj_UL_object", "",
                          self, "delaunay_obj_list",
                          self, "active_delaunay_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("tviz.delaunay_obj_import", icon='ZOOMIN', text="")
        col.operator("tviz.delaunay_obj_remove", icon='ZOOMOUT', text="")
        col.operator("tviz.delaunay_obj_remove_all", icon='X', text="")

        # Voronoi

        row = box.row()
        row.label("Voronoi meshes")

        row = box.row()
        col = row.column()

        col.template_list("Voronoi_Obj_UL_object", "",
                          self, "voronoi_obj_list",
                          self, "active_voronoi_obj_idx",
                          rows=2)

        col = row.column(align=True)
        col.operator("tviz.voronoi_obj_import", icon='ZOOMIN', text="")
        col.operator("tviz.voronoi_obj_remove", icon='ZOOMOUT', text="")
        col.operator("tviz.voronoi_obj_remove_all", icon='X', text="")

        row = box.row()
        row.label("Draw type")
        row.operator("tviz.voronoi_obj_draw_switch")

        row = box.row()
        row.label("Triangulate all objects")
        row.operator("tviz.voronoi_obj_triangulate_all")

        row = box.row()
        row.label("Export all objects to PLY")
        row.operator("tviz.voronoi_obj_export_ply")

    # Add a mesh object to the list
    def add_delaunay_obj(self, name, vert_list, edge_list, face_list, tet_list):
        print("Adding Delaunay object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.delaunay_obj_list]
        if not name in current_object_names:
            obj = self.delaunay_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.delaunay_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.edge_list) > 0:
                obj.edge_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.tet_list) > 0:
                obj.tet_list.remove ( 0 )

        obj.name = name
        for v in vert_list:
            obj.vert_list.add()
            obj.vert_list[-1].set_from_list(v)
        for e in edge_list:
            obj.edge_list.add()
            obj.edge_list[-1].set_from_list(e)
        for f in face_list:
            obj.face_list.add()
            obj.face_list[-1].set_from_list(f)
        for t in tet_list:
            obj.tet_list.add()
            obj.tet_list[-1].set_from_list(t)

    # Remove a mesh object
    def remove_delaunay_obj(self):
        print("Removing Delaunay object from the list")

        self.delaunay_obj_list.remove ( self.active_delaunay_obj_idx )
        if self.active_delaunay_obj_idx > 0:
            self.active_delaunay_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_delaunay_objs(self):
        print("Removing all Delaunay objects")

        while len(self.delaunay_obj_list) > 0:
            self.delaunay_obj_list.remove ( 0 )
        self.active_delaunay_obj_idx = 0

    # Add a mesh object to the list
    def add_voronoi_obj(self, name, vert_list, face_list, cell_list):
        print("Adding Voronoi object to the list")

        # Check by name if the object already is in the list
        current_object_names = [d.name for d in self.voronoi_obj_list]
        if not name in current_object_names:
            obj = self.voronoi_obj_list.add()
        else:
            idx = current_object_names.index(name)
            obj = self.voronoi_obj_list[idx]

            # Clear vert list, tet list
            while len(obj.vert_list) > 0:
                obj.vert_list.remove ( 0 )
            while len(obj.face_list) > 0:
                obj.face_list.remove ( 0 )
            while len(obj.cell_list) > 0:
                obj.cell_list.remove ( 0 )

        obj.name = name
        for v in vert_list:
            obj.vert_list.add()
            obj.vert_list[-1].set_from_list(v)
        for f in face_list:
            obj.face_list.add()
            obj.face_list[-1].set_from_list(f)
        for c in cell_list:
            obj.cell_list.add()
            obj.cell_list[-1].set_from_list(c)

    # Remove a mesh object
    def remove_voronoi_obj(self):
        print("Removing Voronoi object from the list")

        self.voronoi_obj_list.remove ( self.active_voronoi_obj_idx )
        if self.active_voronoi_obj_idx > 0:
            self.active_voronoi_obj_idx -= 1

    # Remove all mesh objects
    def remove_all_voronoi_objs(self):
        print("Removing all Voronoi objects")

        while len(self.voronoi_obj_list) > 0:
            self.voronoi_obj_list.remove ( 0 )
        self.active_voronoi_obj_idx = 0
