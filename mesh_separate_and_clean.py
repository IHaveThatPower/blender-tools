bl_info = {
    "name": "Separate and Clean Selected",
    "author": "Ryan McClure (McC, IHaveThatPower), inspired by Lewis Niven",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Mesh",
    "description": "Combines 'separate selected' and 'remove all modifiers' into one step.",
    "category": "Mesh",
}

import bpy, io, bmesh
from contextlib import redirect_stdout

class SeparateAndCleanOperator(bpy.types.Operator):
    bl_idname = "mesh.separate_and_clean"
    bl_label = "Separate & Clean"
    bl_options = {'REGISTER', 'UNDO'}

    doModifiers: bpy.props.BoolProperty(
        default=True,
        name='Delete Modifiers'
    )
    doMaterials: bpy.props.BoolProperty(
        default=True,
        name='Remove Unused Materials'
    )
    doVtxGroups: bpy.props.BoolProperty(
        default=True,
        name='Delete Vertex Groups'
    )
    doShapeKeys: bpy.props.BoolProperty(
        default=False,
        name='Delete Shape Keys'
    )
    doUVs: bpy.props.BoolProperty(
        default=False,
        name='Delete UV Maps'
    )
    doVtxColors: bpy.props.BoolProperty(
        default=False,
        name='Delete Vertex Colors'
    )
    doFaceMaps: bpy.props.BoolProperty(
        default=False,
        name='Delete Face Maps'
    )

    def execute(self, context):
        if context.edit_object is not None:
            # All initially-selected objects
            initial_selection = context.selected_objects

            # Active object
            obj = context.edit_object
            mesh = obj.data

            # Snag the selection by getting the bmesh
            bm = bmesh.from_edit_mesh(mesh)
            selectedVerts = [v for v in bm.verts if v.select]
            if len(selectedVerts) == 0:
                self.report({'ERROR'}, 'Must have something selected to separate')
                return {'FINISHED'}

            # Separate the selection
            bpy.ops.mesh.separate(type='SELECTED')

            # See what objects we now have selected
            current_selection = context.selected_objects

            # Identify the new objects
            new_objects = [o for o in current_selection if o not in initial_selection]

            # Loop over the objects and clean 'em up
            for no in new_objects:
                print(no.name)
                if self.doModifiers:
                   no.modifiers.clear()

                if self.doMaterials:
                    # Override context so we don't have to mess with our existing context to use an object operator
                    override_context = context.copy()
                    override_context['active_object'] = no

                    # Capture output so we can report it
                    stdout = io.StringIO()
                    with redirect_stdout(stdout):
                        # Do the actual material cleanup
                        bpy.ops.object.material_slot_remove_unused(override_context)
                    stdout.seek(0)
                    self.report({'INFO'}, stdout.read().strip())
                    del stdout

                if self.doVtxGroups:
                    while len(no.vertex_groups) > 0:
                        for vg in no.vertex_groups:
                            no.vertex_groups.remove(vg)

                if self.doShapeKeys:
                    if no.data.shape_keys is not None:
                        for k in no.data.shape_keys.key_blocks:
                            no.shape_key_remove(k)

                if self.doUVs:
                    while len(no.data.uv_layers) > 0:
                        for uv in no.data.uv_layers:
                            no.data.uv_layers.remove(uv)

                if self.doVtxColors:
                    while len(no.data.vertex_colors) > 0:
                        for vc in no.data.vertex_colors:
                            no.data.vertex_colors.remove(vc)

                if self.doFaceMaps:
                    for fm in no.data.face_maps:
                        print("Removing FaceMap (Mesh) %s" % fm.name)
                        no.data.face_maps.remove(fm)
                    for fm in no.face_maps:
                        print("Removing FaceMap (obj) %s" % fm.name)
                        no.face_maps.remove(fm)
        else:
            self.report({'WARNING'}, 'Must have an active object in edit mode')
        return {'FINISHED'}

    """
    Helper function to make mode-swapping easier.
    @param    string new_mode
    @return   boolean success or failure
    @raises   ValueError
    """
    def swap_mode(self, new_mode):
        valid_modes = ['OBJECT', 'EDIT']
        if new_mode not in valid_modes:
            raise ValueError("Wrong mode")
            return False
        bpy.ops.object.mode_set(mode = new_mode)
        return True

def menu_func(self, context):
    self.layout.operator(SeparateAndCleanOperator.bl_idname)

def register():
    bpy.utils.register_class(SeparateAndCleanOperator)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SeparateAndCleanOperator)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)

if __name__ == "__main__":
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    register()

    ## for testing
    # bpy.ops.mesh.separate_and_clean()
