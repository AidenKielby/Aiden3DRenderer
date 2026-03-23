import math

from aiden3drenderer import Renderer3D, obj_loader, renderer_type, Entity, bounding_box

def main():
    # Create the renderer
    renderer = Renderer3D(width=800, height=800, title="My 3D Renderer", load_default_shapes=True)
    
    # Set starting shape (optional)
    renderer.current_shape = "plane"

    renderer.camera.position = [0, 0, 0]
    renderer.camera.rotation = [0, math.radians(0), 0]
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True

    obj = obj_loader.get_obj("./assets/skull.obj", renderer.add_texture_for_raster("./assets/skull.png"), scale=4)

    obj1 = obj_loader.get_obj("./assets/cup.obj", renderer.add_texture_for_raster("./assets/cup.png"), offset=(2,3,2))

    renderer.lighting_strictness = 0.5

    renderer.camera.base_speed = 0.05
    renderer.camera.speed = 0.05

    renderer.vertices_faces_list.append(obj1)

    #renderer.generate_cross_type_cubemap_skybox(20, "./assets/cubemap-cross.jpg")
    renderer.generate_cross_type_cubemap_skybox(20, "./assets/kisspng_skybox2.png")
    #renderer.render_distance = 5

    #renderer.toggle_heat_map(True)
    # Run the renderer
    renderer.generate_sprite_bilboard("./assets/pixelart_guy.png", pos=(2, 2, 0))

    plane = obj_loader.get_obj("./assets/plane.obj", renderer.add_texture_for_raster("./assets/plane.png"), offset=(0,-1,0), type="plane")
    plane_bb = bounding_box.get_bounding_box(plane[0])
    renderer.add_obj(plane, bounding_box=plane_bb)

    ent = Entity(obj, renderer=renderer, bounding_box = bounding_box.get_bounding_box(obj[0]))
    entity_script = """
import math
dx = renderer.camera.position[0] - entity.position[0]
dy = renderer.camera.position[1] - entity.position[1]
dz = renderer.camera.position[2] - entity.position[2]

dist = math.sqrt(dx*dx + dy*dy + dz*dz)

if dist > 0.1:
    speed = 1
    entity.velocity = (dx/dist * speed, dy/dist * speed, dz/dist * speed)
    entity.rotation = (
        0,
        -math.degrees(math.atan2(dx, dz)),
        0
    )
else:
    entity.velocity = (0, 0, 0)
"""


    ent.toggle_gravity()
    renderer.add_entity(ent)

    obj2 = obj_loader.get_obj("./assets/skull.obj", 1, scale=4)

    renderer.vertices_faces_list.append(obj2)

    renderer.set_rasterization_size((500,500))

    #renderer.run()

    renderer.run()


if __name__ == "__main__":
    main()