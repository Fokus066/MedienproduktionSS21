from os import name
import bpy, typing, random
from random import randrange

class Hay_Bale: 

    area_x = 50
    area_y = 50

    bale_x = 2
    bale_y = 3
    bale_z = 3

    number_of_balls = 3

    def generate_bale(self):

        

        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))

        ob = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.area_x,self.area_y,0))
        bpy.ops.mesh.subdivide(number_cuts=7)
        bpy.ops.object.editmode_toggle()

        for number in range(self.number_of_balls):
            x = randrange(self.area_x)
            y = randrange(self.area_y)
            bpy.ops.mesh.primitive_cylinder_add(
                location=(x, y, self.bale_z *0.5), 
                depth=self.bale_z, 
                radius=self.bale_x)
        
            bpy.context.object.rotation_euler[1] = 1.5708
            ob = bpy.context.active_object
                #create the Material
            new_mat = bpy.data.materials.new(name = "Hay Material")
            ob.data.materials.append(new_mat)

            new_mat.use_nodes = True
            nodes = new_mat.node_tree.nodes

            #Operators
            principled_node = nodes.get('Principled BSDF')

            #load image to node
            # Manuel: /Users/manuelhaugg/MedienproduktionSS21/materials/street.png
            bpy.ops.image.open(filepath="/Users/manuelhaugg/MedienproduktionSS21/materials/hay.jpg")
            my_image_node = nodes.new("ShaderNodeTexImage")
            my_image_node.image = bpy.data.images["hay.jpg"]
            
            #linking the nodes
            links = new_mat.node_tree.links
            links.new(my_image_node.outputs[0], principled_node.inputs[0])

bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
              
hay_bale = Hay_Bale()
hay_bale.generate_bale()