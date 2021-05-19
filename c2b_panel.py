import bpy

class Panel(bpy.types.Panel):
    bl_idname = "C2B_PT_Panel"
    bl_label = "Connectome→Blender"
    bl_category = "Connectome→Blender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
            layout = self.layout
            
            row = layout.row()
            row.label(text="Tract source file:")

            row = layout.row()
            row.prop(context.scene, "tract_file", text="")

            row = layout.row()
            row.label(text="Tracts: " + str(context.scene.tract_count))

            row = layout.row()
            row.label(text="Curves: " + str(context.scene.curve_count))

            row = layout.row()
            row.label(text="Vectors: " + str(context.scene.vertex_count))

            row = layout.row()
            row.operator('c2b.parse', text="Calculate tract data")

            row = layout.row()
            row.operator('c2b.plot_tracts', text="Plot tract as curves")
