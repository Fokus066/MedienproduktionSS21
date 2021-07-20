from os import name
import bpy, typing, random
from random import randrange
import os

from pathlib import Path

class Pavement:
    def generate_pavement(self):
        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, -31.5, 0))
            
        pavement = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(20,1.5,1))
        bpy.ops.mesh.subdivide(number_cuts=100, fractal=0.03, fractal_along_normal=1, seed=0)
        bpy.ops.object.editmode_toggle()
                
        pavement.data.materials.append(self.add_pavement_texture())

    def add_pavement_texture(self) -> bpy.types.Material:
        #add material
        pavement_mat: bpy.types.Material = bpy.data.materials.new("pavement material")
        pavement_mat.use_nodes = True

        nodes_pavement: typing.List[bpy.types.Node] = pavement_mat.node_tree.nodes
        node_texbrick: bpy.types.Node = nodes_pavement.new("ShaderNodeTexBrick")
        node_texchecker1: bpy.types.Node = nodes_pavement.new("ShaderNodeTexChecker")
        node_texchecker2: bpy.types.Node = nodes_pavement.new("ShaderNodeTexChecker")

        node_texchecker1.inputs[2].default_value = (0, 0, 0, 1)
        node_texchecker2.inputs[2].default_value = (0, 0, 0, 1)

        node_texbrick.offset = 0
        node_texbrick.offset_frequency = 2
        node_texbrick.squash = 2.4
        node_texbrick.squash_frequency = 7
        node_texbrick.inputs[1].default_value = (0.662596, 0.169031, 0.21754, 1)
        node_texbrick.inputs[2].default_value = (0.0801457, 0.0779214, 0.0714665, 1)
        node_texbrick.inputs[3].default_value = (0.41235, 0.396982, 0.390275, 1)
        node_texbrick.inputs[4].default_value = 50
        node_texbrick.inputs[5].default_value = 0.125
        node_texbrick.inputs[6].default_value = 0
        node_texbrick.inputs[7].default_value = 0.8
        node_texbrick.inputs[8].default_value = 1.4
        node_texbrick.inputs[9].default_value = 5.75
        
        pavement_mat.node_tree.links.new(node_texchecker1.outputs[1], nodes_pavement["Principled BSDF"].inputs[7])
        pavement_mat.node_tree.links.new(node_texchecker2.outputs[1], nodes_pavement["Principled BSDF"].inputs[4])
        pavement_mat.node_tree.links.new(node_texbrick.outputs[0], nodes_pavement["Principled BSDF"].inputs[0])
        
        return pavement_mat  

pavement = Pavement()
pavement.generate_pavement()