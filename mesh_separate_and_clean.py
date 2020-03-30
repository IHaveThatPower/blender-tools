bl_info = {
    "name": "Separate and Clean Selected",
    "author": "Ryan McClure (McC, IHaveThatPower), inspired by Lewis Niven",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Mesh",
    "description": "Combines 'separate selected' and 'remove all modifiers' into one step.",
    "category": "Mesh",
}

import bpy, io
from contextlib import redirect_stdout
 
class SeparateAndCleanOperator(bpy.types.Operator):
    bl_idname = "mesh.separate_and_clean"
    bl_label = "Separate & Clean"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.edit_object is not None:
            # All initially-selected objects
            initial_selection = context.selected_objects
            
            # Active object
            obj = context.edit_object
            mesh = obj.data
            
            # Update and snag the selection by toggling into and out of object mode
            self.swap_mode('OBJECT')
            selectedVerts = [v for v in mesh.vertices if v.select]
            selectedEdges = [e for e in mesh.edges if e.select]
            selectedFaces = [f for f in mesh.polygons if f.select]
            if len(selectedVerts) == 0 and len(selectedEdges) == 0 and len(selectedFaces) == 0:
                self.report({'ERROR'}, 'Must have something selected to separate')
                return {'FINISHED'}
            
            # Capture current mode for later restoration
            # currentMode = bpy.context.tool_settings.mesh_select_mode[:]
            # Set mode to all
            # bpy.context.tool_settings.mesh_select_mode = (True, True, True)

            # selectedVerts = [v for v in mesh.vertices if v.select]
            # bpy.ops.object.mode_set(mode = 'EDIT')
            # If we still have nothing selected, assume we want to operate on everything.
            # hadNoneSelected = False
            # if len(selectedVerts) == 0:
            #    hadNoneSelected = True
            #    bpy.ops.mesh.select_all(action='SELECT')
            
            # Remove doubles
            #stdout = io.StringIO()
            #with redirect_stdout(stdout):
            #    bpy.ops.mesh.remove_doubles(threshold=self.Threshold, use_unselected=False)
            #stdout.seek(0)
            #self.report({'INFO'}, stdout.read().strip())
            #del stdout
            # Restore the non-selection if applicable
            #if hadNoneSelected is True:
            #    bpy.ops.mesh.select_all(action='DESELECT')
            
            # Flip back to edit mode to do the separation
            self.swap_mode('EDIT')
            bpy.ops.mesh.separate(type='SELECTED')
            
            # Flip back to object mode to see what we now have selected
            self.swap_mode('OBJECT')
            current_selection = context.selected_objects
            
            # Identify the new objects only and purge them of modifiers
            new_objects = [o for o in current_selection if o not in initial_selection]
            for no in new_objects:
                no.modifiers.clear()
            
            # Now swap our selection to the new stuff and remove unused materials
            for io in initial_selection:
                if io not in new_objects:
                    io.select_set(False)
            for no in new_objects:
                no.select_set(True)
            bpy.ops.object.material_slot_remove_unused()
            
            # Swap back to our previous selection, including the separated object
            for co in current_selection:
                co.select_set(True)
            # Ensure our original active object is still active
            context.view_layer.objects.active = obj

            # Switch back into edit mode
            self.swap_mode('EDIT')
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