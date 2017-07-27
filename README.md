# Socket Search Blender Addon

Blender addon designed to replicate UE4's node search feature.


## Current state

I am now able to detect a socket release.
It is hard because Blender doesn't generate a "left mouse release" when you release a socket.
THe way I did it is with a timer Operator. it gets called every 0.1 secondes and checks the context.
`bpy.context.active_operator` holds the latest operator executed. I can then test if it is a `bpy.ops.node.link`.

Problem: as long as no other operators are called, the last one stays the same. So I can't know if the socket release has been done a second time or if it is just the last operator.

Possible fix: call my own operator to force the last operator to change and thus be able to detect when `node.link` is fired again

+:
    will work

-:
    quite dirty


I am able to add a node and connect it to the active node.
I can't "re-use" the node add menu, becasue menus in Blender do not "return" what element was clicked. Instead, each entry in the menu calls an operator. In the case of the *search node menu*, each call `bpy.ops.node.add_search` with a unique index per entry.

Possible fix: create a whole different menu containing all the nodes and make each entry call my operator.

+:
    gives the oportunity to make a context-sentifive menu

-:
    a lot of work and a need to redo it for any added node



## References

[Unreal Engine: How to place nodes](https://docs.unrealengine.com/latest/INT/Engine/Blueprints/BP_HowTo/PlacingNodes/index.html)

[Blender Python API news 2.79](https://wiki.blender.org/index.php/Dev:Ref/Release_Notes/2.79/PythonAPI)

[Blender Python API node.link](https://docs.blender.org/api/blender_python_api_2_76_9/bpy.ops.node.html#bpy.ops.node.link)
