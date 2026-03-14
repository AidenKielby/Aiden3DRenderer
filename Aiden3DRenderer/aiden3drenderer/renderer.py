"""
Main 3D renderer class
"""
import math
import pygame
from pygame import QUIT
import sys
import importlib
from enum import Enum
import numpy as np
import moderngl
from PIL import Image

from .camera import Camera

CUSTOM_SHAPES = {}

def register_shape(name: str, key=None, is_animated: bool = False, color: tuple[int] = None):
    def decorator(func):
        CUSTOM_SHAPES[name] = {
            'function': func,
            'is_animated': is_animated,
            'key': key,
            'color': color
        }
        return func
    return decorator

class renderer_type(Enum):
    RASTERIZE = "rasterize"
    POLYGON_FILL = "polygon_fill"
    MESH = "mesh"

compute_shader_for_rasterization = """
#version 430

layout(local_size_x = 16, local_size_y = 16) in;

struct Triangle {
    vec2 pos1;    // 0  - 8  bytes
    vec2 pos2;    // 8  - 16 bytes 
    vec2 pos3;    // 16 - 24 bytes 
    
    float d1;     // 24 - 28 bytes (Depth for p1)
    float d2;     // 28 - 32 bytes (Depth for p2)
    float d3;     // 32 - 36 bytes (Depth for p3)
    
    float light_mult;   // 36 - 40 

    vec2 uv1;    // 40 - 48
    vec2 uv2;    // 48 - 56
    vec2 uv3;    // 56 - 64

    float is_skybox;   // 64 - 68
    float texture_index; // 68 - 72
    float pad1; // 72 - 76
    float pad2; // 76 - 80
};

layout(std430, binding = 0) buffer triangle_data {
    Triangle tris[];
};

layout(std430, binding = 1) buffer DepthBuffer {
    uint pixel_depths[]; // Store as fixed-point integers for atomicMin
};

layout(rgba32f, binding = 0) writeonly uniform image2D destTex;

uniform sampler2DArray inTex;
uniform sampler2D skyTex;
uniform uint tri_count;

uniform bool depthView;
uniform bool heatMap;

shared Triangle local_tris[256];

float dot(vec2 p1, vec2 p3, vec2 p2) {
    vec2 tri_vec = p2-p1;
    vec2 other_vec = p3 - p1;

    return tri_vec.x * other_vec.y - tri_vec.y * other_vec.x;
}   

bool is_point_in_tri(vec2 p0, vec2 p1, vec2 p2, vec2 point) {
    float d1 = dot(p0, p1, point);
    float d2 = dot(p1, p2, point);
    float d3 = dot(p2, p0, point);

    bool has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0);
    bool has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0);
    
    return !(has_neg && has_pos);
}  

float tri_area(vec2 p1, vec2 p2, vec2 p3){
    vec2 a = p2 - p1;
    vec2 b = p3 - p1;
    // The magnitude of the cross product of two vectors 
    // is the area of the parallelogram they form. 
    // Half of that is the triangle area.
    return 0.5 * abs(a.x * b.y - a.y * b.x);
}

float cross2d(vec2 a, vec2 b) {
    return a.x * b.y - a.y * b.x;
}

float depth_in_tri(vec2 p0, vec2 p1, vec2 p2, vec2 point, vec3 depths) {
    vec2 v0 = p1 - p0;
    vec2 v1 = p2 - p0;
    vec2 v2 = point - p0;

    // Total area (technically double the area, but ratios remain the same)
    float total = cross2d(v0, v1);

    // Prevent division by zero for degenerate triangles
    if (abs(total) < 0.00001) {
        return 1e38; // GLSL equivalent of infinity
    }

    // Barycentric coordinates (weights)
    // We use the vectors from the vertices to the point
    float w1 = cross2d(v2, v1) / total;
    float w2 = cross2d(v0, v2) / total;
    float w0 = 1.0 - w1 - w2;

    // Interpolate depth using the weights
    // depths.x = depth at p0, depths.y = depth at p1, depths.z = depth at p2
    float depth = w0 * depths.x + w1 * depths.y + w2 * depths.z;

    return depth;
}

void main() {
    ivec2 pixel_coords = ivec2(gl_GlobalInvocationID.xy);
    ivec2 dims = imageSize(destTex);
    if (pixel_coords.x >= dims.x || pixel_coords.y >= dims.y) return;

    uint pixel_index = pixel_coords.y * dims.x + pixel_coords.x;
    vec2 p_center = vec2(pixel_coords) + 0.5;

    float best_depth = 1e38;
    vec3 best_color = vec3(1.0);

    uint num_tris = min(tri_count, uint(tris.length()));
    uint local_id = gl_LocalInvocationIndex; // 0 to 255

    // LOOP IN CHUNKS OF 256
    for (uint i = 0; i < num_tris; i += 256) {
        if (i + local_id < num_tris) {
            local_tris[local_id] = tris[i + local_id];
        }
        
        barrier(); // Wait for all threads to finish loading

        uint limit = min(256, num_tris - i);
        for (uint j = 0; j < limit; j++) {
            if (is_point_in_tri(local_tris[j].pos1, local_tris[j].pos2, local_tris[j].pos3, p_center)) {
                vec3 ds = vec3(local_tris[j].d1, local_tris[j].d2, local_tris[j].d3);
                float d = depth_in_tri(local_tris[j].pos1, local_tris[j].pos2, local_tris[j].pos3, p_center, ds);
                
                if (d < best_depth) {
                    best_depth = d;
                    if (depthView){
                        float c = -pow(2, (-abs(d) * 0.75))+1;
                        best_color = vec3(c, c, c);
                    }
                    else if (heatMap){
                        float t = clamp(d * 0.35, 0.0, 1.0);
                        best_color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), t);
                    }
                    else{
                        if (local_tris[j].uv1.x < 0.0 || local_tris[j].uv2.x < 0.0 || local_tris[j].uv3.x < 0.0) {
                            float c = -pow(2, (-abs(d) * 0.75))+1;
                            best_color = vec3(c, c, c);
                        }
                        else{
                            vec3 ws = vec3(1.0/local_tris[j].d1, 1.0/local_tris[j].d2, 1.0/local_tris[j].d3);

                            vec3 us = vec3(local_tris[j].uv1.x * ws.x, local_tris[j].uv2.x * ws.y, local_tris[j].uv3.x * ws.z);
                            vec3 vs = vec3(local_tris[j].uv1.y * ws.x, local_tris[j].uv2.y * ws.y, local_tris[j].uv3.y * ws.z);

                            float u_over_w = depth_in_tri(local_tris[j].pos1, local_tris[j].pos2, local_tris[j].pos3, p_center, us);
                            float v_over_w = depth_in_tri(local_tris[j].pos1, local_tris[j].pos2, local_tris[j].pos3, p_center, vs);
                            float one_over_w = depth_in_tri(local_tris[j].pos1, local_tris[j].pos2, local_tris[j].pos3, p_center, ws);

                            vec2 uv = vec2(u_over_w / one_over_w, 1.0 - (v_over_w / one_over_w));

                            vec4 color = vec4(1.0);

                            if (local_tris[j].is_skybox == 1){
                                color = texture(skyTex, uv);
                            }
                            else{
                                color = texture(inTex, vec3(uv, local_tris[j].texture_index));
                            }

                            best_color = vec3(color.x * local_tris[j].light_mult, color.y * local_tris[j].light_mult, color.z * local_tris[j].light_mult);
                        }
                        
                    }
                }
            }
        }
        
        barrier(); // Wait before loading the next chunk
    }

    uint z_int = uint(best_depth * 1000000.0);
    uint old_z = atomicMin(pixel_depths[pixel_index], z_int);

    if (z_int <= old_z) {
        imageStore(destTex, pixel_coords, vec4(best_color, 1.0));
    }
    else{
        imageStore(destTex, pixel_coords, vec4(1.0, 1.0, 1.0, 1.0));
    }
}

"""

tri_dtype = np.dtype([
    ('pos', 'f4', (3, 2)),    # 3 positions (x, y)
    ('depths', 'f4', 3),      # 3 depth values
    ('light_mult', 'f4', 1),
    ('uv', 'f4', (3, 2)),     # 3 positions (u, v)
    ('is_skybox', 'f4', 1),
    ('texture_index', 'f4', 1),
    ('pad1', 'f4', 1),
    ('pad2', 'f4', 1),
])

class Renderer3D:
    
    def __init__(self, width=1000, height=1000, title="Aiden 3D Renderer", load_default_shapes: bool = True):
        pygame.init()
        self.width = width
        self.height = height
        self.half_w = width // 2
        self.half_h = height // 2
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        self.camera = Camera()
        self.clock = pygame.time.Clock()
        
        self.current_shape = "mountain"
        self.last_shape = None
        self.animation_time = 0
        self.grid_coords = None
        self.needs_regen = False
        self.shapes = [self.current_shape]
        self.projected = None

        self.is_starting = True

        self.render_type = renderer_type.MESH
        self.triangle_base_color_1= (150, 0, 150)
        self.triangle_base_color_2 = (50, 0, 50)
        self.triangle_color_list_1= []
        self.triangle_color_list_2 = []

        self.grid_coords_list = []
        self.vertices_faces_list = []
        self.projected_vertices_faces_list = []
        self.using_obj_filetype_format = False
        self.projections_list = []

        self.is_using_default_shapes = load_default_shapes
        self._default_shape_names = set()
        self._default_shapes_loaded = False

        self.last_texture_array = None
        self.last_size = 1
        self.texture_layers = []

        self.lighting_strictness = 0.5

        if load_default_shapes:
            before = set(CUSTOM_SHAPES.keys())
            try:
                mod = importlib.import_module('.shapes', package=__package__)
                importlib.reload(mod)
            except Exception:
                mod = None
            after = set(CUSTOM_SHAPES.keys())
            self._default_shape_names = after - before
            self._default_shapes_loaded = bool(self._default_shape_names)

        self.ctx = moderngl.create_context(standalone=True)
        
        if sys.platform != "darwin":
            self.compute_shader = self.ctx.compute_shader(compute_shader_for_rasterization)
            self.compute_shader["depthView"].value = False
            self.compute_shader["heatMap"].value = False
        else:
            self.compute_shader = None
        
        self.output_tex = self.ctx.texture((width, height), 4, dtype='f4')

        self._output_clear_rgba = np.ones((height, width, 4), dtype=np.float32)
        
        self.depth_init_data = np.full(width * height, np.iinfo(np.uint32).max, dtype='u4')
        self.depth_buffer = self.ctx.buffer(self.depth_init_data.tobytes())
        
        self.tri_buffer = self.ctx.buffer(reserve=tri_dtype.itemsize * 10000)

        self.texture_path = None
        self.skybox_texture_path = None

        self.texture = None
        self.skybox_texture = None

    def toggle_depth_view(self, b: bool):
        if sys.platform != "darwin":
            self.compute_shader["depthView"].value = b
    
    def toggle_heat_map(self, b: bool):
        if sys.platform != "darwin":
            self.compute_shader["heatMap"].value = b

    def set_render_type(self, type: renderer_type):
        self.render_type = type

    def set_texture_for_raster(self, img_path):
        if sys.platform != "darwin":
            if self.texture is not None:
                self.texture.release()

            self.texture_path = img_path
            img = Image.open(self.texture_path).convert("RGBA")
            img_data = np.array(img, dtype='u1')

            self.texture_layers = [img_data]
            self.last_texture_array = img_data
            self.last_size = 1

            array_data = np.stack(self.texture_layers, axis=0)  # (layers, h, w, 4)
            self.texture = self.ctx.texture_array(
                size=(img.size[0], img.size[1], self.last_size),
                components=4,
                data=array_data.tobytes()
            )
            self.texture.use(location=0)
            self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.texture.repeat_x = False
            self.texture.repeat_y = False
            self.compute_shader["inTex"].value = 0

    def add_texture_for_raster(self, img_path):
        if sys.platform != "darwin":
            if not self.texture_layers:
                self.set_texture_for_raster(img_path)
                return

            img = Image.open(img_path).convert("RGBA")
            img_data = np.array(img, dtype='u1')

            base_h, base_w, _ = self.texture_layers[0].shape
            h, w, _ = img_data.shape
            if (h, w) != (base_h, base_w):
                raise ValueError(
                    f"Texture size mismatch: expected {(base_w, base_h)}, got {(w, h)}"
                )

            self.texture_layers.append(img_data)
            self.last_size = len(self.texture_layers)
            self.last_texture_array = img_data

            if self.texture is not None:
                self.texture.release()

            array_data = np.stack(self.texture_layers, axis=0)  # (layers, h, w, 4)
            self.texture = self.ctx.texture_array(
                size=(w, h, self.last_size),
                components=4,
                data=array_data.tobytes()
            )
            self.texture.use(location=0)
            self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.texture.repeat_x = False
            self.texture.repeat_y = False
            self.compute_shader["inTex"].value = 0
            

    def generate_cubemap_skybox(self, radius: int, texture_path, left_uvs, right_uvs, top_uvs, bottom_uvs, forward_uvs, backward_uvs):
        #uv inputs go like: op left uv, top right uv, bottom left uv, bottom right uv
        if sys.platform != "darwin":
            verts = np.array([(-1,-1,-1), (1,-1,-1), (-1,1,-1), (-1,-1,1), (1,1,-1), (-1,1,1), (1,-1,1), (1,1,1)])
            verts = verts * radius
            faces = [(0,3,2), (2,5,3), (1,4,6), (6,4,7), (0,1,2), (2,1,4), (3,5,6), (6,5,7), (0,6,1), (0,3,6), (2,4,5), (5,4,7)]

            uvs = [
                # left (0-3)
                left_uvs[1], left_uvs[3], left_uvs[0], left_uvs[2],
                # right (4-7)
                right_uvs[0], right_uvs[1], right_uvs[2], right_uvs[3],
                # backward (8-11)
                backward_uvs[0], backward_uvs[1], backward_uvs[2], backward_uvs[3],
                # forward (12-15)
                forward_uvs[0], forward_uvs[1], forward_uvs[2], forward_uvs[3],
                # bottom (16-19)
                bottom_uvs[0], bottom_uvs[1], bottom_uvs[2], bottom_uvs[3],
                # top (20-23)
                top_uvs[0], top_uvs[1], top_uvs[2], top_uvs[3],
            ]

            uv_faces = [
                (0, 2, 1), (1, 3, 2),    # left
                (4, 6, 5), (5, 6, 7),    # right
                (9, 8, 11), (11, 8, 10), # backward
                (12, 14, 13), (13, 14, 15), # forward
                (16, 18, 17), (16, 19, 18), # bottom
                (22, 23, 20), (20, 23, 21), # top
            ]

            if self.skybox_texture is not None:
                self.skybox_texture.release()
            self.skybox_texture_path = texture_path
            img = Image.open(self.skybox_texture_path).convert("RGBA")
            img_data = np.array(img, dtype='u1')

            self.skybox_texture = self.ctx.texture(img.size, 4, img_data.tobytes())
            self.skybox_texture.use(location=1)  # bind to texture unit 0
            self.skybox_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
            self.skybox_texture.repeat_x = False
            self.skybox_texture.repeat_y = False
            self.compute_shader["skyTex"].value = 1 

            self.vertices_faces_list.append([verts.tolist(),faces,uvs,uv_faces, True, 0])
        

    def normalize(self, v):
        length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        if length == 0:
            return (0, 0, 0)
        return (v[0]/length, v[1]/length, v[2]/length)

    def cross(self, a, b):
        return (
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0]
        )

    def dot(self, a, b):
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

    def set_starting_shape(self, shape: str):
        self.current_shape = shape
        self.shapes = [self.current_shape]

    def set_use_default_shapes(self, use: bool):
        if use == self.is_using_default_shapes:
            return
        self.is_using_default_shapes = use
        if use:
            before = set(CUSTOM_SHAPES.keys())
            try:
                mod = importlib.import_module('.shapes', package=__package__)
                importlib.reload(mod)
            except Exception:
                return
            after = set(CUSTOM_SHAPES.keys())
            added = after - before
            self._default_shape_names.update(added)
            self._default_shapes_loaded = bool(self._default_shape_names)
        else:
            for name in list(self._default_shape_names):
                if name in CUSTOM_SHAPES:
                    del CUSTOM_SHAPES[name]
            self._default_shape_names.clear()
            self._default_shapes_loaded = False

    def shape_to_verticies_faces(self, matrix):
        faces = []
        uv = [(0, 0), (0, 1), (1, 0), (1, 1)]
        uv_faces = []

        if matrix is None or len(matrix) == 0 or len(matrix[0]) == 0:
            return [[], faces, uv, uv_faces]

        h = len(matrix)
        w = len(matrix[0])

        def idx(r, c):
            return r * w + c

        for r in range(h):
            row = matrix[r]
            for c in range(len(row)):
                point = row[c]
                if point is None:
                    continue

                if c < w - 1 and r < h - 1:
                    p1 = matrix[r][c + 1]
                    p2 = matrix[r + 1][c]
                    if p1 is not None and p2 is not None:
                        faces.append((idx(r, c), idx(r, c + 1), idx(r + 1, c)))
                        uv_faces.append((0, 1, 2))

                if c > 0 and r > 0:
                    p1 = matrix[r][c - 1]
                    p2 = matrix[r - 1][c]
                    if p1 is not None and p2 is not None:
                        faces.append((idx(r, c), idx(r, c - 1), idx(r - 1, c)))
                        uv_faces.append((3, 2, 1))

        verts = [p for row in matrix for p in row]
        return [verts, faces, uv, uv_faces, False, 0]


    def project_3d_to_2d(self, matrix, fov, camera_pos, camera_facing):
        projected = []
        #print(len(self.grid_coords_list))
        if matrix is None:
            return None
        # Cache trig values and projection factor per-call to avoid repeated math calls
        cos_y = math.cos(camera_facing[1])
        sin_y = math.sin(camera_facing[1])
        cos_x = math.cos(camera_facing[0])
        sin_x = math.sin(camera_facing[0])
        cos_z = math.cos(camera_facing[2])
        sin_z = math.sin(camera_facing[2])
        f = 1 / math.tan(fov / 2)
        for xIdx in range(len(matrix)):
            xList = matrix[xIdx]
            row = []
            for yIdx in range(len(xList)):
                point = xList[yIdx]

                if point is None:
                    row.append(None)
                    continue

                x = point[0]
                y = point[1]
                z = point[2]

                x -= camera_pos[0]
                y -= camera_pos[1]
                z -= camera_pos[2]

                x1 = x * cos_y + z * sin_y
                y1 = y
                z1 = -x * sin_y + z * cos_y

                x2 = x1
                y2 = y1 * cos_x - z1 * sin_x
                z2 = y1 * sin_x + z1 * cos_x

                x3 = x2 * cos_z - y2 * sin_z
                y3 = x2 * sin_z + y2 * cos_z
                z3 = z2

                if z3 <= -1 or abs(z3) < 1e-6:
                    row.append(None)
                    continue

                dd_x = (x3 * f) / -z3
                dd_y = (y3 * f) / -z3

                px = dd_x * self.half_w + self.half_w
                py = dd_y * self.half_h + self.half_h

                """margin = 5000
                if px < -margin or px > self.width + margin or py < -margin or py > self.height + margin:
                    row.append(None)
                    continue"""
                
                if self.render_type == renderer_type.MESH:
                    row.append((px, py))
                elif self.render_type == renderer_type.POLYGON_FILL:
                    row.append((px, py, z3))
                elif self.render_type == renderer_type.RASTERIZE:
                    row.append((px, py, z3))
            projected.append(row)

        return projected
    
    def project_3d_to_2d_flat(self, inList, fov, camera_pos, camera_facing, is_skybox):
        projected = []
        #print(len(self.grid_coords_list))
        if inList is None:
            return None
        # Cache trig values and projection factor per-call to avoid repeated math calls
        cos_y = math.cos(camera_facing[1])
        sin_y = math.sin(camera_facing[1])
        cos_x = math.cos(camera_facing[0])
        sin_x = math.sin(camera_facing[0])
        cos_z = math.cos(camera_facing[2])
        sin_z = math.sin(camera_facing[2])
        f = 1 / math.tan(fov / 2)
        for xIdx in range(len(inList)):
            point = inList[xIdx]

            if point is None:
                projected.append(None)
                continue

            x = point[0]
            y = point[1]
            z = point[2]

            if not is_skybox:
                x -= camera_pos[0]
                y -= camera_pos[1]
                z -= camera_pos[2]

            x1 = x * cos_y + z * sin_y
            y1 = y
            z1 = -x * sin_y + z * cos_y

            x2 = x1
            y2 = y1 * cos_x - z1 * sin_x
            z2 = y1 * sin_x + z1 * cos_x

            x3 = x2 * cos_z - y2 * sin_z
            y3 = x2 * sin_z + y2 * cos_z
            z3 = z2

            if z3 <= 0.1:
                projected.append(None)
                continue

            dd_x = (x3 * f) / -z3
            dd_y = (y3 * f) / -z3

            px = dd_x * self.half_w + self.half_w
            py = dd_y * self.half_h + self.half_h

            """margin = 1000
            if px < -margin or px > self.width + margin or py < -margin or py > self.height + margin:
                projected.append(None)
                continue"""
            
            if self.render_type == renderer_type.MESH:
                projected.append((px, py))
            elif self.render_type == renderer_type.POLYGON_FILL:
                projected.append((px, py, z3))
            elif self.render_type == renderer_type.RASTERIZE:
                projected.append((px, py, z3))

        return projected
    
    def render_wireframe(self, matrix):
        if self.render_type == renderer_type.MESH:
            if matrix is None:
                return
            for xIdx in range(len(matrix)):
                xList = matrix[xIdx]
                for yIdx in range(len(xList)):
                    point = xList[yIdx]
                    if point is not None:
                        points = []

                        try:
                            if xIdx < len(matrix) - 1 and matrix[xIdx+1][yIdx] is not None:
                                points.append(matrix[xIdx+1][yIdx])
                            if yIdx < len(xList) - 1 and matrix[xIdx][yIdx+1] is not None:
                                points.append(matrix[xIdx][yIdx+1])
                        except IndexError:
                            continue

                        for p in points:
                            pygame.draw.line(self.screen, (0, 0, 0), point, p, 2)
        elif self.render_type == renderer_type.POLYGON_FILL:
            all_tris = []
            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue
                tris = []

                #print(len(self.triangle_color_list_1))

                col1 = self.triangle_color_list_1[matI] if self.triangle_color_list_1[matI] is not None else self.triangle_base_color_1
                col2 = self.triangle_color_list_2[matI] if self.triangle_color_list_2[matI] is not None else self.triangle_base_color_2
                
                for xIdx in range(len(mat)):
                    xList = mat[xIdx]
                    for yIdx in range(len(xList)):
                        point = xList[yIdx]
                        if point is not None:

                            if xIdx < len(mat) - 1 and yIdx < len(xList) - 1:
                                p1 = mat[xIdx][yIdx + 1]
                                p2 = mat[xIdx + 1][yIdx]
                                if p1 is not None and p2 is not None:
                                    #pygame.draw.polygon(screen, (150, 0, 150), [point, p1, p2], 0)
                                    d1 = (point[2] + p1[2] + p2[2]) / 3 if len(point) > 2 else 0
                                    tris.append((d1, (point, p1, p2), col1))

                            if xIdx > 0 and yIdx > 0:
                                p1 = mat[xIdx][yIdx - 1]
                                p2 = mat[xIdx - 1][yIdx]
                                if p1 is not None and p2 is not None:
                                    #pygame.draw.polygon(screen, (50, 0, 50), [point, p1, p2], 0)
                                    d1 = (point[2] + p1[2] + p2[2]) / 3 if len(point) > 2 else 0
                                    tris.append((d1, (point, p1, p2), col2))
                all_tris.extend(tris)
            
            all_tris.sort(key=lambda t: t[0], reverse=True)

            for _, tri, col in all_tris:
                pygame.draw.polygon(
                    self.screen,
                    col,
                    [(tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])],
                    0,
                )

    def smax_poly(self, a, b, k):
        h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
        return self.mix(b, a, h) + k * h * (1.0 - h)
    
    def smax_exp(self, a, b, k):
        return np.log(np.exp(k * a) + np.exp(k * b)) / k

    def mix(self, a, b, t):
        return a * (1.0 - t) + b * t
    
    def interp_vert(self, v0, v1, t):
        return (
            v0[0] + t * (v1[0] - v0[0]),
            v0[1] + t * (v1[1] - v0[1]),
            v0[2] + t * (v1[2] - v0[2]),
        )
    def interp_uv(self, uv0, uv1, t):
        return (
            uv0[0] + t * (uv1[0] - uv0[0]),
            uv0[1] + t * (uv1[1] - uv0[1]),
        )
    def t_near(self, v_in, v_out, near):
        denom = v_out[2] - v_in[2]
        if abs(denom) < 1e-10:
            return 0.0
        return (near - v_in[2]) / denom
    
    def clip_triangle_near(self, verts_3d, uvs, near=0.1):

        inside  = [(v, uv) for v, uv in zip(verts_3d, uvs) if v[2] >= near]
        outside = [(v, uv) for v, uv in zip(verts_3d, uvs) if v[2] <  near]

        if len(inside) == 3:
            return [(verts_3d, uvs)]

        if len(inside) == 0:
            return []

        if len(inside) == 1:
            v0, uv0 = inside[0]
            v1, uv1 = outside[0]
            v2, uv2 = outside[1]
            t1 = self.t_near(v0, v1, near)
            t2 = self.t_near(v0, v2, near)
            p1 = self.interp_vert(v0, v1, t1);  puv1 = self.interp_uv(uv0, uv1, t1)
            p2 = self.interp_vert(v0, v2, t2);  puv2 = self.interp_uv(uv0, uv2, t2)
            return [([v0, p1, p2], [uv0, puv1, puv2])]

        if len(inside) == 2:
            v0, uv0 = inside[0]
            v1, uv1 = inside[1]
            v2, uv2 = outside[0]
            t1 = self.t_near(v0, v2, near)
            t2 = self.t_near(v1, v2, near)
            p1 = self.interp_vert(v0, v2, t1);  puv1 = self.interp_uv(uv0, uv2, t1)
            p2 = self.interp_vert(v1, v2, t2);  puv2 = self.interp_uv(uv1, uv2, t2)
            tri1 = ([v0, v1, p1], [uv0, uv1, puv1])
            tri2 = ([v1, p2, p1], [uv1, puv2, puv1])
            return [tri1, tri2]

        return []
    
    def cam(self, pt, is_skybox):
        if not is_skybox:
            x, y, z = pt[0]-self.camera.position[0], pt[1]-self.camera.position[1], pt[2]-self.camera.position[2]
        else:
            x, y, z = pt[0], pt[1], pt[2]
        cy, sy = math.cos(self.camera.rotation[1]), math.sin(self.camera.rotation[1])
        cx, sx = math.cos(self.camera.rotation[0]), math.sin(self.camera.rotation[0])
        cz, sz = math.cos(self.camera.rotation[2]), math.sin(self.camera.rotation[2])
        x1 = x*cy + z*sy;  z1 = -x*sy + z*cy
        x2 = x1;           y2 = y*cx - z1*sx;  z2 = y*sx + z1*cx
        x3 = x2*cz - y2*sz; y3 = x2*sz + y2*cz
        return (x3, y3, z2)

    def render_shape_from_obj_format(self, matrix, texture_p):
        #print(matrix[0][0])
        if self.render_type == renderer_type.RASTERIZE:
            self.depth_buffer.write(self.depth_init_data.tobytes())

            all_tris = []
            fov_rad = math.radians(self.camera.fov)

            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue

                vertices, faces, uv, uv_faces, is_skybox, texture_index = mat
                if self.using_obj_filetype_format:
                    unprojected_verticies, same_faces, same_uv, same_uv_faces, is_skybox1, texture_index1 = self.vertices_faces_list[matI]

                for faceI in range(len(faces)):
                    face = faces[faceI]

                    if self.using_obj_filetype_format:
                        up0 = unprojected_verticies[face[0]]
                        up1 = unprojected_verticies[face[1]]
                        up2 = unprojected_verticies[face[2]]
                        if None in (up0, up1, up2):
                            continue

                    uv_face = uv_faces[faceI]
                    uv0 = uv[uv_face[0]]
                    uv1 = uv[uv_face[1]]
                    uv2 = uv[uv_face[2]]
                    
                    if self.using_obj_filetype_format:
                        unprojected_normal = self.normalT_camera_space((up0, up1, up2))
                        light_dir = np.array([0, 1, 0])
                        light_m = max(self.lighting_strictness, np.dot(light_dir, np.array(unprojected_normal)))

                        cam0, cam1, cam2 = self.cam(up0, is_skybox), self.cam(up1, is_skybox), self.cam(up2, is_skybox)

                        clipped = self.clip_triangle_near([cam0, cam1, cam2], [uv0, uv1, uv2], near=0.1)

                        for clipped_verts, clipped_uvs in clipped:
                            def proj(v):
                                f = 1.0 / math.tan(fov_rad / 2)
                                return (
                                    (v[0] * f / -v[2]) * self.half_w + self.half_w,
                                    (v[1] * f / -v[2]) * self.half_h + self.half_h,
                                    v[2]
                                )
                            pp0, pp1, pp2 = proj(clipped_verts[0]), proj(clipped_verts[1]), proj(clipped_verts[2])
                            all_tris.append((
                                (pp0[2], pp1[2], pp2[2]),
                                (pp0, pp1, pp2),
                                clipped_uvs[0], clipped_uvs[1], clipped_uvs[2],
                                light_m, is_skybox, texture_index
                            ))
                    else:
                        p0 = vertices[face[0]]
                        p1 = vertices[face[1]]
                        p2 = vertices[face[2]]
                        if not (p0[2] < 0 or p1[2] < 0 or p2[2] < 0):
                            all_tris.append((
                                (p0[2], p1[2], p2[2]),
                                (p0, p1, p2),
                                uv0, uv1, uv2,
                                1, is_skybox, texture_index
                            ))

            n = len(all_tris)
            if n == 0:
                return

            data = np.zeros(n, dtype=tri_dtype)
            for i, (depths, tri, uv1, uv2, uv3, light_m, is_skybox, tri_tex_index) in enumerate(all_tris):
                p0, p1, p2 = tri
                data[i]['pos'] = ((p0[0], p0[1]), (p1[0], p1[1]), (p2[0], p2[1]))
                data[i]['depths'] = depths
                if not is_skybox:
                    if None in (uv1, uv2, uv3) or self.texture == None:
                        data[i]['uv'] = ((-1.0, -1.0), (-1.0, -1.0), (-1.0, -1.0))
                        data[i]['light_mult'] = 1
                        data[i]["is_skybox"] = 0
                        data[i]["texture_index"] = tri_tex_index
                    else:
                        data[i]['uv'] = (uv1, uv2, uv3)
                        data[i]['light_mult'] = light_m
                        data[i]["is_skybox"] = 0
                        data[i]["texture_index"] = tri_tex_index
                else:
                    if None in (uv1, uv2, uv3) or self.skybox_texture == None:
                        data[i]['uv'] = ((-1.0, -1.0), (-1.0, -1.0), (-1.0, -1.0))
                        data[i]['light_mult'] = 1
                        data[i]["is_skybox"] = 0
                    else:
                        data[i]['uv'] = (uv1, uv2, uv3)
                        data[i]['light_mult'] = 1
                        data[i]["is_skybox"] = 1
                

            self.tri_buffer.write(data.tobytes())
            self.tri_buffer.bind_to_storage_buffer(0, offset=0, size=data.nbytes)

            self.depth_buffer.bind_to_storage_buffer(1)
            self.output_tex.bind_to_image(0, read=False, write=True)

            self.compute_shader['tri_count'].value = n

            self.output_tex.write(self._output_clear_rgba.tobytes())
            self.compute_shader.run((self.width + 15) // 16, (self.height + 15) // 16)
            
            raw_data = self.output_tex.read()
            img_array = np.frombuffer(raw_data, dtype='f4').reshape((self.height, self.width, 4))
            img_uint8 = (img_array * 255).astype('uint8')
            
            image_surface = pygame.image.frombuffer(img_uint8.tobytes(), (self.width, self.height), 'RGBA')
            self.screen.blit(image_surface, (0, 0))


        elif self.render_type == renderer_type.POLYGON_FILL:
            all_tris = []
            s = True
            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue
                vertices, faces, *_ = mat
                unprojected_verticies, same_faces, *_  = self.vertices_faces_list[matI]
                for face in faces:
                    p0 = vertices[face[0]]
                    p1 = vertices[face[1]]
                    p2 = vertices[face[2]]

                    up0 = unprojected_verticies[face[0]]
                    up1 = unprojected_verticies[face[1]]
                    up2 = unprojected_verticies[face[2]]
                    if None in (p0, p1, p2):
                        continue
                    if p0[2] <= 0.1 or p1[2] <= 0.1 or p2[2] <= 0.1:
                        continue

                    # Consistent depth: average of projected Z
                    depth = max(p0[2], p1[2], p2[2])
                    unprojected_normal = self.normalT_camera_space((up0, up1, up2))
                    # Only cull if normal clearly faces away — flip sign if needed
                    up0,up1,up2 = self.to_cam_space(up0), self.to_cam_space(up1), self.to_cam_space(up2)
                    if None in (up0, up1, up2):
                        continue
                    normal = self.normalT_camera_space((up0, up1, up2))

                    """if normal[2] >= 0:
                        continue"""
                    if unprojected_normal[0] > 0:
                        col = (255, 0, 0)
                    elif unprojected_normal[0] < 0:
                        col = (155, 0, 0)
                    elif unprojected_normal[1] > 0:
                        col = (0, 255, 0)
                    elif unprojected_normal[1] < 0:
                        col = (0, 155, 0)
                    elif unprojected_normal[2] > 0:
                        col = (0, 0, 255)
                    elif unprojected_normal[2] < 0:
                        col = (0, 0, 155)

                    view_dir = (0, 0, 1)  # if camera faces +Z in camera space
                    dot = normal[0]*view_dir[0] + normal[1]*view_dir[1] + normal[2]*view_dir[2]
                    """if dot >= 0:
                        continue"""

                    #col = self.triangle_base_color_1 if s else self.triangle_base_color_2
                    s = not s
                    all_tris.append((depth, (p0, p1, p2), col))

            all_tris.sort(key=lambda t: t[0], reverse=True)
            for _, tri, col in all_tris:
                pygame.draw.polygon(self.screen, col, [(v[0], v[1]) for v in tri], 0)
        elif self.render_type == renderer_type.MESH:
            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue
                vertices, faces, *_  = mat
                # Try to get the original 3D vertices for proper backface culling
                unprojected_vertices = None
                if matI < len(self.vertices_faces_list):
                    try:
                        unprojected_vertices, _ = self.vertices_faces_list[matI]
                    except Exception:
                        unprojected_vertices = None

                for face in faces:
                    p0 = vertices[face[0]]
                    p1 = vertices[face[1]]
                    p2 = vertices[face[2]]
                    if None in (p0, p1, p2):
                        continue

                    # Backface culling: if we have original 3D verts, compute normal in camera space
                    # and skip faces that face away from the camera.
                    skip_face = False
                    if unprojected_vertices is not None:
                        up0 = unprojected_vertices[face[0]]
                        up1 = unprojected_vertices[face[1]]
                        up2 = unprojected_vertices[face[2]]
                        if None in (up0, up1, up2):
                            skip_face = True
                        else:
                            cu0 = self.to_cam_space(up0)
                            cu1 = self.to_cam_space(up1)
                            cu2 = self.to_cam_space(up2)
                            if None in (cu0, cu1, cu2):
                                skip_face = True
                            else:
                                normal = self.normalT_camera_space((cu0, cu1, cu2))
                                # If normal's Z component faces away (positive), cull
                                """if normal[2] >= 0:
                                    skip_face = True"""

                    if skip_face:
                        continue

                    pygame.draw.line(self.screen, (0, 0, 0), p0, p1, 2)
                    pygame.draw.line(self.screen, (0, 0, 0), p1, p2, 2)
                    pygame.draw.line(self.screen, (0, 0, 0), p2, p0, 2)
    


    def normalize(self, v):
        return v / np.linalg.norm(v)

    def depth_in_tri(self, tri, point, depths):
        t_p0 = tri[0]
        t_p1 = tri[1]
        t_p2 = tri[2]
        # Compute barycentric weights using triangle sub-areas, then interpolate depth.
        # weight for p0 = area(p1,p2,P) / area(p0,p1,p2)
        a0 = self.tri_area(t_p1, t_p2, point)
        a1 = self.tri_area(t_p2, t_p0, point)
        a2 = self.tri_area(t_p0, t_p1, point)

        total = self.tri_area(t_p0, t_p1, t_p2)
        if total == 0:
            return math.inf

        w0 = a0 / total
        w1 = a1 / total
        w2 = a2 / total

        depth = w0 * depths[0] + w1 * depths[1] + w2 * depths[2]

        return depth

    def tri_area(self, p1, p2, p3):
        x1 = p1[0]
        x2 = p2[0]
        x3 = p3[0]
        y1 = p1[1]
        y2 = p2[1]
        y3 = p3[1]
        return 0.5 * abs(x1*(y2-y3)+x2*(y3-y1)+x3*(y1-y2))

    def dot(self, p1, p2, p3):
        tri_vec = (p2[0] - p1[0], p2[1] - p1[1])
        other_vec = (p3[0] - p1[0], p3[1] - p1[1])

        rotated_vec = (tri_vec[1], -tri_vec[0])

        return other_vec[0] * rotated_vec[0] + other_vec[1] * rotated_vec[1]

    
    def is_point_inside_triangle(self, p0, p1, p2, point):
        #print(p0,p1,p2)
        d1 = self.dot(p0, p1, point)
        d2 = self.dot(p1, p2, point)
        d3 = self.dot(p2, p0, point)

        if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
            return True
        
        return False

    def to_cam_space(self, point):
        x = point[0]
        y = point[1]
        z = point[2]

        x -= self.camera.position[0]
        y -= self.camera.position[1]
        z -= self.camera.position[2]

        x1 = x * math.cos(self.camera.rotation[1]) + z * math.sin(self.camera.rotation[1])
        y1 = y
        z1 = -x * math.sin(self.camera.rotation[1]) + z * math.cos(self.camera.rotation[1])

        x2 = x1
        y2 = y1 * math.cos(self.camera.rotation[0]) - z1 * math.sin(self.camera.rotation[0])
        z2 = y1 * math.sin(self.camera.rotation[0]) + z1 * math.cos(self.camera.rotation[0])

        x3 = x2 * math.cos(self.camera.rotation[2]) - y2 * math.sin(self.camera.rotation[2])
        y3 = x2 * math.sin(self.camera.rotation[2]) + y2 * math.cos(self.camera.rotation[2])
        z3 = z2

        if z3 <= 0.1:
            return None

        return (x3, y3, z3)

    def normalT_camera_space(self, tri):
        p0, p1, p2 = tri
        edge1 = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
        edge2 = (p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2])
        nx = edge1[1]*edge2[2] - edge1[2]*edge2[1]
        ny = edge1[2]*edge2[0] - edge1[0]*edge2[2]
        nz = edge1[0]*edge2[1] - edge1[1]*edge2[0]
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length == 0:
            return (0, 0, 0)
        return (nx/length, ny/length, nz/length)
    
    def generate_shape(self, shape_name, time=0):
        if shape_name in CUSTOM_SHAPES:
            shape_info = CUSTOM_SHAPES[shape_name]
            func = shape_info['function']
            color = shape_info['color']

            if color is not None:
                self.triangle_color_list_2.append((color[0]*0.75, color[1]*0.75, color[2]*0.75))
            else:
                self.triangle_color_list_2.append(None)

            self.triangle_color_list_1.append(color)
            
            
            if shape_info['is_animated']:
                return func(time=time), True
            else:
                return func(), False
        
        return None, False
    
    def generate_shape_from_key_press(self, pressedKeys, time=0):
        shapesList = []
        for shape, value in CUSTOM_SHAPES.items():
            key = value['key']
            if key is not None:
                if pressedKeys[key]:
                    shapesList.append(shape)
        
        if len(shapesList) >= 1:
            self.shapes = shapesList
        
    def min_z(self, lvl1):
        values = [
            t[2]
            for lvl2 in lvl1
            for t in lvl2
            if t is not None
        ]
        return max(values) if values else float("-inf")

    def run(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))
            self.clock.tick(60)
            self.animation_time += 0.01
            # Precompute FOV radians once per frame
            fov_rad = math.radians(self.camera.fov)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                self.camera.handle_mouse_events(event)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            
            self.camera.update(keys)
            
            self.generate_shape_from_key_press(keys, self.animation_time)
            if not self.using_obj_filetype_format:
                for i in range(len(self.shapes)):
                    shape_name = self.shapes[i]
                    #print(shape_name)
                    self.grid_coords_list.append(self.generate_shape(shape_name, self.animation_time))

                for i in range(len(self.grid_coords_list)):
                    self.grid_coords = self.grid_coords_list[i]
                    if self.grid_coords:
                        projected = self.project_3d_to_2d(
                            self.grid_coords[0],
                            fov_rad,
                            tuple(self.camera.position),
                            tuple(self.camera.rotation)
                        )
                        self.projections_list.append(projected)

                if self.render_type == renderer_type.POLYGON_FILL:
                    self.render_wireframe(self.projections_list)
                elif self.render_type == renderer_type.MESH:
                    for proj in self.projections_list:
                        self.render_wireframe(proj)
                elif self.render_type == renderer_type.RASTERIZE:
                    self.projected_vertices_faces_list = [
                        self.shape_to_verticies_faces(proj)
                        for proj in self.projections_list
                    ]
                    self.render_shape_from_obj_format(self.projected_vertices_faces_list, self.texture_path)
            else:
                if self.render_type == renderer_type.RASTERIZE:
                    for i in range(len(self.vertices_faces_list)):
                        projected = self.project_3d_to_2d_flat(
                                self.vertices_faces_list[i][0],
                                fov_rad,
                                tuple(self.camera.position),
                                tuple(self.camera.rotation),
                                self.vertices_faces_list[i][4]
                            )
                        self.projected_vertices_faces_list.append([projected, self.vertices_faces_list[i][1], self.vertices_faces_list[i][2], self.vertices_faces_list[i][3], self.vertices_faces_list[i][4], self.vertices_faces_list[i][5]])
                    #if not self.is_mesh:
                    self.render_shape_from_obj_format(self.projected_vertices_faces_list, self.texture_path)

            self.grid_coords_list = []
            self.triangle_color_list_1 = []
            self.triangle_color_list_2 = []
            self.projections_list = []
            self.projected_vertices_faces_list = []


            pygame.display.update()
        
        pygame.quit()

    def loopable_run(self):
        self.screen.fill((255, 255, 255))
        self.clock.tick(60)
        self.animation_time += 0.01
        # Precompute FOV radians once per frame
        fov_rad = math.radians(100)
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                
            self.camera.handle_mouse_events(event)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        
        self.camera.update(keys)
        
        self.generate_shape_from_key_press(keys, self.animation_time)

        if not self.using_obj_filetype_format:
            for i in range(len(self.shapes)):
                shape_name = self.shapes[i]
                #print(shape_name)
                self.grid_coords_list.append(self.generate_shape(shape_name, self.animation_time))

            for i in range(len(self.grid_coords_list)):
                self.grid_coords = self.grid_coords_list[i]
                if self.grid_coords:
                    projected = self.project_3d_to_2d(
                        self.grid_coords[0],
                        fov_rad,
                        tuple(self.camera.position),
                        tuple(self.camera.rotation)
                    )
                    self.projections_list.append(projected)

            if self.render_type == renderer_type.POLYGON_FILL:
                self.render_wireframe(self.projections_list)
            elif self.render_type == renderer_type.MESH:
                for proj in self.projections_list:
                    self.render_wireframe(proj)
            elif self.render_type == renderer_type.RASTERIZE:
                self.projected_vertices_faces_list = [
                    self.shape_to_verticies_faces(proj)
                    for proj in self.projections_list
                ]
                self.render_shape_from_obj_format(self.projected_vertices_faces_list, self.texture_path)
        else:
            for i in range(len(self.vertices_faces_list)):
                projected = self.project_3d_to_2d_flat(
                        self.vertices_faces_list[i][0],
                        fov_rad,
                        tuple(self.camera.position),
                        tuple(self.camera.rotation),
                        self.vertices_faces_list[i][4]
                    )
                self.projected_vertices_faces_list.append([projected, self.vertices_faces_list[i][1], self.vertices_faces_list[i][2], self.vertices_faces_list[i][3], self.vertices_faces_list[i][4], self.vertices_faces_list[i][5]])
            #if not self.is_mesh:
            self.render_shape_from_obj_format(self.projected_vertices_faces_list, self.texture_path)

        self.grid_coords_list = []
        self.triangle_color_list_1 = []
        self.triangle_color_list_2 = []
        self.projections_list = []
        self.projected_vertices_faces_list = []
        
        pygame.display.update()
        


def main():
    renderer = Renderer3D()
    renderer.run()


if __name__ == "__main__":
    main()