import bpy

class Biab_Panel(bpy.types.Panel):
    bl_idname = "BIAB_PT_Panel"
    bl_label = "Brain in a Blender"
    bl_category = "Brain in a Blender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
            layout = self.layout
            
            row = layout.row()
            row.label(text="Tract source file:")

            row = layout.row()
            row.prop(context.scene, "tract_file", text="")

            row = layout.row()
            row.operator('curve.plot_tracts', text="Plot tract curves")

            row = layout.row()
            row.label(text="Additional operations:")

            row = layout.row()
            row.operator('view3d.cursor_center', text="Center 3D Cursor")