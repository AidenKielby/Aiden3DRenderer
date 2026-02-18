"""
Main 3D renderer class
"""
import math
import pygame
from pygame import QUIT
import sys

from .camera import Camera

CUSTOM_SHAPES = {}

def register_shape(name: str, key=None, is_animated: bool = False):
    def decorator(func):
        CUSTOM_SHAPES[name] = {
            'function': func,
            'is_animated': is_animated,
            'key': key
        }
        return func
    return decorator


class Renderer3D:
    
    def __init__(self, width=1000, height=1000, title="Aiden 3D Renderer"):
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
        self.shapes = ["mountain"]
        self.projected = None

        self.is_starting = True

        self.is_mesh = True
        self.triangle_color_1= (150, 0, 150)
        self.triangle_color_2 = (50, 0, 50)

        self.grid_coords_list = []
        self.projections_list = []
        
    def project_3d_to_2d(self, matrix, fov, camera_pos, camera_facing):
        projected = []
        
        for xIdx in range(len(matrix)):
            xList = matrix[xIdx]
            row = []
            for yIdx in range(len(xList)):
                point = xList[yIdx]
                #print(point)
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
                
                if self.is_mesh:
                    row.append((px, py))
                else:
                    row.append((px, py, z3))
            projected.append(row)

        return projected
    
    def render_wireframe(self, matrix):
        if self.is_mesh:
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
            for mat in matrix:
                tris = []
                
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
                                    tris.append((d1, (point, p1, p2), self.triangle_color_1))

                            if xIdx > 0 and yIdx > 0:
                                p1 = mat[xIdx][yIdx - 1]
                                p2 = mat[xIdx - 1][yIdx]
                                if p1 is not None and p2 is not None:
                                    #pygame.draw.polygon(screen, (50, 0, 50), [point, p1, p2], 0)
                                    d1 = (point[2] + p1[2] + p2[2]) / 3 if len(point) > 2 else 0
                                    tris.append((d1, (point, p1, p2), self.triangle_color_2))
                all_tris.extend(tris)
            
            all_tris.sort(key=lambda t: t[0], reverse=True)

            for _, tri, col in all_tris:
                pygame.draw.polygon(
                    self.screen,
                    col,
                    [(tri[0][0], tri[0][1]), (tri[1][0], tri[1][1]), (tri[2][0], tri[2][1])],
                    0,
                )
    
    def generate_shape(self, shape_name, time=0):
        if shape_name in CUSTOM_SHAPES:
            shape_info = CUSTOM_SHAPES[shape_name]
            func = shape_info['function']
            
            if shape_info['is_animated']:
                return func(time=time), True
            else:
                return func(), False
        
        return None, False
    
    def generate_shape_from_key_press(self, pressedKeys, time=0):
        shapesList = []
        for shape, value in CUSTOM_SHAPES.items():
            key = value['key']
            if pressedKeys[key]:
                shapesList.append(shape)
        
        if len(shapesList) >= 1:
            self.shapes = shapesList
        """if self.needs_regen or self.is_starting:
            self.grid_coords, self.needs_regen = self.generate_shape(
                        self.current_shape, 
                        self.animation_time,
                )
            
            self.is_starting = False"""
        
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
            all_tris = []
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

            self.grid_coords_list = []

            for i in range(len(self.shapes)):
                shape_name = self.shapes[i]
                #print(shape_name)
                self.grid_coords_list.append(self.generate_shape(shape_name, self.animation_time))

            
            self.projections_list = []

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

        self.grid_coords_list = []

        for i in range(len(self.shapes)):
            shape_name = self.shapes[i]
            #print(shape_name)
            self.grid_coords_list.append(self.generate_shape(shape_name, self.animation_time))

        
        self.projections_list = []

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
        
        pygame.display.update()
        


def main():
    renderer = Renderer3D()
    renderer.run()


if __name__ == "__main__":
    main()
