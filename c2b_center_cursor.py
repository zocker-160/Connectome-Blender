import bpy

class C2b_CenterCursor(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple test operator"
    bl_description = "Center 3D cursor"

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        return {'FINISHED'}