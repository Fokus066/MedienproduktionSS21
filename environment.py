import os, bpy, random, math, add_curve_sapling
from bpy.props import *

class Environment_Panel(bpy.types.Panel):
    bl_label = "Environment Operator"
    bl_idname = "Environment_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Create"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("wm.environment_operator")
 
class Environment_Operator(bpy.types.Operator):
    bl_label = "Environment Operator"
    bl_idname = "wm.environment_operator"
    
    distance_relative = True
    materials= True
    
    # Fix missing "bend" property in Sapling, which would otherwise prevent
    # execution of tree_add()
    add_curve_sapling.AddTree.bend = 0.0

    def getPresets(self, context):
        # get Sapling presets
        sapling_presets = []
        for p in add_curve_sapling.getPresetpaths():
            sapling_presets = sapling_presets + [a for a in os.listdir(p) if a[-3:] == '.py']
                
        # Prepare enum item list from filenamesa
        preset_items = []
        for s in sapling_presets:
            preset_items.append((s, s, 'Use "'+s+'" as preset'))
        return preset_items  

    # Define class properties that will show up as UI elements on the dialog
    sunlight_enum: bpy.props.EnumProperty( name="Daytime", description="Select an option", items=[ ("OP1", "daytime",  "set daytime"), ("OP2", "night-time",  "set night-time")])
    meadow_size: IntProperty(name="Meadow size", description="Square area of meadow", default=20, min=1, max=50)

    # Define class properties that will show up as UI elements on the dialog
    presets: EnumProperty(name="Preset", description="Available sapling tree presets", items=getPresets)
    tree_number: IntProperty(name="Number of Trees", description="Number of trees that will be generated by Sapling", default=10, min=1, max=15)
    distance: FloatProperty(name="Distance", description="Area in which Saplings will be created", unit='LENGTH', min=1, max=5)
    max_branch_levels: IntProperty(name="Maximum Branch Levels", description="Maximum branch levels to import from the preset", min = 1,default=2, max=5) 

    # leaf shape enum copied directly from Sapling.
    leaf_shape: EnumProperty(name="Leaf Shape", items=(('hex', 'Hexagonal', '0'), ('rect', 'Rectangular', '1'), ('dFace', 'DupliFaces', '2'), ('dVert', 'DupliVerts', '3')), default='rect')
    show_leaves: BoolProperty(name="Show Leaves", description="Generate leaves for all generated Saplings", default=True)

    def light_setting(self):

        sun_data = bpy.data.lights.new('sun', type='SUN')
        sun = bpy.data.objects.new('sun', sun_data)
        sun.location = (5,-5,30)
        

        bpy.context.collection.objects.link(sun) 

        # changing these values does affect the render.
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.6 
      
        if self.sunlight_enum == "OP1":           
            sun.data.energy = 10
            sun.data.color = (0.939978, 1, 0.355009)
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.243161, 0.887797, 1, 0.421429)
    
        if self.sunlight_enum == "OP2":           
            sun.data.energy = 1
            sun.data.color = (1, 1, 1)
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.00824402, 0.0024832, 0.0331013, 0.421429)

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
    
    def generate_Water(self):

        # add plane
        bpy.ops.mesh.primitive_plane_add(location=(0, self.meadow_size + 4, 0))

        ob = bpy.context.active_object

        #edit plane
        bpy.ops.object.editmode_toggle()
        bpy.ops.transform.resize(value=(self.meadow_size,4,1))
        #bpy.ops.mesh.subdivide(number_cuts=7)
        bpy.ops.object.editmode_toggle()
        
        ob.data.materials.append(self.add_water_color()) 

    def meadow_color(self )-> bpy.types.Material:        

        #add material
        material = bpy.data.materials.new("grass")
        material.diffuse_color = (0.029, 0.107, 0.03, 42) # darkish green
        material.roughness = 0.4
        material.specular_intensity = 0.5

        return material    

    def generate_meadow(self):

            # add plane
            bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))

            ob = bpy.context.active_object

            #edit plane
            bpy.ops.object.editmode_toggle()
            bpy.ops.transform.resize(value=(self.meadow_size,self.meadow_size,0))
            bpy.ops.mesh.subdivide(number_cuts=7)
            bpy.ops.object.editmode_toggle()


            #particle system
            ps = ob.modifiers.new("grasshair", 'PARTICLE_SYSTEM')

            ptcsys = ob.particle_systems[ps.name]
            ptcsys.settings.count = 15000 *self.meadow_size
            ptcsys.settings.type = 'HAIR'
            ptcsys.settings.hair_length = 0.3
            ptcsys.settings.brownian_factor = 0.3
            ptcsys.settings.hair_step = 1
            
            #add material to object
            ob.data.materials.append(self.meadow_color()) 

    # Generate collection of trees
    create_collection: BoolProperty(name="Create Collection", description="Create a new Collection for the new randomized objects", default=True)   

    # set some defaults before popping up the dialog, then pop up the dialog
    def invoke(self, context, event):
        self.tree_number = 10
        self.leaf_shape='hex'
        self.distance_relative = True
        self.distance = 2.0
        self.create_collection = True
        return context.window_manager.invoke_props_dialog(self)
    
    # Run the actual code upon pressing "OK" on the dialog
    def execute(self, context):

        self.generate_meadow()
        self.light_setting()
        self.generate_Water()
        
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
                add_curve_sapling.settings["levels"] = self.max_branch_levels
            add_curve_sapling.settings["limitImport"] = False
            add_curve_sapling.settings["do_update"] = True
            add_curve_sapling.settings["bevel"] = True
            add_curve_sapling.settings["prune"] = False
            add_curve_sapling.settings["showLeaves"] = self.show_leaves
            add_curve_sapling.settings["leafShape"] = self.leaf_shape
            add_curve_sapling.settings["useArm"] = False
            
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
        
        # "distance" will be relative 
        distance = math.sqrt(random.randint(1, 100))*(random.randint(1,3)*self.tree_number)/self.distance

        # also prepare a list of potentially joined meshes
        for obj in newobjects:
            
            # some operators require selections, so first deselect everything
            bpy.ops.object.select_all(action='DESELECT')
            
            # process trunks
            if obj.type == 'CURVE':
                cursor = bpy.context.scene.cursor.location
                x = (random.random() * self.meadow_size) - self.meadow_size/2 + cursor[0] 
                y = (random.random() * self.meadow_size) - self.meadow_size/2 + cursor[1] 
                obj.location = (x, y, cursor[2])
                print(x)
                print(y)


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
        
        bpy.ops.object.select_all(action='DESELECT')
        
        return {'FINISHED'}    

classes = [Environment_Panel,Environment_Operator]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
