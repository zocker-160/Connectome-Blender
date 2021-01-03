import bpy
import re

class Biab_Calculate(bpy.types.Operator):
    bl_idname = "curve.plot_tracts"
    bl_label = "Plot Tracts"
    bl_description = "Plot tracts from connectome source file in bezier curves"

    def getTractCount(self, tract_file):
        tract_file_data = tract_file.read()
        tracts = re.split('\n\d\n', tract_file_data)
        return len(tracts)

    def getGroupCount(self, tract_file):
        tract_file_data = tract_file.read()
        groups = re.findall('\n\d\n', tract_file_data)
        return len(groups)

    def getVertexCount(self, tract_file):
        tract_file_data = tract_file.read()
        groups = re.findall('\n\d\n', tract_file_data)
        return len(groups)

    def getCoords3d(self, tract):
        coords_list = re.findall('(?!\d+\n)((\d+(\.\d*)?\s))', tract)       # get all 3D vectors from text
        coords = coords_list[i][0].split()
        print(coords)
        return len(coords)

    def execute(self, context):
        tract_file = open(context.scene.tract_file,"r")
        tracts = self.getTracts(tract_file)

        for t in tracts:
            print("\nNow calculating line: " + str(tracts.index(t)))

        return {'FINISHED'}