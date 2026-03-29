import math
from pathlib import Path

from aiden3drenderer import Renderer3D, obj_loader, renderer_type, Entity, bounding_box

def main():
    # Create the renderer
    renderer = Renderer3D(width=800, height=800, title="My 3D Renderer", load_default_shapes=True, resizable_window=True)
    
    # Set starting shape (optional)
    renderer.current_shape = "plane"

    # Position the camera back so objects at the origin are visible
    renderer.camera.position = [0, 0, -5]
    renderer.camera.rotation = [0, 0, 0]
    # Use GPU rasterization (compute shader) rendering
    renderer.render_type = renderer_type.RASTERIZE
    renderer.using_obj_filetype_format = True

    # Resolve example asset paths relative to the project root so running from any CWD works
    assets_dir = Path(__file__).resolve().parent.parent / "assets"

    obj = obj_loader.get_obj(str(assets_dir / "skull.obj"), renderer.add_texture_for_raster(str(assets_dir / "skull.png")), scale=4)

    obj1 = obj_loader.get_obj(str(assets_dir / "cup.obj"), renderer.add_texture_for_raster(str(assets_dir / "cup.png")), offset=(2,3,2))

    renderer.lighting_strictness = 0.5

    renderer.camera.base_speed = 0.05
    renderer.camera.speed = 0.05

    renderer.vertices_faces_list.append(obj1)

    #renderer.generate_cross_type_cubemap_skybox(20, "./assets/cubemap-cross.jpg")
    renderer.generate_cross_type_cubemap_skybox(20, str(assets_dir / "kisspng_skybox2.png"))
    #renderer.render_distance = 5

    #renderer.toggle_heat_map(True)
    # Run the renderer
    renderer.generate_sprite_bilboard(str(assets_dir / "pixelart_guy.png"), pos=(2, 2, 0))

    plane = obj_loader.get_obj(str(assets_dir / "plane.obj"), renderer.add_texture_for_raster(str(assets_dir / "plane.png")), offset=(0,-1,0), type="plane")
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

    obj2 = obj_loader.get_obj(str(assets_dir / "skull.obj"), 1, scale=4)

    renderer.vertices_faces_list.append(obj2)

    renderer.set_rasterization_size((400,400))

    # Example: add a post-process compute shader (separable bloom around red pixels)
    from aiden3drenderer.custom_shader import CustomShader

    horiz_cs = """
    #version 430
    layout(local_size_x = 16, local_size_y = 16) in;

    layout(rgba32f, binding = 0) uniform image2D destTex;
    uniform sampler2D srcTex; // original scene (bound to unit 2 for first pass)
    uniform float threshold = 0.15;
    uniform int radius = 8;

    void main() {
        ivec2 px = ivec2(gl_GlobalInvocationID.xy);
        ivec2 dims = imageSize(destTex);
        if (px.x >= dims.x || px.y >= dims.y) return;

        vec2 uv = (vec2(px) + vec2(0.5)) / vec2(dims);

        float sigma = max(1.0, float(radius) * 0.4);
        float falloff = 2.0 * sigma * sigma;

        vec3 col_sum = vec3(0.0);
        float w_sum = 0.0;

        for (int x = -radius; x <= radius; x++) {
            float w = exp(-float(x * x) / falloff);
            vec4 s = texture(srcTex, uv + vec2(float(x) / float(dims.x), 0.0));
            float redness = max(0.0, s.r - max(s.g, s.b));
            float mask = smoothstep(threshold, threshold + 0.15, redness);
            col_sum += s.rgb * mask * w;
            w_sum += w;
        }

        vec3 result = col_sum / max(1e-5, w_sum);
        imageStore(destTex, px, vec4(result, 1.0));
    }
    """

    vert_cs = """
    #version 430
    layout(local_size_x = 16, local_size_y = 16) in;

    layout(rgba32f, binding = 0) uniform image2D destTex;
    uniform sampler2D srcTex;   // horizontal-blurred bloom (bound to unit 2 for second pass)
    uniform sampler2D sceneTex; // original scene (we bind original output to unit 3)
    uniform float strength = 2.0;
    uniform int radius = 8;

    void main() {
        ivec2 px = ivec2(gl_GlobalInvocationID.xy);
        ivec2 dims = imageSize(destTex);
        if (px.x >= dims.x || px.y >= dims.y) return;

        vec2 uv = (vec2(px) + vec2(0.5)) / vec2(dims);

        float sigma = max(1.0, float(radius) * 0.4);
        float falloff = 2.0 * sigma * sigma;

        vec3 bloom_sum = vec3(0.0);
        float w_sum = 0.0;

        for (int y = -radius; y <= radius; y++) {
            float w = exp(-float(y * y) / falloff);
            bloom_sum += texture(srcTex, uv + vec2(0.0, float(y) / float(dims.y))).rgb * w;
            w_sum += w;
        }

        vec3 bloom = bloom_sum / max(1e-5, w_sum);
        vec4 scene = texture(sceneTex, uv);
        vec3 outc = scene.rgb + bloom * strength;
        outc = clamp(outc, 0.0, 1.0);
        imageStore(destTex, px, vec4(outc, scene.a));
    }
    """

    BLOOM_RADIUS = 70
    STRENGTH = 2.5
    THRESHOLD = 0.02

    try:
        cs_h = CustomShader(horiz_cs, context=renderer.ctx)
        cs_v = CustomShader(vert_cs, context=renderer.ctx)

        rw, rh = renderer.rasterization_size
        # Bind the current scene texture to unit 3 so the vertical pass can combine it
        try:
            renderer.output_tex.use(location=3)
        except Exception:
            pass

        renderer.shaders.append({
            'shader': cs_h,
            'inputs': [
                ("threshold", THRESHOLD),
                ("radius", BLOOM_RADIUS),
                # srcTex is bound automatically to unit 2 (current input texture)
            ],
        })

        renderer.shaders.append({
            'shader': cs_v,
            'inputs': [
                ("strength", STRENGTH),
                ("radius", BLOOM_RADIUS),
                ("sceneTex", lambda: 3),
            ],
        })

    except Exception as e:
        print(f"Bloom shader error: {e}")

    renderer.run()


if __name__ == "__main__":
    main()