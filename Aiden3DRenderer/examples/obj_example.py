
from aiden3drenderer import Renderer3D, obj_loader, renderer_type
import pygame
import math

def main():
    # Create the renderer
    renderer = Renderer3D(width=700, height=700, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = None

    renderer.camera.position = [0, 1, -2]
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/monkey.obj")
    #print(obj)

    renderer.vertices_faces_list.append(obj)
    # Run the renderer

    renderer.toggle_depth_view(True)

    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()
