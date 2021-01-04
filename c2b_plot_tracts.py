import bpy
import re

class C2b_PlotTracts(bpy.types.Operator):
    bl_idname = "curve.plot_tracts"
    bl_label = "Plot Tracts"
    bl_description = "Plot tracts from connectome source file in bezier curves"

    groups = []
    file_data = []

    def execute(self, context):
        tract_file = open(context.scene.tract_file,"r")
        self.file_data = re.split(r"\s\n(\d)\n?", tract_file.read())
        self.file_data.pop() # remove last regex find because it's an empty group, see re.split documentation for more info
        print(self.file_data)

        new_collection = []

        for d in self.file_data:
            if len(str(d)) <= 3:
                if(int(d) not in self.groups):
                    print("Group label " + str(int(d)) + " is not in group list " + str(self.groups))
                    self.groups.append(int(d))
                    
                    print("Creating group collection.")

                    new_collection = bpy.data.collections.new(name="Tract " + str(d))
                    bpy.context.scene.collection.children.link(new_collection) 
                    new_collection.objects.link(current_curve)
                    bpy.context.collection.objects.unlink(current_curve) # remove from default collection

                    print("Added " + str(current_curve) + " to " + str(new_collection))

                else:
                    new_collection.objects.link(current_curve)
                    bpy.context.collection.objects.unlink(current_curve) # remove from default collection
                    print("Added " + str(current_curve) + " to " + str(new_collection))

            else:
                context.view_layer.objects.active = self.makeCurve(d)
                current_curve = context.view_layer.objects.active
                

        self.updateCalculations(context)

        print("Connectome plotting completed!")
        return {'FINISHED'}

    def makeCurve(self, vertices):
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        curveObj = curveData.splines.new('NURBS')
        
        coords3d = self.getTractCoords(vertices)

        curveObj.points.add(len(coords3d))
        for i in coords3d:
            for i, coords in enumerate(coords3d):
                x,y,z = coords
                curveObj.points[i].co = (x, y, z, 1)

        curve = bpy.data.objects.new('Tract Curve', curveData)
        bpy.context.collection.objects.link(curve) # add to default collection for active object tracking, is removed in next steps
        
        return curve

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

    def updateCalculations(self, context):
        context.scene.group_count = len(self.groups)
        context.scene.tract_count = len(self.file_data)
        context.scene.vertex_count = len(self.getTractCoords(str(self.file_data)))

        return
