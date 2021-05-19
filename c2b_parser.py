import bpy
import re

class Parser(bpy.types.Operator):
    bl_idname = "c2b.parse"
    bl_label = "Calculate tract data"
    bl_description = "Count the source file's tract groups, individual tracts, and tract curve vectors."

    def execute(self, context):
        print("parser triggered...", end="")
        return self.updateCalculations()

    def getCurves(self):
        tract_file = open(bpy.context.scene["tract_file"],"r").read()

        # Finds all tract listings (group 1) and tract group numbers (group 2):
        curves = re.findall(r"(?P<Curve>(?:(?:\d+\.\d*?\s){3})+)(?:\n(?P<TractID>\d+))", tract_file)
        return curves

    def updateCalculations(self):
        data = self.getCurves()

        bpy.context.scene["tract_count"] = data[-1][1]
        bpy.context.scene["curve_count"] = len(data)

        # save curve-data
        bpy.context.scene["curve_data"] = data

        # context.scene.vertex_count = len(re.findall(r"((\d+(\.\d*)?\s){3})", tract_file))
        
        print("done")
        return {'FINISHED'}