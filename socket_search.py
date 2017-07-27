#    'Socket Search' is a blender addon designed to mimic
#    Unreal Engine 4's Blueprint node search system
#    Copyright (C) 2017 Scott Winkelmann
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name":        "Socket Search",
    "author":      "Scott Winkelmann <scottlandart@gmail.com>",
    "version":     (1, 0, 0),
    "blender":     (2, 78, 0),
    "location":    "Node Editor",
    "description": "This addons mimics UE4's Blueprint node search system",
    "warning":     "DEV VERSION",
    "wiki_url":    "https://github.com/ScottishCyclops/socket_search",
    "tracker_url": "https://github.com/ScottishCyclops/socket_search/issues",
    "category":    "Node"
}

addon_keymaps = []


class SSRelease(bpy.types.Operator):
    """Operator running on timer to check if a socket realease occured"""
    bl_idname = "node.release_socket"
    bl_label = "Socket Search Timer"

    _timer = None
    catched = False

    def modal(self, context, event):
        op = context.active_operator
        if op is not None:
            if op.name == "Link Nodes":
                if not self.catched:
                    self.catched = True
                    print("released!")
                    print(event.type)
            else:
                self.catched = False
        '''
        if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            op = context.active_operator
            if op is not None:
                print(op.name)
        '''

        return {'PASS_THROUGH'}

    def execute(self, context):
        #add the timer on first run
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        #remove the timer
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


class SSAddConnect(bpy.types.Operator):
    """Calls the add node menu and connects the added node"""
    bl_idname = "node.ss_add_connect"
    bl_label = "Add And Connect"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        #we are in the node editor, on a shader node tree, and we have an active node
        return context.space_data.type == "NODE_EDITOR" and \
            context.space_data.tree_type == "ShaderNodeTree" and \
            context.active_node is not None

    def execute(self, context):
        #the folowing line calls the add menu. it is useless (see README)
        #bpy.ops.wm.call_menu(name="NODE_MT_add")

        #save the active node for later
        node = context.active_node
        #add a new node
        #clling add_search without the "node_item" param uses 0 and thus adds the first node "Attribute"
        bpy.ops.node.add_search(use_transform=False)
        #re-select the node
        node.select = True
        #link the two nodes
        #replace=True is not mandatory
        bpy.ops.node.link_make(replace=True)

        return {"FINISHED"}

    def invoke(self, context, event):
        #folowing line invokes the property dialogue. not usefull for now
        #return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)


#defines the list that will contain all the addon keymaps
#disabled for now, because of the use of the timer to detect socket release instead of the left click release
#addon_keymaps = []


def register():
    bpy.utils.register_class(SSRelease)
    bpy.utils.register_class(SSAddConnect)

    '''
    # handle the keymap
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(
        name="Node Editor", space_type="NODE_EDITOR")
    kmi = km.keymap_items.new(
        SSRelease.bl_idname, "LEFTMOUSE", "RELEASE", ctrl=False, shift=False)

    addon_keymaps.append((km, kmi))
    '''


def unregister():
    '''
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    '''

    bpy.utils.unregister_class(SSAddConnect)
    bpy.utils.unregister_class(SSRelease)


if __name__ == "__main__":
    register()

    #calls the timer to start it
    #if the addon is installed, you will need to run the operator yourself the first time
    bpy.ops.node.release_socket()
