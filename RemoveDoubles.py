bl_info = {
	"name": "Remove Doubles Classic",
	"author": "Ryan McClure (McC, IHaveThatPower), melak47",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Mesh",
	"description": "Simple remove doubles functionality that can be directly keybound, operating either on existing selection or selecting the entire current object.",
	"category": "Mesh",
}

import bpy
 
class RemoveDoublesOperator(bpy.types.Operator):
	bl_idname = "mesh.remove_doubles_classic"
	bl_label = "Remove Doubles"
	bl_options = {'REGISTER', 'UNDO'}
	
	threshold: bpy.props.FloatProperty(
		min=0,
		default=0.0001,
	)
	
	def execute(self, context):
		if bpy.context.edit_object is not None:
			obj = bpy.context.edit_object
			mesh = obj.data
			# Flip to edit mode for object operation
			# Capture current mode for later restoration
			currentMode = bpy.context.tool_settings.mesh_select_mode[:]
			# Set mode to vertex
			bpy.context.tool_settings.mesh_select_mode = (True, False, False)
			# Update and snag the selection by toggling into and out of object mode
			bpy.ops.object.mode_set(mode = 'OBJECT')
			selectedVerts = [v for v in mesh.vertices if v.select]
			bpy.ops.object.mode_set(mode = 'EDIT')
			# If we still have nothing selected, assume we want to operate on everything.
			hadNoneSelected = False
			if len(selectedVerts) == 0:
				hadNoneSelected = True
				bpy.ops.mesh.select_all(action='SELECT')
			selectedVerts = [v for v in mesh.vertices if v.select]
			# Remove doubles
			bpy.ops.mesh.remove_doubles(threshold=self.threshold, use_unselected=False)
			# Restore the non-selection if applicable
			if hadNoneSelected is True:
				bpy.ops.mesh.select_all(action='DESELECT')
			# Restore selection mode
			bpy.context.tool_settings.mesh_select_mode = currentMode
			# Update by toggling into and out of object mode
			bpy.ops.object.mode_set(mode = 'OBJECT')
			bpy.ops.object.mode_set(mode = 'EDIT')
		else:
			self.report({'WARNING'}, 'Must have an active object in edit mode')
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(RemoveDoublesOperator.bl_idname)

def register():
	bpy.utils.register_class(RemoveDoublesOperator)
	bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
	bpy.utils.unregister_class(RemoveDoublesOperator)
	bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)

if __name__ == "__main__":
	register()

	## for testing
	bpy.ops.mesh.remove_doubles_classic()