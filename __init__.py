#    'Drag and Search' is a blender addon designed to mimic
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
    "name":        "Drag and Search
    "author":      "Scott Winkelmann <scottlandart@gmail.com>",
    "version":     (1, 0, 0),
    "blender":     (2, 78, 0),
    "location":    "Node Editor",
    "description": "This addons mimics UE4's Blueprint node search system",
    "warning":     "",
    "wiki_url":    "https://github.com/ScottishCyclops/tensionmap",
    "tracker_url": "https://github.com/ScottishCyclops/tensionmap/issues",
    "category":    "Object"
}


addon_keymaps = []

class OpTest(bpy.types.Operator):
    """My test operator"""
    bl_idname = "yoyoyo.boy"
    bl_label = "do some shit bro"
    bl_options = {"REGISTER"}
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        bpy.ops.wm.call_menu(name="NODE_MT_add")
        self.report({"INFO"}, "executed...")
        return {"FINISHED"}

addon_keymaps = []

def register():
    bpy.utils.register_class(OpTest)
    
    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type="NODE_EDITOR")

    kmi = km.keymap_items.new(OpTest.bl_idname, 'LEFTMOUSE', 'PRESS', ctrl=False, shift=False)

    addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(OpTest)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
if __name__ == "__main__":
    register()
