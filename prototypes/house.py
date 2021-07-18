import bpy, typing 

class house: 


    groundX = 40
    groundY= 40
    groundZ= 0.5

    housemainX = 20
    housemainY = 15
    housemainZ = 10

    garageX = 12
    garageY = 15
    garageZ = 6

    door_size_x = 0.3
    door_size_y = 2.5
    door_size_z = 4
    
    patio_size_x = 0.3
    patio_size_y = 3.5
    patio_size_z = 4



    garagedoor_size_x = 0.3
    garagedoor_size_y = 4.5
    garagedoor_size_z = 4
   

    def building_material(self) -> bpy.types.Material:

        building_mat: bpy.types.Material = bpy.data.materials.new("Water Material")
        building_mat.use_nodes = True

        nodes_building: typing.List[bpy.types.Node] = building_mat.node_tree.nodes
        node_musgrav: bpy.types.Node = nodes_building.new("ShaderNodeTexMusgrave")
        node_texcoord: bpy.types.Node = nodes_building.new("ShaderNodeTexCoord")
        node_bump: bpy.types.Node = nodes_building.new("ShaderNodeBump")
        node_noise: bpy.types.Node = nodes_building.new("ShaderNodeTexNoise")
        node_mix: bpy.types.Node = nodes_building.new("ShaderNodeMixRGB")
        node_colorramp_1: bpy.types.Node = nodes_building.new("ShaderNodeValToRGB")
        node_colorramp_2: bpy.types.Node = nodes_building.new("ShaderNodeValToRGB")

                
        node_mapping: bpy.types.Node = nodes_building.new("ShaderNodeMapping")

        node_mix.blend_type = 'DIFFERENCE'
        node_bump.inputs[0].default_value = 0.3
        node_musgrav.inputs[3].default_value = 21.000
        node_musgrav.inputs[3].default_value = 0
        node_noise.inputs[2].default_value = 6.000
        node_noise.inputs[3].default_value = 16.000
        node_noise.inputs[4].default_value = 0.1
        node_noise.inputs[5].default_value = 4.0
        node_colorramp_1.color_ramp.elements[0].color = (0.480457, 0.480457, 0.480457, 1)
        node_colorramp_1.color_ramp.elements[1].color =  (0.781435, 0.781435, 0.781435, 1)
        
        node_colorramp_2.color_ramp.elements[1].color = (0.875713, 0.875713, 0.875713, 1)
        node_colorramp_2.color_ramp.elements[0].color = (0.480457, 0.480457, 0.480457, 1)
        

        building_mat.node_tree.links.new(node_texcoord.outputs[3], node_mapping.inputs[0])

        building_mat.node_tree.links.new(node_mapping.outputs[0],node_musgrav.inputs[0])
        building_mat.node_tree.links.new(node_mapping.outputs[0],node_noise.inputs[0])

        building_mat.node_tree.links.new(node_musgrav.outputs[0],node_mix.inputs[1])

        building_mat.node_tree.links.new(node_noise.outputs[0],node_colorramp_1.inputs[0])
        building_mat.node_tree.links.new(node_colorramp_1.outputs[0], node_mix.inputs[2])

        building_mat.node_tree.links.new( node_mix.outputs[0],node_colorramp_2.inputs[0])
        building_mat.node_tree.links.new( node_mix.outputs[0],node_bump.inputs[2])

        building_mat.node_tree.links.new( node_colorramp_2.outputs[0], nodes_building["Principled BSDF"].inputs[0])
        building_mat.node_tree.links.new( node_bump.outputs[0], nodes_building["Principled BSDF"].inputs[20])

        return building_mat
        

    def generate_building(self):

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0,  self.housemainZ * 0.5), scale=(self.housemainX, self.housemainY,self.housemainZ))
         #extrudien
        bpy.ops.object.mode_set( mode   = 'EDIT'   )
        bpy.ops.mesh.select_mode( type  = 'FACE'   )
        bpy.ops.mesh.select_all( action = 'SELECT' )

        bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value":(0, 0, 8)})

        bpy.ops.object.mode_set( mode = 'OBJECT' )
        mainhouse = bpy.context.object
        mainhouse = bpy.context.object

        mainhouse.data.materials.append(self.building_material()) 

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(self.garageX*0.33, self.garageY ,self.garageZ * 0.5), scale=(self.garageX, self.garageY, self.garageZ))

        garage = bpy.context.object
        garage.data.materials.append(self.building_material()) 

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, self.housemainY *0.16666, 0), scale=(self.groundX, self.groundY, self.groundZ))

        ground = bpy.context.object

        door1 = bpy.ops.mesh.primitive_cube_add(scale=(self.door_size_x, self.door_size_y, self.door_size_z),location=( self.housemainX *0.5 , 0, self.door_size_z*0.5))

        patio1 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_x, self.patio_size_y, self.patio_size_z),location=( self.housemainX *-0.5 , self.housemainY *0.33, self.housemainZ*0.2))
        patio2 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_y, self.patio_size_x, self.patio_size_z),location=( self.housemainX *-0.25 , self.housemainY *0.5, self.housemainZ*0.2))
        patio3 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_y, self.patio_size_x, self.patio_size_z),location=( self.housemainX *0.2 , self.housemainY *0.5, self.housemainZ*0.8))

        garagedoor1 = bpy.ops.mesh.primitive_cube_add(scale=(self.garagedoor_size_x, self.garagedoor_size_y, self.garagedoor_size_z),location=( self.housemainX *0.5 , self.housemainY *1, self.garagedoor_size_z*0.5))
    
    # def add_glass(self) -> bpy.types.Material:
    #     #add material
    #     glass_mat: bpy.types.Material = bpy.data.materials.new("Water Material")
    #     glass_mat.use_nodes = True

    #     nodes_glass: typing.List[bpy.types.Node] = glass_mat.node_tree.nodes
       
    #     nodes_glass["Principled BSDF"].inputs[5].default_value = 1.0       
    #     nodes_glass["Principled BSDF"].inputs[7].default_value = 0.0
    #     nodes_glass["Principled BSDF"].inputs[15].default_value = 1.0
    #     #nodes_glass.use_screen_refraction = True
    #     bpy.context.scene.eevee.use_ssr = True
    #     bpy.context.scene.eevee.use_ssr_refraction = True
        
    #     return glass_mat

    def generate_Window(self):

        windows_size_x = 0.5
        windows_size_y = 3
        windows_size_z = 2

        windows = []
        
        window1 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( self.housemainX *0.5 , 0.25*self.housemainY, self.housemainZ*0.90))
        window2 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( self.housemainX *0.5 , -0.25*self.housemainY, self.housemainZ*0.90))
        window3 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( -self.housemainX *0.5 , 0.25*self.housemainY, self.housemainZ*0.90))
        window4 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( -self.housemainX *0.5 , -0.25*self.housemainY, self.housemainZ*0.90))

        sidewindows_size_x = 3
        sidewindows_size_y = 0.5
        sidewindows_size_z = 2

        window5 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*0.33, -self.housemainY*0.5, self.housemainZ*0.90))
        window6 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*-0.33, -self.housemainY*0.5, self.housemainZ*0.90))
        window7 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( self.housemainX*0, -self.housemainY*0.5, self.housemainZ*0.90))

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
#house.generate_Garagedoor()
