from os import name
import bpy, typing, random
from random import randrange

class Water:

    def generate_Water(self):
        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
        water = bpy.context.active_object
        water.data.materials.append(self.add_water_color()) 

    def add_water_color(self) -> bpy.types.Material:
        #add material
        water_mat: bpy.types.Material = bpy.data.materials.new("Water Material")
        water_mat.use_nodes = True

        nodes_water: typing.List[bpy.types.Node] = water_mat.node_tree.nodes
        node_musgrav: bpy.types.Node = nodes_water.new("ShaderNodeTexMusgrave")
        node_bump: bpy.types.Node = nodes_water.new("ShaderNodeBump")

        node_musgrav.inputs[2].default_value = 45.000
        node_musgrav.inputs[3].default_value = 18.000
        node_musgrav.inputs[4].default_value = 45.000
        node_musgrav.inputs[5].default_value = 12.000

        node_bump.inputs[0].default_value = 0.1
        
        nodes_water["Principled BSDF"].inputs[0].default_value = (0.20213, 0.244409, 0.8, 1)
        nodes_water["Principled BSDF"].inputs[7].default_value = 0.05
        nodes_water["Principled BSDF"].inputs[4].default_value = 0.9
            
        water_mat.node_tree.links.new(node_musgrav.outputs[0], node_bump.inputs[2])
        water_mat.node_tree.links.new(node_bump.outputs[0], nodes_water["Principled BSDF"].inputs[20])
        
        return water_mat

water = Water()
water.generate_Water()