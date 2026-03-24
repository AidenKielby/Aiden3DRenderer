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

    # Example: add a post-process compute shader (bloom for red pixels)
    from aiden3drenderer.custom_shader import CustomShader

    # ── Pass 1: horizontal blur → intermediate texture ──────────────────────────
    horiz_cs = """
    #version 430
    layout(local_size_x = 16, local_size_y = 16) in;

    layout(rgba32f, binding = 0) uniform image2D destTex;
    uniform sampler2D srcTex;
    uniform float threshold = 0.15;
    uniform int   radius    = 16;

    void main() {
        ivec2 px   = ivec2(gl_GlobalInvocationID.xy);
        ivec2 dims = imageSize(destTex);
        if (px.x >= dims.x || px.y >= dims.y) return;

        vec2  uv      = (vec2(px) + 0.5) / vec2(dims);
        float sigma   = max(1.0, float(radius) * 0.4);
        float falloff = 2.0 * sigma * sigma;

        vec3  col_sum = vec3(0.0);
        float w_sum   = 0.0;

        for (int x = -radius; x <= radius; x++) {
            float w   = exp(-float(x * x) / falloff);
            vec2  off = vec2(float(x) / float(dims.x), 0.0);
            vec4  s   = texture(srcTex, uv + off);

            // only let pixels that are "red enough" emit bloom
            float redness = max(0.0, s.r - max(s.g, s.b));
            float mask    = smoothstep(threshold, threshold + 0.15, redness);
            col_sum += s.rgb * mask * w;
            w_sum   += w;
        }

        vec3 result = col_sum / max(1e-5, w_sum);
        imageStore(destTex, px, vec4(result, 1.0));
    }
    """

    # ── Pass 2: vertical blur + composite onto original ─────────────────────────
    vert_cs = """
    #version 430
    layout(local_size_x = 16, local_size_y = 16) in;

    layout(rgba32f, binding = 0) uniform image2D destTex;   // final output
    uniform sampler2D srcTex;      // original scene colour
    uniform sampler2D bloomTex;    // result of horizontal pass
    uniform float strength = 2.0;
    uniform int   radius   = 16;

    void main() {
        ivec2 px   = ivec2(gl_GlobalInvocationID.xy);
        ivec2 dims = imageSize(destTex);
        if (px.x >= dims.x || px.y >= dims.y) return;

        vec2  uv      = (vec2(px) + 0.5) / vec2(dims);
        float sigma   = max(1.0, float(radius) * 0.4);
        float falloff = 2.0 * sigma * sigma;

        vec3  bloom_sum = vec3(0.0);
        float w_sum     = 0.0;

        for (int y = -radius; y <= radius; y++) {
            float w   = exp(-float(y * y) / falloff);
            vec2  off = vec2(0.0, float(y) / float(dims.y));
            bloom_sum += texture(bloomTex, uv + off).rgb * w;
            w_sum     += w;
        }

        vec3 bloom = bloom_sum / max(1e-5, w_sum);

        // yellow-tint the bloom and add onto original scene
        vec3 tint   = vec3(1.0, 0.88, 0.3);
        vec4 scene  = texture(srcTex, uv);
        vec3 outc   = scene.rgb + bloom * tint * strength;
        outc        = clamp(outc, 0.0, 1.0);

        imageStore(destTex, px, vec4(outc, scene.a));
    }
    """

    BLOOM_RADIUS = 200
    STRENGTH     = 10.0
    THRESHOLD    = 0.01

    try:
        cs_h = CustomShader(horiz_cs, context=renderer.ctx)
        cs_v = CustomShader(vert_cs,  context=renderer.ctx)

        # ↓ paste it all here, replacing everything that was here before
        rw, rh = renderer.rasterization_size
        bloom_intermediate = renderer.ctx.texture((rw, rh), 4, dtype='f4')
        scene_snapshot     = renderer.ctx.texture((rw, rh), 4, dtype='f4')

        cs_h.compute_shader['threshold'].value = THRESHOLD
        cs_h.compute_shader['radius'].value    = BLOOM_RADIUS
        cs_h.compute_shader['srcTex'].value    = 2

        cs_v.compute_shader['strength'].value  = STRENGTH
        cs_v.compute_shader['radius'].value    = BLOOM_RADIUS
        cs_v.compute_shader['srcTex'].value    = 2
        cs_v.compute_shader['bloomTex'].value  = 3

        renderer.output_tex.use(location=2)
        bloom_intermediate.use(location=3)

        renderer.shaders.append({'shader': cs_h, 'inputs': [], '_dest_tex': bloom_intermediate})
        renderer.shaders.append({'shader': cs_v, 'inputs': []})

    except Exception as e:
        print(f"Bloom shader error: {e}")

    renderer.run()


if __name__ == "__main__":
    main()