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
    "blender":     (2, 78, 5),
    "location":    "Node Editor",
    "description": "This addons mimics UE4's Blueprint node search system",
    "warning":     "DEV VERSION",
    "wiki_url":    "https://github.com/ScottishCyclops/socket_search",
    "tracker_url": "https://github.com/ScottishCyclops/socket_search/issues",
    "category":    "Node"
}

addon_keymaps = []

'''
tree = context.space_data.node_tree

    # Get nodes from currently edited tree.
    # If user is editing a group, space_data.node_tree is still the base level (outside group).
    # context.active_node is in the group though, so if space_data.node_tree.nodes.active is not
    # the same as context.active_node, the user is in a group.
    # Check recursively until we find the real active node_tree:
    if tree.nodes.active:
        while tree.nodes.active != context.active_node:
            tree = tree.nodes.active.node_tree

    return tree.nodes, tree.links
'''

'''
class SgExportSkeletalMesh(bpy.types.Operator):
    """Export the selection into a skeletal mesh as an FBX file"""

    bl_idname = "sg.export_sk"
    bl_label = "Export selection as a Skeletal mesh"
    bl_options = {"REGISTER"}

    overwrite = bpy.props.BoolProperty(name="overwrite", default=False)
    name = bpy.props.StringProperty(name="name", default="SK_Untitled")

    def run(self, context):
        objects = context.selected_objects
        export_skeletal_mesh(self, context, objects, self.name)

    def execute(self, context):
        self.run(context)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
'''


class SSRelease(bpy.types.Operator):
    """Calls the add node menu and connects the added node"""
    bl_idname = "node.ss_release_socket"
    bl_label = "Release socket"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        #we are in the node editor, on a shader node tree, and we have an active node
        return context.space_data.type == "NODE_EDITOR" and \
            context.space_data.tree_type == "ShaderNodeTree" and \
            context.active_node is not None

    def execute(self, context):
        '''
        nodes = context.selected_nodes
        tree = context.space_data.node_tree

        if len(nodes) == 2:
            bpy.ops.node.link_make(replace=True)
            '''

        node = context.active_node
        bpy.ops.node.add_search(use_transform=False)
        #bpy.ops.wm.call_menu(name="NODE_MT_add")
        node.select = True
        bpy.ops.node.link_make(replace=True)

        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        #return self.execute(context)


addon_keymaps = []


def register():
    bpy.utils.register_class(SSRelease)

    # handle the keymap
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(
        name="Node Editor", space_type="NODE_EDITOR")

    kmi = km.keymap_items.new(
        SSRelease.bl_idname, "LEFTMOUSE", "RELEASE", ctrl=True, shift=True)

    addon_keymaps.append((km, kmi))


def unregister():
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(SSRelease)


if __name__ == "__main__":
    register()
