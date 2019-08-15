import bpy
from . import export_xml
from bpy_extras.io_utils import ExportHelper

class Delaunay_Obj_Export_To_XML(bpy.types.Operator, ExportHelper):
    bl_idname = "tviz.delaunay_obj_export_xml"
    bl_label = "Export Delaunay objects to XML"

    # Allowed fnames
    filename_ext = ".xml"

    # Get the filename
    def execute(self, context):

        # Get the selected delaunay object
        f = context.scene.tviz
        obj = f.delaunay_obj_list[f.active_delaunay_obj_idx]

        # Get the verts, etc
        vert_list = [[v.xval, v.yval, v.zval] for v in obj.vert_list]
        tet_list = [[t.v0, t.v1, t.v2, t.v3] for t in obj.tet_list]

        # Export
        export_xml.export_to_xml(self.filepath, vert_list, tet_list)

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
