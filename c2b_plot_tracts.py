import importlib
import bpy
import re
from . import c2b_parser

class PlotTracts(bpy.types.Operator):
    bl_idname = "c2b.plot_tracts"
    bl_label = "Plot Tracts"
    bl_description = "Plot tracts from connectome source file in bezier curves"

    def execute(self, context):
        # Reset group variable and open/parse curve data:
        groups = []
        curves = c2b_parser.Parser.getCurves(c2b_parser.Parser)

        # Plot each dataset retrieved from the file data's regex results:
        for g in curves:
            # Plot curve:
            print("Now plotting a curve in tract ID [" + str(g[1]) + "], using vector set:\n" + str(g[0]))
            context.view_layer.objects.active = self.makeCurve(g[0])
            current_curve = context.view_layer.objects.active

            # If the tract group has not been created yet, create it and add the curve:
            if(int(g[1]) not in groups):
                print("Collection with tract ID [" + str(int(g[1])) + "] does not exist. ")

                groups.append(int(g[1]))                
                print("Created group collection with ID [" + str(int(g[1])) + "]")

                new_collection = bpy.data.collections.new(name="Tract " + str(g[1]))
                bpy.context.scene.collection.children.link(new_collection) 
                new_collection.objects.link(current_curve)
                bpy.context.collection.objects.unlink(current_curve) # remove from default collection
                print("Added " + str(current_curve) + " to " + str(new_collection) + "\n")

            # If the tract group already is created, add the curve:
            else:
                new_collection.objects.link(current_curve)
                bpy.context.collection.objects.unlink(current_curve) # remove from default collection
                print("Added " + str(current_curve) + " to " + str(new_collection) + "\n")

        print("Connectome plotting completed!")

        return {'FINISHED'}

    def makeCurve(self, vertices):
        # Create spline data
        curveData = bpy.data.curves.new('myCurve', type='CURVE')
        curveData.dimensions = '3D'
        curveObj = curveData.splines.new('NURBS')
        
        # Get coordinates to plot
        coords3d = self.getTractCoords(vertices)

        # Plot vectors on curve
        curveObj.points.add(len(coords3d))
        for i in coords3d:
            for i, coords in enumerate(coords3d):
                x,y,z = coords
                curveObj.points[i].co = (x, y, z, 1)

        # Create curve object from spline
        curve = bpy.data.objects.new('Tract Curve', curveData)

        # Temporarily add curve to default collection, so it is the active object
        bpy.context.collection.objects.link(curve)
        
        return curve

    def getTractCoords(self, tract):
        # Get all 3D coordinates for curve from data
        coords_list = re.findall(r"((\d+(\.\d*)?\s){3})", tract)
        tract_vertices = []

        # Extract vector coordinates from tract curve data
        for i in range(0, len(coords_list)):
            coords = coords_list[i][0].split()
            vertex = []

            # Create list of vector integers from data strings
            for c in range(0, len(coords)):
                coordsFloat = float(coords[c])
                if len(vertex) == 2:
                    vertex.append(coordsFloat)
                    tract_vertices.append(tuple((vertex[0],vertex[1],vertex[2],)))
                  # Uncomment for verbose vector plotting:  
                  # print("Vector " + str(i) + ": " + str(vertex))
                    vertex = []
                else:
                    vertex.append(coordsFloat)

        return tract_vertices

