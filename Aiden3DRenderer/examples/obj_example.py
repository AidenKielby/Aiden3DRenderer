
from aiden3drenderer import Renderer3D, obj_loader, renderer_type
import pygame
import math

def main():
    # Create the renderer
    renderer = Renderer3D(width=500, height=500, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = None

    renderer.camera.position = [0, 1, -2]
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True
    renderer.rasterization_size = (250,250)

    obj = obj_loader.get_obj("./assets/alloy_forge_block.obj")
    #print(obj)

    renderer.vertices_faces_list.append(obj)
    # Run the renderer

    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()
