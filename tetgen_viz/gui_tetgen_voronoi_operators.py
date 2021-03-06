import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
from bpy_extras.io_utils import ExportHelper

class Voronoi_Obj_DrawSwitch(bpy.types.Operator):
    bl_idname = "tviz.voronoi_obj_draw_switch"
    bl_label = "Switch wire and textured draw types"

    # Get the filename
    def execute(self, context):

        # Iterate over all objects
        f = context.scene.tviz
        for obj in f.voronoi_obj_list:

            # Get the blender obj
            obj_blender = bpy.data.objects[obj.name]

            # Set draw type
            if obj_blender.draw_type == 'TEXTURED':
                obj_blender.draw_type = 'WIRE'
            elif obj_blender.draw_type == 'WIRE':
                obj_blender.draw_type = 'TEXTURED'

        return {'FINISHED'}


class Voronoi_Obj_Triangulate_All(bpy.types.Operator):
    bl_idname = "tviz.voronoi_obj_triangulate_all"
    bl_label = "Triangulate all objects"

    # Get the filename
    def execute(self, context):

        # Deselect all objects
        bpy.context.scene.objects.active = None
        for obj in bpy.data.objects:
            obj.select = False

        # Iterate over all objects
        f = context.scene.tviz
        for obj in f.voronoi_obj_list:

            # Get the blender obj
            obj_blender = bpy.data.objects[obj.name]

            # Select object
            obj_blender.select = True
            context.scene.objects.active = obj_blender

            # Select all faces
            bpy.ops.object.mode_set(mode='EDIT')
            # Face selection mode
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            bpy.ops.mesh.select_all(action='SELECT')

            # Triangulate
            bpy.ops.mesh.quads_convert_to_tris()

            # Back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect
            obj_blender.select = False

        return {'FINISHED'}

class Voronoi_Obj_Export_To_PLY(bpy.types.Operator):
    bl_idname = "tviz.voronoi_obj_export_ply"
    bl_label = "Export Voronoi objects to PLY"

    directory = StringProperty(name="directory path") # subtype='DIR_PATH'

    # Get the filename
    def execute(self, context):

        # Deselect all objects
        bpy.context.scene.objects.active = None
        for obj in bpy.data.objects:
            obj.select = False

        # Go through all objects
        f = context.scene.tviz
        for obj in f.voronoi_obj_list:

            # Get the blender obj
            obj_blender = bpy.data.objects[obj.name]

            # Select object
            obj_blender.select = True
            context.scene.objects.active = obj_blender

            # File path
            fpath = self.directory
            if fpath[-1] != "/":
                fpath += "/"
            fpath += obj.name
            fpath += ".ply"

            # Export
            bpy.ops.export_mesh.ply("EXEC_DEFAULT",filepath=fpath)

            # Deseelct object
            obj_blender.select = False

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
