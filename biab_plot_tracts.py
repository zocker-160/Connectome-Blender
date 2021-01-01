import bpy
import re

class Biab_PlotTracts(bpy.types.Operator):
    bl_idname = "curve.plot_tracts"
    bl_label = "Plot Tracts"
    bl_description = "Plot tracts from connectome source file in bezier curves"

    def getTracts(self, tract_file):
        tract_file_data = tract_file.read()
        tracts = re.split('\n\d\n', tract_file_data)
        return tracts

    def getCoords3d(self, tract):
        coords_list = re.findall('((\d+\.\d*?\s){3})', tract)       # get all 3D coordinates from text
        coords3d = []
        for i in range(0, len(coords_list)):
            coords = coords_list[i][0].split()
            vector3d = []
            for c in range(0, len(coords)):       # convert coordinates from str to int
                coordsFloat = float(coords[c])
                if len(vector3d) == 2:
                    vector3d.append(coordsFloat)
                    coords3d.append(tuple((vector3d[0],vector3d[1],vector3d[2],)))
                    vector3d = []
                else:
                    vector3d.append(coordsFloat)
        print(coords3d)
        return coords3d

    def makeCurve(self, tract):
        # create the curve
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        # curveData.resolution_u = 2            # what is this doing? expose?
        curveObj = curveData.splines.new('NURBS')
        
        coords3d = self.getCoords3d(tract)
        self.getCoords3d(tract)
        #coords3d = [(1.5,1,1), (2,2.5,2), (1.2,2.1,1)]

        curveObj.points.add(len(coords3d))
        for i in coords3d:
            for i, coords in enumerate(coords3d):
                x,y,z = coords
                curveObj.points[i].co = (x, y, z, 1)

        # create object, attach to scene
        tract = bpy.data.objects.new('Tract Curve', curveData)
        bpy.context.collection.objects.link(tract)


    def execute(self, context):
        tract_file = open(context.scene.tract_file,"r")
        tracts = self.getTracts(tract_file)

        for t in tracts:
            self.makeCurve(t)

        return {'FINISHED'}