"""
Main 3D renderer class
"""
import math
import pygame
from pygame import QUIT
import sys
import importlib

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

        self.is_mesh = True
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

    def project_3d_to_2d(self, matrix, fov, camera_pos, camera_facing):
        projected = []
        #print(len(self.grid_coords_list))
        if matrix is None:
            return None
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

                x1 = x * math.cos(camera_facing[1]) + z * math.sin(camera_facing[1])
                y1 = y
                z1 = -x * math.sin(camera_facing[1]) + z * math.cos(camera_facing[1])

                x2 = x1
                y2 = y1 * math.cos(camera_facing[0]) - z1 * math.sin(camera_facing[0])
                z2 = y1 * math.sin(camera_facing[0]) + z1 * math.cos(camera_facing[0])

                x3 = x2 * math.cos(camera_facing[2]) - y2 * math.sin(camera_facing[2])
                y3 = x2 * math.sin(camera_facing[2]) + y2 * math.cos(camera_facing[2])
                z3 = z2

                if z3 <= 0.1:
                    row.append(None)
                    continue

                f = 1 / math.tan(fov / 2)
                dd_x = (x3 * f) / -z3
                dd_y = (y3 * f) / -z3

                px = dd_x * self.half_w + self.half_w
                py = dd_y * self.half_h + self.half_h

                margin = 1000
                if px < -margin or px > self.width + margin or py < -margin or py > self.height + margin:
                    row.append(None)
                    continue
                
                if self.is_mesh:
                    row.append((px, py))
                else:
                    row.append((px, py, z3))
            projected.append(row)

        return projected
    
    def project_3d_to_2d_flat(self, inList, fov, camera_pos, camera_facing):
        projected = []
        #print(len(self.grid_coords_list))
        if inList is None:
            return None
        for xIdx in range(len(inList)):
            point = inList[xIdx]

            if point is None:
                projected.append(None)
                continue

            x = point[0]
            y = point[1]
            z = point[2]

            x -= camera_pos[0]
            y -= camera_pos[1]
            z -= camera_pos[2]

            x1 = x * math.cos(camera_facing[1]) + z * math.sin(camera_facing[1])
            y1 = y
            z1 = -x * math.sin(camera_facing[1]) + z * math.cos(camera_facing[1])

            x2 = x1
            y2 = y1 * math.cos(camera_facing[0]) - z1 * math.sin(camera_facing[0])
            z2 = y1 * math.sin(camera_facing[0]) + z1 * math.cos(camera_facing[0])

            x3 = x2 * math.cos(camera_facing[2]) - y2 * math.sin(camera_facing[2])
            y3 = x2 * math.sin(camera_facing[2]) + y2 * math.cos(camera_facing[2])
            z3 = z2

            if z3 <= 0.1:
                projected.append(None)
                continue

            f = 1 / math.tan(fov / 2)
            dd_x = (x3 * f) / -z3
            dd_y = (y3 * f) / -z3

            px = dd_x * self.half_w + self.half_w
            py = dd_y * self.half_h + self.half_h

            margin = 1000
            if px < -margin or px > self.width + margin or py < -margin or py > self.height + margin:
                projected.append(None)
                continue
            
            if self.is_mesh:
                projected.append((px, py))
            else:
                projected.append((px, py, z3))

        return projected
    
    def render_wireframe(self, matrix):
        if self.is_mesh:
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
        else:
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

    def render_shape_from_obj_format(self, matrix):
        if not self.is_mesh:
            all_tris = []
            s = True
            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue
                vertices, faces = mat
                unprojected_verticies, same_faces = self.vertices_faces_list[matI]
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

                    if normal[2] >= 0:
                        continue
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
                    if dot >= 0:
                        continue

                    #col = self.triangle_base_color_1 if s else self.triangle_base_color_2
                    s = not s
                    all_tris.append((depth, (p0, p1, p2), col))

            all_tris.sort(key=lambda t: t[0], reverse=True)
            for _, tri, col in all_tris:
                pygame.draw.polygon(self.screen, col, [(v[0], v[1]) for v in tri], 0)
        else:
            for matI in range(len(matrix)):
                mat = matrix[matI]
                if mat is None:
                    continue
                vertices, faces = mat
                for face in faces:
                    p0 = vertices[face[0]]
                    p1 = vertices[face[1]]
                    p2 = vertices[face[2]]
                    if None in (p0, p1, p2):
                        continue

                    pygame.draw.line(self.screen, (0, 0, 0), p0, p1, 2)
                    pygame.draw.line(self.screen, (0, 0, 0), p1, p2, 2)
                    pygame.draw.line(self.screen, (0, 0, 0), p2, p0, 2)

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
                            math.radians(100),
                            tuple(self.camera.position),
                            tuple(self.camera.rotation)
                        )
                        self.projections_list.append(projected)

                if not self.is_mesh:
                    self.render_wireframe(self.projections_list)
                else:
                    for proj in self.projections_list:
                        self.render_wireframe(proj)
            else:
                for i in range(len(self.vertices_faces_list)):
                    projected = self.project_3d_to_2d_flat(
                            self.vertices_faces_list[i][0],
                            math.radians(100),
                            tuple(self.camera.position),
                            tuple(self.camera.rotation)
                        )
                    self.projected_vertices_faces_list.append([projected, self.vertices_faces_list[i][1]])
                #if not self.is_mesh:
                self.render_shape_from_obj_format(self.projected_vertices_faces_list)

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
                        math.radians(100),
                        tuple(self.camera.position),
                        tuple(self.camera.rotation)
                    )
                    self.projections_list.append(projected)

            if not self.is_mesh:
                self.render_wireframe(self.projections_list)
            else:
                for proj in self.projections_list:
                    self.render_wireframe(proj)
        else:
            for i in range(len(self.vertices_faces_list)):
                projected = self.project_3d_to_2d_flat(
                        self.vertices_faces_list[i][0],
                        math.radians(100),
                        tuple(self.camera.position),
                        tuple(self.camera.rotation)
                    )
                self.projected_vertices_faces_list.append([projected, self.vertices_faces_list[i][1]])
            #if not self.is_mesh:
            self.render_shape_from_obj_format(self.projected_vertices_faces_list)

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
