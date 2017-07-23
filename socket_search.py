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
    "blender":     (2, 79, 0),
    "location":    "Node Editor",
    "description": "This addons mimics UE4's Blueprint node search system",
    "warning":     "DEV VERSION",
    "wiki_url":    "https://github.com/ScottishCyclops/socket_search",
    "tracker_url": "https://github.com/ScottishCyclops/socket_search/issues",
    "category":    "Node"
}

addon_keymaps = []

'''
def autolink(node1, node2, links):
    link_made = False

    for outp in node1.outputs:
        for inp in node2.inputs:
            if not inp.is_linked and inp.name == outp.name:
                link_made = True
                links.new(outp, inp)
                return True

    for outp in node1.outputs:
        for inp in node2.inputs:
            if not inp.is_linked and inp.type == outp.type:
                link_made = True
                links.new(outp, inp)
                return True

    # force some connection even if the type doesn't match
    for outp in node1.outputs:
        for inp in node2.inputs:
            if not inp.is_linked:
                link_made = True
                links.new(outp, inp)
                return True

    # even if no sockets are open, force one of matching type
    for outp in node1.outputs:
        for inp in node2.inputs:
            if inp.type == outp.type:
                link_made = True
                links.new(outp, inp)
                return True

    # do something!
    for outp in node1.outputs:
        for inp in node2.inputs:
            link_made = True
            links.new(outp, inp)
            return True

    print("Could not make a link from " + node1.name + " to " + node2.name)
    return link_made
'''

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


def make_link(node1, node2, tree):
    for inp in node1.inputs:
        if not inp.is_linked:
            for outp in node2.outputs:
                if not outp.is_linked:
                    if inp.name == outp.name or inp.type == outp.type:
                        # print(inp.name)
                        # print(outp.name)
                        tree.links.new(outp, inp)
                        return True
    print("could not connect nodes")
    return False


class SSRelease(bpy.types.Operator):
    """Calls the add node menu and connects the added node"""
    bl_idname = "ss.release"
    bl_label = "Release socket"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.space_data.type == "NODE_EDITOR" and \
            context.space_data.tree_type == "ShaderNodeTree" and \
            context.active_node is not None

    def execute(self, context):
        nodes = bpy.context.selected_nodes
        tree = context.space_data.node_tree

        if len(nodes) == 2:
            make_link(nodes[0], nodes[1], tree)

        bpy.ops.wm.call_menu(name="NODE_MT_add")
        #print(info)
        return {"FINISHED"}


addon_keymaps = []


def register():
    bpy.utils.register_class(SSRelease)

    # handle the keymap
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(
        name="Node Editor", space_type="NODE_EDITOR")

    kmi = km.keymap_items.new(
        SSRelease.bl_idname, "LEFTMOUSE", "RELEASE", ctrl=False, shift=False)

    addon_keymaps.append((km, kmi))


def unregister():
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.utils.unregister_class(SSRelease)


if __name__ == "__main__":
    register()
