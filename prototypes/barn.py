from os import name
import bpy, typing 

class Barn: 

    barn_x = 25
    barn_y = 15
    barn_z = 10

    roof_width_x = 25
    roof_width_y = 13
    roof_height_z = 8

    inner_space_width_x = 27
    inner_space_width_y = 13
    inner_space_height_z = 8

    def generate_building(self):

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0,  0), scale=(self.barn_x, self.barn_y,self.barn_z))
        mainhouse = bpy.context.object
        #mainhouse.data.materials.append(self.building_material()) 

        cube_mesh_roof = bpy.ops.mesh.primitive_cube_add(scale=(self.roof_width_x, self.roof_width_y, self.roof_height_z),location=( 0 , 0, self.barn_z*0.5))

        cube_mesh_inner_space = bpy.ops.mesh.primitive_cube_add(scale=(self.inner_space_width_x, self.inner_space_width_y, self.inner_space_height_z),location=( 0 , 0, 0))

        modifier_bool = mainhouse.modifiers.new("Main Bool", "BOOLEAN")
        modifier_bool.object = cube_mesh_inner_space

bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
              
barn = Barn()
barn.generate_building()