
from aiden3drenderer import Renderer3D, obj_loader, renderer_type
import pygame
import math

def main():
    # Create the renderer
    renderer = Renderer3D(width=500, height=500, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = None

    renderer.camera.position = [0, 1, -2]
    renderer.render_type = renderer_type.MESH
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/alloy_forge_block.obj")
    obj1 = obj_loader.get_obj("./assets/cobe.obj", (1, 5, 2))
    #print(obj)

    renderer.vertices_faces_list.append(obj)
    renderer.vertices_faces_list.append(obj1)
    # Run the renderer

    renderer.run()


if __name__ == "__main__":
    main()
