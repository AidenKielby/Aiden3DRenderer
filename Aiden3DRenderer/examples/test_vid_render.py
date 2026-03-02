from aiden3drenderer import VideoRenderer3D, VideoRendererObject

vO1 = VideoRendererObject("./assets/cobe.obj")
vO1.rotations_per_seccond = [1, 1, 0]
vO1.anchor_pos = [0, 0, 2]

renderer = VideoRenderer3D(300, 250, 5, [vO1])

renderer.render("test.avi", 5, True)