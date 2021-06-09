from os import name
import bpy, typing 

class house: 

    housemainX = 20
    housemainY = 15
    housemainZ = 10

    garageX = 12
    garageY = 15
    garageZ = 6

    door_size_x = 0.3
    door_size_y = 2.5
    door_size_z = 4

    def generate_building(self):

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0,  self.housemainZ * 0.5), scale=(self.housemainX, self.housemainY,self.housemainZ))

        mainhouse = bpy.context.object

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(self.garageX*0.33, self.garageY ,self.garageZ * 0.5), scale=(self.garageX, self.garageY, self.garageZ))

        garage = bpy.context.object

        door1 = bpy.ops.mesh.primitive_cube_add(scale=(self.door_size_x, self.door_size_y, self.door_size_z),location=( self.housemainX *0.5 , 0, self.door_size_z*0.5))
    
    def add_glass(self) -> bpy.types.Material:
        #add material
        glass_mat: bpy.types.Material = bpy.data.materials.new("Water Material")
        glass_mat.use_nodes = True

        nodes_glass: typing.List[bpy.types.Node] = glass_mat.node_tree.nodes
       
        nodes_glass["Principled BSDF"].inputs[5].default_value = 1.0       
        nodes_glass["Principled BSDF"].inputs[7].default_value = 0.0
        nodes_glass["Principled BSDF"].inputs[15].default_value = 1.0
        #nodes_glass.use_screen_refraction = True
        bpy.context.scene.eevee.use_ssr = True
        bpy.context.scene.eevee.use_ssr_refraction = True
        
        return glass_mat

    def generate_Window(self):

        windows_size_x = 0.5
        windows_size_y = 3
        windows_size_z = 2

        windows = []
        
        window1 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( self.housemainX *0.5 , 0.25*self.housemainY, self.housemainZ*0.66))
        window2 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( self.housemainX *0.5 , -0.25*self.housemainY, self.housemainZ*0.66))
        window3 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( -self.housemainX *0.5 , 0.25*self.housemainY, self.housemainZ*0.66))
        window4 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( -self.housemainX *0.5 , -0.25*self.housemainY, self.housemainZ*0.66))

        sidewindows_size_x = 3
        sidewindows_size_y = 0.5
        sidewindows_size_z = 2

        window5 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*0.33, -self.housemainY*0.5, self.housemainZ*0.66))
        window6 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*-0.33, -self.housemainY*0.5, self.housemainZ*0.66))
        window7 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*0, -self.housemainY*0.5, self.housemainZ*0.66))

        windows.append(window1)
        windows.append(window2)
        windows.append(window3) 
        windows.append(window4)
        windows.append(window5)
        windows.append(window6)
        windows.append(window7) 

        windows
        print(windows)

        
                    
    

house= house()
house.generate_building()
house.generate_Window()

    
