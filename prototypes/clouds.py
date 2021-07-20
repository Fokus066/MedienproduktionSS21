import bpy, typing

class clouds: 

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
        node_colorramp.color_ramp.elements[0].position = 0.6
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
        bpy.ops.mesh.primitive_cube_add()
            
        cloud= bpy.context.object
        cloud.name = "cloud"

        cloud.data.materials.append(self.cloud_material())

              
hay_bale = clouds()
hay_bale.generate_clouds()
    
    