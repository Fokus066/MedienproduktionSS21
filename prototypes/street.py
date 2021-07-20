from os import name
import bpy, typing, random
from random import randrange
import os

from pathlib import Path

class Street:
    
    def generate_Street(self):
        base_path = os.getcwd()
        print(base_path)
        bpy.ops.mesh.primitive_plane_add()
        street = bpy.context.active_object
        street.name = "street"

        #move Object
        street.location = (0, 0,0)

        #create the Material
        new_mat = bpy.data.materials.new(name = "My Material")
        street.data.materials.append(new_mat)
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

        #Operators
        principled_node = nodes.get('Principled BSDF')

        #load image to node
        # Manuel: /Users/manuelhaugg/MedienproduktionSS21/materials/street.png
        #Fokus: C:\Users\HFU\Documents\Furtwangen\Uni\Semester_5\Medienproduktion\img\street.png
        base_path = os.getcwd()
        base_path = Path(base_path).parent
        file_path = str(base_path) + '/materials/street.png'

        bpy.ops.image.open(filepath=file_path)
        my_image_node = nodes.new("ShaderNodeTexImage")
        my_image_node.image = bpy.data.images["street.png"]
        
        #linking the nodes
        links = new_mat.node_tree.links
        links.new(my_image_node.outputs[0], principled_node.inputs[0])

street = Street()
#street.generate_Street()