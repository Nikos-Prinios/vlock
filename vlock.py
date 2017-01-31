# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Vlock",
    "author": "Nikos",
    "version": (0,1),
    "blender": (2, 7, 8, 0),
    "api": 44539,
    "category": "3D View",
    "location": "View3D > Header",
    "description": "This addon helps you keep some vertices in place.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",}
''' version 0.1 '''

import bpy
from bpy.types import Header
import bmesh

global lock_ON
import bgl
import random
handle = [None]
from bpy import context

lock_ON = False


def VL_update(context):
    """
    """
    global lock_ON
    global vertices
    edit_obj = bpy.context.edit_object
    if edit_obj is not None and edit_obj.is_updated_data is True and lock_ON:
        mesh = bpy.context.scene.objects.active.data
        bm = bmesh.from_edit_mesh(mesh)
        for v in vertices:
            bm.verts[v[0]].co.x = v[1]
            bm.verts[v[0]].co.y = v[2]
            bm.verts[v[0]].co.z = v[3]
        bpy.context.scene.objects.active = bpy.context.scene.objects.active
        bmesh.update_edit_mesh(mesh, True)
    
    if edit_obj is None :
    	lock_ON = False
    bpy.context.area.tag_redraw()	
    return True

def callbackFunction():
    global lock_ON
    global vertices
    if lock_ON:
        obj = context.active_object
        for v in vertices:
            xyz = obj.matrix_world * obj.data.vertices[v[0]].co
            x = xyz[0]
            y = xyz[1]
            z = xyz[2]
            bgl.glPointSize(15)
            bgl.glColor3f(1.0, 0.0, 0.0)
            bgl.glBegin(bgl.GL_POINTS)
            bgl.glVertex3f(float(x),float(y),float(z))
            bgl.glEnd()
    else:
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        

def lock():
    global vertices
    vertices = []
    mesh = bpy.context.scene.objects.active.data
    bm = bmesh.from_edit_mesh(mesh)
    sel_verts = [ vert for vert in bm.verts if vert.select ]
    for v in sel_verts:
        row = [v.index, v.co.x,v.co.y,v.co.z]
        vertices.append(row)


class lock_OP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.lock_action"
    bl_label = "Lock vertices"
    
    def execute(self, context):
        global lock_ON
        lock_ON = not lock_ON
        if lock_ON:
            lock()
        print(lock_ON)
        return {'FINISHED'}


class vlock_button(Header):
    bl_space_type = 'VIEW_3D'
    bl_label = "Vlock"
    bl_idname = "OBJECT_Vlock"
    bl_region_type = 'HEADER'
    bl_context = "scene"

    def draw(self, context):
        global lock_ON
        edit_obj = bpy.context.edit_object
        if edit_obj is not None :
            layout = self.layout
            row = layout.row()
            row.separator()
            if lock_ON:
                row.operator("scene.lock_action", icon='PINNED', text='')
            else:
                row.operator("scene.lock_action", icon='UNPINNED', text='')

  
def register():
    bpy.utils.register_module(__name__)
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(VL_update)
    handle[0] = bpy.types.SpaceView3D.draw_handler_add(callbackFunction, (), 'WINDOW', 'POST_VIEW')



def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.app.handlers.scene_update_post.remove(VL_update)
    #bpy.types.SpaceView3D.draw_handler_remove(handle[0], 'WINDOW')
    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
    handle[0] = None


if __name__ == "__main__":
    register()
