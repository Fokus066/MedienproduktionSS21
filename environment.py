import os, bpy, random, math, add_curve_sapling

from bpy import context
from bpy.props import *

# Class for rendering the UI Panel
class Environment_Panel(bpy.types.Panel):
    bl_label = "Environment Operator"
    bl_idname = "Environment_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Create"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.environment_operator")

# Class for Operator that generates the scene
class Environment_Operator(bpy.types.Operator):

    # global definitions----------------------------------------------------
    bl_label = "Environment Operator"
    bl_idname = "wm.environment_operator"
    materials = True

    # Fix missing "bend" property in Sapling, which would otherwise prevent
    # execution of tree_add()
    add_curve_sapling.AddTree.bend = 0.0

    # Get Items from Tree Addon
    def get_presets(self, context):
        # get Sapling presets
        sapling_presets = []
        for p in add_curve_sapling.getPresetpaths():
            sapling_presets = sapling_presets + [a for a in os.listdir(p) if a[-3:] == '.py']   
        # Prepare enum item list from filenamesa
        preset_items = []
        for s in sapling_presets:
            preset_items.append((s, s, 'Use "'+s+'" as preset'))
        return preset_items  

    # UI Properties--------------------------------------------------------
    # Define class properties that will show up as UI elements on the dialog
    sunlight_enum: bpy.props.EnumProperty( name="Daytime", description="Select an option", items=[ ("OP1", "daytime",  "set daytime"), ("OP2", "night-time",  "set night-time")])
    meadow_size: IntProperty(name="Meadow size", description="Square area of meadow", default=25, min=25, max=75)

    # Define class properties that will show up as UI elements on the dialog
    presets: EnumProperty(name="Preset", description="Available sapling tree presets", items=get_presets)
    tree_number: IntProperty(name="Number of Trees", description="Number of trees that will be generated by Sapling", default=10, min=1, max=20)
    stones_number: IntProperty(name="Number of stones", description="stones will be generates randomly in the meadow", min=1, max=15)
    max_branch_levels: IntProperty(name="Maximum Branch Levels", description="Maximum branch levels to import from the preset", min = 1,default=2, max=5) 

    # leaf shape enum copied directly from Sapling.
    leaf_shape: EnumProperty(name="Leaf Shape", items=(('hex', 'Hexagonal', '0'), ('rect', 'Rectangular', '1'), ('dFace', 'DupliFaces', '2'), ('dVert', 'DupliVerts', '3')), default='rect')
    show_leaves: BoolProperty(name="Show Leaves", description="Generate leaves for all generated Saplings", default=True)

    # random floors enum for house generation
    random_floors: BoolProperty(name="Random Floors", description="Generate random number of floors of houses", default=False)

    # Show Clouds
    show_clouds: BoolProperty(name="Show Clouds", description="Generate Clouds", default=False)

    # Generate collection of trees
    create_collection: BoolProperty(name="Create Collection", description="Create a new Collection for the new randomized objects", default=True)  
    
    # Scene Objects----------------------------------------------------------------
    # Scene light definition----------------------------------------------------------------
    def light_setting(self):
        # Blender sun object
        sun_data = bpy.data.lights.new('sun', type='SUN')
        sun = bpy.data.objects.new('sun', sun_data) 
        bpy.context.collection.objects.link(sun) 
        # changing these values does affect the render.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6 
        # daytime and nighttime options
        if self.sunlight_enum == "OP1":           
            sun.data.energy = 10
            sun.data.color = (1, 1, 1)      
            sun.location = (-15,-70,45)        
            sun.rotation_euler = (0.872665, -0.349066 ,-0.261799)
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.243161, 0.887797, 1, 0.421429)
        if self.sunlight_enum == "OP2":           
            sun.data.energy = 1
            sun.data.color = (1, 1, 1)
            sun.location = (-12,44,45)   
            sun.rotation_euler = (-0.698132 , -0.610865 ,-0.436332 )
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.00824402, 0.0024832, 0.0331013, 0.421429)

    # Water Object----------------------------------------------------------------
    def generate_Water(self):
        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, 24, 0))
        water = bpy.context.active_object
        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,4,1))
        bpy.ops.object.editmode_toggle()
        # add water color
        water.data.materials.append(self.add_water_color()) 

    # definition of water color - returns material type
    def add_water_color(self) -> bpy.types.Material:
        #add material
        water_mat: bpy.types.Material = bpy.data.materials.new("Water Material")
        water_mat.use_nodes = True
        # generate node
        nodes_water: typing.List[bpy.types.Node] = water_mat.node_tree.nodes
        node_musgrav: bpy.types.Node = nodes_water.new("ShaderNodeTexMusgrave")
        node_bump: bpy.types.Node = nodes_water.new("ShaderNodeBump")
        # set node values
        node_musgrav.inputs[2].default_value = 45.000
        node_musgrav.inputs[3].default_value = 18.000
        node_musgrav.inputs[4].default_value = 45.000
        node_musgrav.inputs[5].default_value = 12.000
        node_bump.inputs[0].default_value = 0.1
        nodes_water["Principled BSDF"].inputs[0].default_value = (0.20213, 0.244409, 0.8, 1)
        nodes_water["Principled BSDF"].inputs[7].default_value = 0.05
        nodes_water["Principled BSDF"].inputs[4].default_value = 0.9
        # link different nodes
        water_mat.node_tree.links.new(node_musgrav.outputs[0], node_bump.inputs[2])
        water_mat.node_tree.links.new(node_bump.outputs[0], nodes_water["Principled BSDF"].inputs[20])
        
        return water_mat
    
    # Lantern object----------------------------------------------------------------
    def generate_lantern(self):
        # create material of latern light and stick
        light_mat = bpy.data.materials.new(name = "Light")
        black_mat = bpy.data.materials.new(name="Black")
        black_mat.diffuse_color=(0,0,0,1)
        # set node definitions
        light_mat.use_nodes = True
        nodes = light_mat.node_tree.nodes
        material_output = nodes.get("Material Output")
        node_emission = nodes.new(type='ShaderNodeEmission')
        #glow effect
        node_emission.inputs[0].default_value = (0.0, 0.1, 1.0, 1 )#colour
        node_emission.inputs[1].default_value = 500.0 #strength
        links= light_mat.node_tree.links
        links.new(node_emission.outputs[0], material_output.inputs[0])
        # spaces for generated objects
        lantern_array = []
        lantern_lights =[]
        # generate proper number of objects based on scene size
        for i in range(round((self.meadow_size/2)-1)):
            #add latern MESHES
            bpy.ops.mesh.primitive_cylinder_add(location=(-self.meadow_size + (i * 5), -19.5, 5), scale=( 0.5, 0.5, 5))
            lantern= bpy.context.active_object 
            lantern.name='lantern'.format(i) 
            lantern_array.append(lantern)
            lantern_array[i].data.materials.append(black_mat)
            #add latern_light MESHES
            bpy.ops.mesh.primitive_cylinder_add(location=(-self.meadow_size + (i * 5), -19.5, 7.8112), scale=(0.5, 0.5, 0.7))
            lantern_light= bpy.context.active_object 
            lantern_light.name='lantern'.format(i) 
            lantern_lights.append(lantern_light)
            lantern_lights[i].data.materials.append(light_mat) 
            # remove objects if they are not on the scene plane
            if lantern_array[i].location[0] > self.meadow_size or lantern_array[i].location[0] < -self.meadow_size:
                    bpy.data.objects.remove( lantern_array[i] )
                    bpy.data.objects.remove( lantern_lights[i])

        
    
    def generate_Streets(self):
        bpy.ops.mesh.primitive_plane_add()
        street1 = bpy.context.active_object
        street1.name = "street"

        #edit plane 1
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,5,1))
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.primitive_plane_add()
        street2 = bpy.context.active_object
        street2.name = "street"

        #edit plane 2
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,5,1))
        bpy.ops.object.editmode_toggle()

        #move Object
        street1.location = (0, -25,0)
        street2.location = (0, -78,0)

        #create the Material
        new_mat = bpy.data.materials.new(name = "My Material")
        street1.data.materials.append(new_mat)
        street2.data.materials.append(new_mat)

        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes

        #Operators
        principled_node = nodes.get('Principled BSDF')


        #load image to node
        # Manuel: /Users/manuelhaugg/MedienproduktionSS21/materials/street.png
        #Fokus: C:\Users\HFU\Documents\Furtwangen\Uni\Semester_5\Medienproduktion\img\street.png
        base_path = os.getcwd()
        bpy.ops.image.open(filepath="/Users/manuelhaugg/MedienproduktionSS21/materials/street.png")
        my_image_node = nodes.new("ShaderNodeTexImage")
        my_image_node.image = bpy.data.images["street.png"]
        
        #linking the nodes
        links = new_mat.node_tree.links
        links.new(my_image_node.outputs[0], principled_node.inputs[0])

    def generate_pavement(self):

        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, -31.5, 0))
        
        pavement = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,1.5,1))
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

    def meadow_color(self )-> bpy.types.Material:        

        #add material
        material = bpy.data.materials.new("grass")
        material.diffuse_color = (0.029, 0.107, 0.03, 42) # darkish green
        material.roughness = 0.4
        material.specular_intensity = 0.5

        return material    

    def generate_meadow(self):

        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0),scale=(self.meadow_size,20,0))
        meadow = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,20,0))
        bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.primitive_plane_add(location=(0, -53, 0),scale=(self.meadow_size,20,0))
        meadow_house_side = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,20,0))
        bpy.ops.object.editmode_toggle()

        meadow_all = [meadow,meadow_house_side]        

        for i in range(len(meadow_all)):

            ps = meadow_all[i].modifiers.new("grasshair", 'PARTICLE_SYSTEM')
            ptcsys = meadow_all[i].particle_systems[ps.name]
            ptcsys.settings.count = 15000 *self.meadow_size
            ptcsys.settings.type = 'HAIR'
            ptcsys.settings.hair_length = 0.3
            ptcsys.settings.brownian_factor = 0.3
            ptcsys.settings.hair_step = 1

            meadow_all[i].data.materials.append(self.meadow_color()) 

    # set some defaults before popping up the dialog, then pop up the dialog
    def invoke(self, context, event):
        self.tree_number = 10
        self.leaf_shape='hex'
        self.stones_number = 10
        self.create_collection = True

        return context.window_manager.invoke_props_dialog(self)

    def generate_lantern(self):

        #create Material
        new_mat = bpy.data.materials.new(name = "My Material")
        black_mat = bpy.data.materials.new(name="Black")
        black_mat.diffuse_color=(0,0,0,1)
    
        new_mat.use_nodes = True
        nodes = new_mat.node_tree.nodes
        material_output = nodes.get("Material Output")
        node_emission = nodes.new(type='ShaderNodeEmission')

        #glow effect
        node_emission.inputs[0].default_value = (0.0, 0.1, 1.0, 1 )#colour
        node_emission.inputs[1].default_value = 500.0 #strength

        links= new_mat.node_tree.links
        links.new(node_emission.outputs[0], material_output.inputs[0])

        lantern_array = []
        lantern_lights =[]

        for i in range(round((self.meadow_size/2)-1)):
            bpy.ops.mesh.primitive_cylinder_add(location=(-self.meadow_size + (i * 15), -30, 5), scale=( 0.5, 0.5, 10))
            lantern= bpy.context.active_object 
            lantern.name='lantern'.format(i) 
            lantern_array.append(lantern)
            lantern_array[i].data.materials.append(black_mat)

            bpy.ops.mesh.primitive_cylinder_add(location=(-self.meadow_size + (i * 15), -30, 10.34), scale=(0.5, 0.5, 0.7))
            lantern_light= bpy.context.active_object 
            lantern_light.name='lantern'.format(i) 
            lantern_lights.append(lantern_light)
            lantern_lights[i].data.materials.append(new_mat)            

            if lantern_array[i].location[0] > self.meadow_size or lantern_array[i].location[0] < -self.meadow_size:
                bpy.data.objects.remove( lantern_array[i] )
                bpy.data.objects.remove( lantern_lights[i] )           


    def stone_material(self) -> bpy.types.Material:

        stone_mat: bpy.types.Material = bpy.data.materials.new("stones texture")
        stone_mat.use_nodes = True

        nodes_stone: typing.List[bpy.types.Node] = stone_mat.node_tree.nodes
        node_musgrav: bpy.types.Node = nodes_stone.new("ShaderNodeTexMusgrave")
        node_texcoord: bpy.types.Node = nodes_stone.new("ShaderNodeTexCoord")
        node_bump: bpy.types.Node = nodes_stone.new("ShaderNodeBump")
        node_noise: bpy.types.Node = nodes_stone.new("ShaderNodeTexNoise")
        node_mix: bpy.types.Node = nodes_stone.new("ShaderNodeMixRGB")
        node_colorramp_1: bpy.types.Node = nodes_stone.new("ShaderNodeValToRGB")
        node_colorramp_2: bpy.types.Node = nodes_stone.new("ShaderNodeValToRGB")
                
        node_mapping: bpy.types.Node = nodes_stone.new("ShaderNodeMapping")

        node_mix.blend_type = 'DIFFERENCE'
        node_bump.inputs[0].default_value = 0.4
        node_musgrav.inputs[2].default_value = .8
        node_musgrav.inputs[3].default_value = 3.300
        node_musgrav.inputs[4].default_value = 16.000
        node_noise.inputs[2].default_value = 2.000
        node_noise.inputs[3].default_value = 1.000
        node_noise.inputs[4].default_value = 0.1
        node_noise.inputs[5].default_value = 4.0

        node_colorramp_1.color_ramp.elements[0].color = (0.157482, 0.14257, 0.140865, 1)
        node_colorramp_1.color_ramp.elements[1].color =  (0.013177, 0.013177, 0.013177, 1)

        node_colorramp_2.color_ramp.elements[1].color =  (0.0406683, 0.0406683, 0.0406683, 1)
        node_colorramp_2.color_ramp.elements[0].color = (0.117462, 0.117462, 0.117462, 1)
        
        stone_mat.node_tree.links.new(node_texcoord.outputs[3], node_mapping.inputs[0])

        stone_mat.node_tree.links.new(node_mapping.outputs[0],node_musgrav.inputs[0])
        stone_mat.node_tree.links.new(node_mapping.outputs[0],node_noise.inputs[0])

        stone_mat.node_tree.links.new(node_musgrav.outputs[0],node_mix.inputs[1])

        stone_mat.node_tree.links.new(node_noise.outputs[0],node_colorramp_1.inputs[0])
        stone_mat.node_tree.links.new(node_colorramp_1.outputs[0], node_mix.inputs[2])

        stone_mat.node_tree.links.new( node_mix.outputs[0],node_colorramp_2.inputs[0])
        stone_mat.node_tree.links.new( node_mix.outputs[0],node_bump.inputs[2])

        stone_mat.node_tree.links.new( node_colorramp_2.outputs[0], nodes_stone["Principled BSDF"].inputs[0])
        stone_mat.node_tree.links.new( node_bump.outputs[0], nodes_stone["Principled BSDF"].inputs[20])

        return stone_mat
    
    def generate_stones(self):

       # get window_manager context to make updating the progress indicator less code
        Window_Manager = bpy.context.window_manager
                
        # get list of current objects
        objects_before = bpy.data.objects.values()
                
        # start progress indicator
        Window_Manager.progress_begin(0,10)

        for index in range(0, self.stones_number):          
                            
            # run the actual tree generating code
            bpy.ops.mesh.primitive_cube_add()
            
            stone = bpy.context.object
            stone.name = "stone"

            stone_subsurf = stone.modifiers.new("stone structure", "SUBSURF")
            stone_subsurf.levels = 4

            bpy.ops.object.modifier_add(type='DISPLACE')

            # Generate the texture and set the attributes
            voronoi_tex = bpy.data.textures.new("displace_voronoi", 'VORONOI')
            voronoi_tex.noise_intensity = .67
            voronoi_tex.noise_scale = round(random.uniform(0.77, 1.3))
            voronoi_tex.contrast = .22

            # Displacement modifier
            disp_mod = None
            for modifier in stone.modifiers:
                if modifier.type == 'DISPLACE':
                    disp_mod = modifier        

            if not disp_mod:
                disp_mod = stone.modifiers.new(name='MyVoronoiDisplace', type='DISPLACE')

            # Assign the texture
            disp_mod.texture = voronoi_tex
            disp_mod.strength = 5
            disp_mod.vertex_group = "Group"
                                    
            # update the progress indicator after each tree
            Window_Manager.progress_update(index)
                
            # tell the progress indicator we're finished
            Window_Manager.progress_end()

        objects_next = bpy.data.objects.values()
        newobjects = [object for object in objects_next if object not in objects_before]   

        # also prepare a list of potentially joined meshes
        for obj in newobjects:

            #some operators require selections, so first deselect everything
            bpy.ops.object.select_all(action='DESELECT')

            obj.rotation_euler[0] = random.uniform(0.1, 5.0)
            obj.rotation_euler[1] = random.uniform(0.1, 5.0)
            obj.scale = (random.randrange(1, 3),random.randrange(1, 3),1)    

            x = random.randrange(-self.meadow_size, self.meadow_size)
            y = random.randrange(-20, 20)
                                                    
            obj.location = (x, y, 1)
            obj.data.materials.append(self.stone_material())

        newcol = bpy.data.collections.new("stones collections: ")
        bpy.context.scene.collection.children.link(newcol)

        # move new objects into collection
        for objref in newobjects:
            # link new object to new collection
            newcol.objects.link(objref)

        
    def generate_trees(self):

         # get window_manager context to make updating the progress indicator less code
        Window_Manager = bpy.context.window_manager
        
        # get list of current objects
        objects_before = bpy.data.objects.values()
         
        # start progress indicator
        Window_Manager.progress_begin(0, self.tree_number)

        # generate a number of trees
        for index in range(0, self.tree_number):            
                        
            # use Sapling's own ImportData class to read the preset files into the "settings" list
            add_curve_sapling.ImportData.filename = self.presets
            add_curve_sapling.ImportData.execute(add_curve_sapling.ImportData, bpy.context)
            
            # have to override the preset values after reading them
            if add_curve_sapling.settings["levels"] > self.max_branch_levels:
                add_curve_sapling.settings["levels"] =  self.max_branch_levels
            add_curve_sapling.settings["branchDist"] = round(random.uniform(0.1, 10.00), 2)
            add_curve_sapling.settings["nrings"] = random.randint(7,10)
            add_curve_sapling.settings["seed"] = random.randint(7,10)
            add_curve_sapling.settings["limitImport"] = False
            add_curve_sapling.settings["do_update"] = True
            add_curve_sapling.settings["bevel"] = True
            add_curve_sapling.settings["prune"] = False
            add_curve_sapling.settings["showLeaves"] = self.show_leaves
            add_curve_sapling.settings["leafShape"] = self.leaf_shape
            add_curve_sapling.settings["useArm"] = False
            add_curve_sapling.settings["leaves"]  = random.randrange(250, 500) 
            add_curve_sapling.settings["scale"]  = random.randint(5,10)         
            # run the actual tree generating code
            obj = bpy.ops.curve.tree_add(
                limitImport=False,
                do_update=True,
                bevel=True,
                prune=False,
                showLeaves=self.show_leaves,
                leafShape=self.leaf_shape,
                useArm=False,
            )
            # update the progress indicator after each tree
            Window_Manager.progress_update(index)
        
        # tell the progress indicator we're finished
        Window_Manager.progress_end()
            
        # set up basic materials
        if self.materials:
            # trunk
            trunk_material = bpy.data.materials.new("Sapling Trunk")
            trunk_material.diffuse_color = (0.064, 0.001, 0.001, 25) # dark brown
            trunk_material.roughness = 5.0
            trunk_material.specular_intensity = 1.0
            
            # leaves
            leaf_material = bpy.data.materials.new("Sapling Leaves")
            leaf_material.diffuse_color = (0.034, 0.089, 0.058, 35) # darkish green
            leaf_material.roughness = 0.4
            leaf_material.specular_intensity = 0.5

        # since we cannot tell Sapling where to put its new trees, we have to iterate through all new "tree" objects
        # and move them randomly after generating them
        
        # make object list after generating
        objects_next = bpy.data.objects.values()
        newobjects = [object for object in objects_next if object not in objects_before]     

        # also prepare a list of potentially joined meshes
        for obj in newobjects:
            
            # some operators require selections, so first deselect everything
            bpy.ops.object.select_all(action='DESELECT')
            
            # process trunks
            if obj.type == 'CURVE':

                x = random.randrange(-self.meadow_size, self.meadow_size)
                y = random.randrange(-20, 20)
                                                         
                obj.location = (x, y, 0)
                    
                if self.materials:
                    obj.data.materials.append(trunk_material)            
            
            # leaves
            if obj.type == 'MESH' and self.materials:
                obj.data.materials.append(leaf_material)
         
        if self.create_collection:
            # make new collection
            newcol = bpy.data.collections.new("Environment collections: ")
            bpy.context.scene.collection.children.link(newcol)

            # move new objects into collection
            for objref in newobjects:
                # link new object to new collection
                newcol.objects.link(objref)
                # remove object from scene collection
                bpy.context.scene.collection.objects.unlink(objref)

    def add_fence_texture_vertical(self) -> bpy.types.Material:

        #add material
        fence_mat: bpy.types.Material = bpy.data.materials.new("fence material")
        fence_mat.use_nodes = True

        nodes_fence: typing.List[bpy.types.Node] = fence_mat.node_tree.nodes
        node_musgrave: bpy.types.Node = nodes_fence.new("ShaderNodeTexMusgrave")
        node_texvoronoi: bpy.types.Node = nodes_fence.new("ShaderNodeTexVoronoi")
        node_texnoise: bpy.types.Node = nodes_fence.new("ShaderNodeTexNoise")

        node_texnoise.inputs[4].default_value = 1   
        nodes_fence["Principled BSDF"].inputs[0].default_value = (0.455477, 0.463941, 0.489882, 1)
        nodes_fence["Principled BSDF"].inputs[5].default_value = 0
        nodes_fence["Principled BSDF"].inputs[7].default_value = 0.9
        fence_mat.node_tree.links.new(node_musgrave.outputs[0], node_texvoronoi.inputs[0])
        fence_mat.node_tree.links.new(node_texvoronoi.outputs[0], nodes_fence["Principled BSDF"].inputs[4])
        fence_mat.node_tree.links.new(node_texnoise.outputs[0], nodes_fence["Material Output"].inputs[2])
        
        return fence_mat

    def add_fence_texture_horizontal(self) -> bpy.types.Material:

        #add material
        fence_mat: bpy.types.Material = bpy.data.materials.new("fence material")
        fence_mat.use_nodes = True

        nodes_fence: typing.List[bpy.types.Node] = fence_mat.node_tree.nodes
        node_musgrave: bpy.types.Node = nodes_fence.new("ShaderNodeTexMusgrave")
        node_texvoronoi: bpy.types.Node = nodes_fence.new("ShaderNodeTexVoronoi")
        node_texnoise: bpy.types.Node = nodes_fence.new("ShaderNodeTexNoise")

        node_texnoise.inputs[4].default_value = 1   
        nodes_fence["Principled BSDF"].inputs[0].default_value = (0.0187184, 0.00194077, 0.00739711, 1)
        nodes_fence["Principled BSDF"].inputs[5].default_value = 0
        nodes_fence["Principled BSDF"].inputs[7].default_value = 0.9

        fence_mat.node_tree.links.new(node_musgrave.outputs[0], node_texvoronoi.inputs[0])
        fence_mat.node_tree.links.new(node_texvoronoi.outputs[0], nodes_fence["Principled BSDF"].inputs[4])
        fence_mat.node_tree.links.new(node_texnoise.outputs[0], nodes_fence["Material Output"].inputs[2])
        
        return fence_mat


    def generate_fence(self):

        fence_z = 10

        fence_scale_y = 0.2
        fence_scalet_z = 0.95

        fence_vertical_z = 5

        fence_vertical_scale_x = 0.8
        fence_vertical_scale_y = 0.6
        fence_vertical_scalet_z = 5

        fences_horinzontal = []

        fences_vertical = []

        for i in range(round((self.meadow_size/2)-1)):
            bpy.ops.mesh.primitive_cube_add(location=(-self.meadow_size + (i * 5), -33, fence_vertical_z*0.5), scale=(fence_vertical_scale_x, fence_vertical_scale_y, fence_vertical_scalet_z))
            fence= bpy.context.active_object 
            fence.name = "fence_vertical".format(i) 
            fences_vertical.append(fence)
            fences_vertical[i].data.materials.append(self.add_fence_texture_vertical())
            if fences_vertical[i].location[0] > self.meadow_size or fences_vertical[i].location[0] < -self.meadow_size:
                bpy.data.objects.remove( fences_vertical[i] )

        for i in range(2):
            bpy.ops.mesh.primitive_cube_add(location=(0, -33,  (fence_z/2.5) - (2 * i)), scale=(self.meadow_size*2, fence_scale_y, fence_scalet_z))
            fence= bpy.context.active_object
            fence.name = "fence_horinzontal".format(i)  
            fences_horinzontal.append(fence)
            fences_horinzontal[i].data.materials.append(self.add_fence_texture_horizontal())   

    def cloud_material(self) -> bpy.types.Material:

        cloud_mat: bpy.types.Material = bpy.data.materials.new("clouds texture")
        cloud_mat.use_nodes = True
        
        #Get the node in its node tree (replace the name below)
        node_to_delete =  cloud_mat.node_tree.nodes['Principled BSDF']
        node_material =  cloud_mat.node_tree.nodes['Material Output']

        #Remove it
        cloud_mat.node_tree.nodes.remove( node_to_delete )
        cloud_mat.node_tree.nodes.remove( node_material)

        nodes_cloud: typing.List[bpy.types.Node] = cloud_mat.node_tree.nodes
        node_math: bpy.types.Node = nodes_cloud.new("ShaderNodeMath")
        node_colorramp: bpy.types.Node = nodes_cloud.new("ShaderNodeValToRGB")
        node_noise_1: bpy.types.Node = nodes_cloud.new("ShaderNodeTexNoise")
        node_noise_2: bpy.types.Node = nodes_cloud.new("ShaderNodeTexNoise")
        node_mix: bpy.types.Node = nodes_cloud.new("ShaderNodeMixRGB")
        node_texcoord: bpy.types.Node = nodes_cloud.new("ShaderNodeTexCoord")         
        node_mapping: bpy.types.Node = nodes_cloud.new("ShaderNodeMapping")
        node_volume: bpy.types.Node = nodes_cloud.new("ShaderNodeVolumePrincipled")
        node_matoutput: bpy.types.Node = nodes_cloud.new("ShaderNodeOutputMaterial")

        node_volume.inputs[0].default_value = (1, 1, 1, 1)

        node_math.operation = 'MULTIPLY'
        node_math.inputs[1].default_value = 1000

        node_colorramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        node_colorramp.color_ramp.elements[0].position = 0.709
        node_colorramp.color_ramp.elements[1].color = (1, 1, 1, 1)

        node_noise_1.inputs[5].default_value = 2

        node_noise_1.inputs[2].default_value = 2.4
        node_noise_2.inputs[2].default_value = 2.4

        node_mix.blend_type = 'MIX'
        node_mix.inputs[0].default_value = 0.8

        cloud_mat.node_tree.links.new(node_colorramp.outputs[0], node_math.inputs[0])
        cloud_mat.node_tree.links.new(node_noise_1.outputs[0], node_colorramp.inputs[0])
        cloud_mat.node_tree.links.new(node_mix.outputs[0], node_noise_1.inputs[0])
        cloud_mat.node_tree.links.new(node_mapping.outputs[0], node_mix.inputs[1])
        
        cloud_mat.node_tree.links.new(node_noise_2.outputs[1], node_mix.inputs[2])
        cloud_mat.node_tree.links.new(node_texcoord.outputs[3], node_mapping.inputs[0])
        
        cloud_mat.node_tree.links.new(node_texcoord.outputs[3], node_noise_2.inputs[0])
        cloud_mat.node_tree.links.new( node_math.outputs[0], node_volume.inputs[2])
        cloud_mat.node_tree.links.new( node_volume.outputs[0], node_matoutput.inputs[1])

        return cloud_mat

    def generate_clouds(self):

        # run the actual tree generating code
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 35),scale=(self.meadow_size*2,50, 3))
        cloud1 = bpy.context.object
        bpy.ops.mesh.primitive_cube_add(location=(0, -53, 35),scale=(self.meadow_size*2,50, 3))
        cloud2= bpy.context.object
                    
        cloud1.name = "cloud"
        cloud2.name = "cloud"

        cloud1.data.materials.append(self.cloud_material())
        cloud2.data.materials.append(self.cloud_material())    

    def generate_houses(self):
        house_size_x = 20
        house_size_y = 15
        house_size_z = 10

        house_loc_y = -53
        house_loc_x = 5
        house_loc_z = house_size_z * 0.5

        garage_size_x = 12
        garage_size_y = 15
        garage_size_z = 6

        garage_loc_y = -53
        garage_loc_x = house_loc_x - house_size_x * 0.75
        garage_loc_z = garage_size_z * 0.5

        ground_size_x = 21
        ground_size_y = 31
        ground_size_z = 1

        ground_loc_x = -2.75
        ground_loc_y = -63
        ground_loc_z = 0.95

        if self.meadow_size >= 50 and self.meadow_size < 75:
            number_houses = 2
        elif self.meadow_size is 75:
            number_houses = 3
        else:
            number_houses = 1

        diff = self.meadow_size - 25

        for i in range(number_houses):
                bpy.ops.mesh.primitive_cube_add(location=(-self.meadow_size/2  + (i * 50), house_loc_y, house_loc_z),scale=(house_size_x, house_size_y, house_size_z))
                house = bpy.context.object
                house.rotation_euler = (0 , 0 ,1.5708 )

                bpy.ops.mesh.primitive_cube_add(location=(-self.meadow_size/2 +  (i * 50) -15, garage_loc_y, garage_loc_z),scale=(garage_size_x, garage_size_y, garage_size_z))
                garage = bpy.context.object
                garage.rotation_euler = (0 , 0 ,1.5708 )

                bpy.ops.mesh.primitive_cube_add(location=(-self.meadow_size/2 +  (i * 50) -7, ground_loc_y, ground_loc_z),scale=(ground_size_x, ground_size_y, ground_size_z))
                ground = bpy.context.object
                ground.rotation_euler = (0 , 0 ,1.5708 )
          
    
    # Run the actual code upon pressing "OK" on the dialog
    def execute(self, context):

        bpy.ops.object.select_all(action='SELECT') # selektiert alle Objekte
        bpy.ops.object.delete(use_global=False, confirm=False) # löscht selektierte objekte
        bpy.ops.outliner.orphans_purge() # löscht überbleibende Meshdaten etc.
        bpy.ops.object.select_all(action='DESELECT')

        main_house = House()
        second_house = House()
        third_house = House()

        if self.meadow_size > 25:
            diff = self.meadow_size - 25
            main_house.house_loc_x = main_house.house_loc_x - diff
            main_house.garage_loc_x = main_house.garage_loc_x-diff
            main_house.ground_loc_x = main_house.ground_loc_x-diff


        #main_house.generate_obj()
        
        if self.meadow_size >= 50 and self.meadow_size <= 75:
            factor = 50
            second_house.house_loc_x = main_house.house_loc_x + factor
            second_house.garage_loc_x = main_house.house_loc_x + factor - 15
            second_house.ground_loc_x = main_house.house_loc_x + factor - 7.5
            #second_house.generate_obj()
            if self.meadow_size is 75:
                third_house.house_loc_x = second_house.house_loc_x + factor
                third_house.garage_loc_x = second_house.house_loc_x + factor - 15
                third_house.ground_loc_x = second_house.house_loc_x + factor - 7.5
                #third_house.generate_obj()

        self.generate_houses()
        self.generate_fence()
        self.generate_meadow()
        self.generate_Water()
        self.generate_Streets()
        self.light_setting()
        self.generate_pavement()
        self.generate_trees()  
        self.generate_stones()
        self.generate_lantern()
        if self.show_clouds is True:
            self.generate_clouds()
        
        return {'FINISHED'}

class House:

    house_size_x = 20
    house_size_y = 15
    house_size_z = 10

    house_loc_y = -53
    house_loc_x = 5
    house_loc_z = house_size_z * 0.5

    garage_size_x = 12
    garage_size_y = 15
    garage_size_z = 6

    garage_loc_y = -53
    garage_loc_x = house_loc_x - house_size_x * 0.75
    garage_loc_z = garage_size_z * 0.5

    ground_size_x = 21
    ground_size_y = 31
    ground_size_z = 1

    ground_loc_x = -2.75
    ground_loc_y = -63
    ground_loc_z = 0.95

    def generate_obj(self):

        bpy.ops.mesh.primitive_cube_add(location=(self.house_loc_x, self.house_loc_y, self.house_loc_z),scale=(self.house_size_x, self.house_size_y, self.house_size_z))
        house = bpy.context.object
        house.rotation_euler = (0 , 0 ,1.5708 )

        bpy.ops.mesh.primitive_cube_add(location=(self.garage_loc_x, self.garage_loc_y, self.garage_loc_z),scale=(self.garage_size_x, self.garage_size_y, self.garage_size_z))
        garage = bpy.context.object
        garage.rotation_euler = (0 , 0 ,1.5708 )

        bpy.ops.mesh.primitive_cube_add(location=(self.ground_loc_x, self.ground_loc_y, self.ground_loc_z),scale=(self.ground_size_x, self.ground_size_y, self.ground_size_z))
        ground = bpy.context.object
        ground.rotation_euler = (0 , 0 ,1.5708 )

        





classes = [Environment_Panel,Environment_Operator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
