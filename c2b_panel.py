import bpy

class Panel(bpy.types.Panel):
    bl_idname = "C2B_PT_Panel"
    bl_label = "Connectome→Blender"
    bl_category = "Connectome→Blender"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context):
            layout = self.layout

            row = layout.row()
            #row.prop(context.scene, "tract_file", text="")
            row.operator('c2b.import', text="Import file", icon='IMPORT')

            row = layout.row()
            row.prop(context.scene, 'tract_file', text="Filepath")

            row = layout.row()
            row.label(text=f'Tracts: {context.scene.get("tract_count")}')

            row = layout.row()
            row.label(text=f'Curves: {context.scene.get("curve_count")}')

            row = layout.row()
            row.label(text=f'Vectors: {context.scene.get("vertex_count")}')

            row = layout.row()
            row.operator('c2b.parse', text="Recalculate tract data")

            row = layout.row()
            row.operator('c2b.plot_tracts', text="Plot tract as curves", icon='NORMALIZE_FCURVES')
