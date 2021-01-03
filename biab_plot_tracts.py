import bpy
import re

class Biab_PlotTracts(bpy.types.Operator):
    bl_idname = "curve.plot_tracts"
    bl_label = "Plot Tracts"
    bl_description = "Plot tracts from connectome source file in bezier curves"

    def execute(self, context):
        tract_file = open(context.scene.tract_file,"r")
        file_data = re.split(r"\n(\d)\n", tract_file.read())
        groups = [0]

        for d in file_data:
            #if len(t) <2 then append as group if not found already
            self.makeCurve(d, groups[-1])
        
        self.updateCalculations(context, groups, file_data)

        print("Connectome plotting completed!")
        return {'FINISHED'}

    def makeCurve(self, tract, group):
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        curveObj = curveData.splines.new('NURBS')
        
        coords3d = self.getTractCoords(tract)

        curveObj.points.add(len(coords3d))
        for i in coords3d:
            for i, coords in enumerate(coords3d):
                x,y,z = coords
                curveObj.points[i].co = (x, y, z, 1)

        curve = bpy.data.objects.new('Tract Curve', curveData)
        bpy.context.collection.objects.link(curve)
        # add curve to latest group. create this group if necessary

    def getTractCoords(self, tract):
        coords_list = re.findall(r"((\d+(\.\d*)?\s){3})", tract)       # get all 3D coordinates from tract data
        tract_vertices = []

        for i in range(0, len(coords_list)):
            coords = coords_list[i][0].split()
            vertex = []
            for c in range(0, len(coords)):       # convert coordinates from str to int
                coordsFloat = float(coords[c])
                if len(vertex) == 2:
                    vertex.append(coordsFloat)
                    tract_vertices.append(tuple((vertex[0],vertex[1],vertex[2],)))
                    print("Vector " + str(i) + ": " + str(vertex))
                    vertex = []
                else:
                    vertex.append(coordsFloat)

        return tract_vertices

    def updateCalculations(self, context, groups, file_data):
        context.scene.group_count = len(groups)
        context.scene.tract_count = len(file_data)
        context.scene.vertex_count = len(self.getTractCoords(str(file_data)))

        return
