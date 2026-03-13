import math

from aiden3drenderer import Renderer3D, obj_loader, renderer_type

def main():
    # Create the renderer
    renderer = Renderer3D(width=800, height=800, title="My 3D Renderer", load_default_shapes=True)
    
    # Set starting shape (optional)
    renderer.current_shape = "plane"

    renderer.camera.position = [0, 0, 0]
    renderer.camera.rotation = [0, math.radians(0), 0]
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/skull.obj")

    renderer.lighting_strictness = 0.5

    renderer.camera.base_speed = 0.01
    renderer.camera.speed = 0.01

    renderer.vertices_faces_list.append(obj)
    renderer.set_texture_for_raster("./assets/skull.png")

    eps_x = 0.5 / 1024
    eps_y = 0.5 / 768

    renderer.generate_cubemap_skybox(20, "./assets/kisspng_skybox2.png",
        # right: 
        ((0.75-eps_x,   1/3+eps_y), (0.5+eps_x,     1/3+eps_y), (0.75-eps_x,   2/3-eps_y), (0.5+eps_x,     2/3-eps_y)),
        # left:
        ((0.25-eps_x,   1/3+eps_y), (0+eps_x,       1/3+eps_y), (0.25-eps_x,   2/3-eps_y), (0+eps_x,       2/3-eps_y)),
        # top: 
        ((0.5-eps_x,    1-eps_y),   (0.25+eps_x,    1-eps_y),   (0.5-eps_x,    2/3+eps_y), (0.25+eps_x,    2/3+eps_y)),
        # bottom:
        ((0.25+eps_x,    1/3-eps_y), (0.5-eps_x,    1/3-eps_y), (0.25+eps_x,    0+eps_y),   (0.5-eps_x,    0+eps_y)),
        # forward:
        ((0.75+eps_x,    1/3+eps_y), (1-eps_x,      1/3+eps_y), (0.75+eps_x,    2/3-eps_y), (1-eps_x,      2/3-eps_y)),
        # back: 
        ((0.25+eps_x,    1/3+eps_y), (0.5-eps_x,    1/3+eps_y), (0.25+eps_x,    2/3-eps_y), (0.5-eps_x,    2/3-eps_y)),
    )

    #renderer.toggle_heat_map(True)
    # Run the renderer

    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()