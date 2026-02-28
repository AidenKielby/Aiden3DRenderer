from aiden3drenderer import VideoRenderer3D, VideoRendererObject

vO = VideoRendererObject("./assets/trident.obj")
vO.rotations_per_seccond = [1, 1, 0]
vO.anchor_pos = [0, 0, 5]

vO1 = VideoRendererObject("./assets/cobe.obj")
vO1.rotations_per_seccond = [1, 1, 0]
vO1.anchor_pos = [0, 0, 2]

renderer = VideoRenderer3D(200, 200, 5, [vO, vO1])

renderer.render("test.avi", 5, True)