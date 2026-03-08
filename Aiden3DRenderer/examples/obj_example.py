from aiden3drenderer import Renderer3D, obj_loader, renderer_type

def main():
    # Create the renderer
    renderer = Renderer3D(width=800, height=600, title="My 3D Renderer")
    
    # Set starting shape (optional)
    renderer.current_shape = None

    renderer.camera.position = [0, 0, 0]
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/alloy_forge_block.obj")
    #print(obj)

    renderer.vertices_faces_list.append(obj)
    renderer.set_texture_for_raster("./assets/alloy_forge_block.png")

    #renderer.toggle_depth_view(True)
    # Run the renderer

    renderer.run()


if __name__ == "__main__":
    main()