import bpy, typing
import bmesh 

class house: 


    number_of_floors = 2

    groundX = 20
    groundY= 30
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

        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(30, 0,  self.housemainZ * 0.5), scale=(self.housemainX, self.housemainY,self.housemainZ))

        
        if  self.number_of_floors == 2:
            #extrudien
            bpy.ops.object.mode_set( mode   = 'EDIT'   )
            bpy.ops.mesh.select_mode( type  = 'FACE'   )
            bpy.ops.mesh.select_all( action = 'SELECT' )

            bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, 8)})

        else:
            bpy.ops.object.mode_set( mode   = 'EDIT'   )
            bpy.ops.mesh.select_mode( type  = 'FACE'   )
            bpy.ops.mesh.select_all( action = 'SELECT' )

            bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value":(0, 0, 3)})
            

 
        bpy.ops.object.mode_set( mode = 'OBJECT' )
             # extrudieren Face skalieren (ops transforn resize auf einer achse) 
        mainhouse = bpy.context.object
        mainhouse.name = "mainhouse"
        mainhouse.data.materials.append(self.building_material()) 



        #Garage
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=( bpy.data.objects['mainhouse'].location.x+3.96 , bpy.data.objects['mainhouse'].location.y+15, bpy.data.objects['mainhouse'].location.z-2), scale=(self.garageX, self.garageY, self.garageZ))

        garage = bpy.context.object
        garage.data.materials.append(self.building_material()) 

       


        door1 = bpy.ops.mesh.primitive_cube_add(scale=(self.door_size_x, self.door_size_y, self.door_size_z),location=(  bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y, bpy.data.objects['mainhouse'].location.z-3))
       
        

        patio1 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_y, self.patio_size_x, self.patio_size_z),location=(  bpy.data.objects['mainhouse'].location.x-5 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z-3))
        patio2 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_x, self.patio_size_y, self.patio_size_z),location=( bpy.data.objects['mainhouse'].location.x-10 , bpy.data.objects['mainhouse'].location.y+4.95, bpy.data.objects['mainhouse'].location.z-3))
        patio3 = bpy.ops.mesh.primitive_cube_add(scale=(self.patio_size_y, self.patio_size_x, self.patio_size_z),location=( bpy.data.objects['mainhouse'].location.x+3 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+3))

        garagedoor1 = bpy.ops.mesh.primitive_cube_add(scale=(self.garagedoor_size_x, self.garagedoor_size_y, self.garagedoor_size_z),location=(  bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y+15, bpy.data.objects['mainhouse'].location.z-3))
        garage = bpy.context.object
        garage.name = "garage"
        # objects = bpy.data.objects
        # a = objects['mainhouse']
        # b = objects['garage']
        # a.parent = b

    

    def generate_ground(self):
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(bpy.data.objects['mainhouse'].location.x+20, bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z-5.0), scale=(self.groundX, self.groundY, self.groundZ))
        
        ground = bpy.context.object
        ground.name = "ground"
        new_mat = bpy.data.materials.new(name = "Wood Floor")
        ground.data.materials.append(new_mat)

        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

            #Operators
        principled_node = nodes.get('Principled BSDF')

            #load image to node
            # Manuel: /Users/manuelhaugg/MedienproduktionSS21/materials/street.png
        bpy.ops.image.open(filepath="/Users/Vinzenz/Documents/MedienProd/Materials/Boden/granite.jpg")
        my_image_node = nodes.new("ShaderNodeTexImage")
        my_image_node.image = bpy.data.images["granite.jpg"]
        #new_mat = bpy.data.materials.new(name = "Wood Floor")
            #linking the nodes
        links = new_mat.node_tree.links
        links.new(my_image_node.outputs[0], principled_node.inputs[0])    

        



    def generate_Window(self):

        windows_size_x = 0.5
        windows_size_y = 3
        windows_size_z = 3

        sidewindows_size_x = 3
        sidewindows_size_y = 0.5
        sidewindows_size_z = 3
        
        
        window1 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x-10 , bpy.data.objects['mainhouse'].location.y+3.75, bpy.data.objects['mainhouse'].location.z+4))
        window2 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=(  bpy.data.objects['mainhouse'].location.x-10 , bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z+4))
        window3 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x-10 , bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z))


        window4 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x-6.6 , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+4))
        window5 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x+0, bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+4))
        window6 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x+6.6, bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+4))
        window7 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x-6.6, bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z))        
        window8 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z))
        window9 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=( bpy.data.objects['mainhouse'].location.x+6.6 , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z))
       
        window11 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z+4))
        window12 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y+3.75, bpy.data.objects['mainhouse'].location.z+4))
        window13 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z))
        window14 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=( bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y +3.75, bpy.data.objects['mainhouse'].location.z))

        window15 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x -1 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+4))
        window16 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x+7.2 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+4))
        


        windows = [window1,window2,window3,window4,window5,window6,window7,window8,window9,window11,window12,window13,window14,window15,window16]
        windows = bpy.context.object
        windows.name = "windows"

        


        if  self.number_of_floors == 2:

            
            window17 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=(bpy.data.objects['mainhouse'].location.x-10 , bpy.data.objects['mainhouse'].location.y+3.75, bpy.data.objects['mainhouse'].location.z+9))
            window18 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=(bpy.data.objects['mainhouse'].location.x-10, bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z+9))

            window19 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x-6.6 , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+9))
            window20 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x+0 , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+9))
            window21 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x+6.6 , bpy.data.objects['mainhouse'].location.y-7.5, bpy.data.objects['mainhouse'].location.z+9))

            window22 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x+6.6 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+9))
            window23 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x+0 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+9))
            window24 = bpy.ops.mesh.primitive_cube_add(scale=(sidewindows_size_x, sidewindows_size_y, sidewindows_size_z),location=(bpy.data.objects['mainhouse'].location.x-6.6 , bpy.data.objects['mainhouse'].location.y+7.5, bpy.data.objects['mainhouse'].location.z+9))

            window25 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=(bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y-3.75, bpy.data.objects['mainhouse'].location.z+9))
            window26 = bpy.ops.mesh.primitive_cube_add(scale=(windows_size_x, windows_size_y, windows_size_z),location=(bpy.data.objects['mainhouse'].location.x+10 , bpy.data.objects['mainhouse'].location.y+3.75, bpy.data.objects['mainhouse'].location.z+9))

            
            windows = [window17,window18,window19,window20,window21,window22,window23,window24,window25,window26]

            
       
            
            

            
        # for i in range(len(windows)): 
        #     windows[i].data.materials.append(new_mat)

        #     new_mat.use_nodes = True
        #     nodes = new_mat.node_tree.nodes

        #     #Operators
        #     principled_node = nodes.get('Principled BSDF')

        #     #load image to node
        #     # Manuel: /Users/manuelhaugg/MedienproduktionSS21/materials/street.png
        #     bpy.ops.image.open(filepath="Users/Vinzenz/Documents/MedienProd/Materials/Holzboden/WoodFloor047_1K_Color.jpg")
        #     my_image_node = nodes.new("ShaderNodeTexImage")
        #     my_image_node.image = bpy.data.images["WoodFloor047_1K_Color.jpg"]
            
        #     #linking the nodes
        #     links = new_mat.node_tree.links
        #     links.new(my_image_node.outputs[0], principled_node.inputs[0]) 
        # windows
        # print(windows)      



house= house()
house.generate_building()
house.generate_Window()
house.generate_ground()
#house.generate_Garagedoor()