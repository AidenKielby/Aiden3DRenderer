import dis
import math
import random
import pygame
from .renderer import Renderer3D
from . import shapes

class ShapePhysicsObject:
    def __init__(self, renderer: Renderer3D, shape: str, rotation: tuple[float], color: tuple[int], size: float, mass: float, grid_size: float):
        self.renderer = renderer
        valid_shapes = ["sphere", "plane"]
        if shape not in valid_shapes:
            raise ValueError(f"Invalid Input '{shape}'. expected one of {valid_shapes}")
        
        self.shape = shape
        self.mass = mass
        self.grid_size = grid_size
        self.grid_coords = None
        self.rotation = rotation

        self.color = color

        self.forces = [0, 0, 0]
        self.anchor_position = [0, 0, 0]
        self.velocity = [0, 0, 0]
        self.timeStep = 1
        self.size = size

        if shape == "sphere":
            self.grid_coords = shapes.generate_sphere(resolution=grid_size, radius=size)
        elif shape == "plane":
            self.mass = float("inf")
            self.grid_coords = shapes.generate_plane(size=size, rot_x=math.radians(rotation[0]), rot_y=math.radians(rotation[1]), rot_z=math.radians(rotation[2]))
            #self.anchor_position = self.rotate_xyz(self.anchor_position, math.radians(rotation[0]), math.radians(rotation[1]), math.radians(rotation[2]))


            # --- Compute plane normal from first 3 vertices ---
            p0 = self.grid_coords[0][0]
            p1 = self.grid_coords[0][1]
            p2 = self.grid_coords[1][0]

            # Edge vectors
            e1 = (p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2])
            e2 = (p2[0]-p0[0], p2[1]-p0[1], p2[2]-p0[2])

            # Cross product
            nx = e1[1]*e2[2] - e1[2]*e2[1]
            ny = e1[2]*e2[0] - e1[0]*e2[2]
            nz = e1[0]*e2[1] - e1[1]*e2[0]

            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            if length != 0:
                nx /= length
                ny /= length
                nz /= length

            self.plane_normal = (nx, ny, nz)
            self.plane_point = p0

    def rotate_xyz(self, pos, rx, ry, rz):
        x, y, z = pos

        # Rotate X
        cosx, sinx = math.cos(rx), math.sin(rx)
        y, z = y*cosx - z*sinx, y*sinx + z*cosx

        # Rotate Y
        cosy, siny = math.cos(ry), math.sin(ry)
        x, z = x*cosy + z*siny, -x*siny + z*cosy

        # Rotate Z
        cosz, sinz = math.cos(rz), math.sin(rz)
        x, y = x*cosz - y*sinz, x*sinz + y*cosz

        return [x, y, z]

    def add_forces(self, force: tuple[float]):
        self.forces[0] += force[0]
        self.forces[1] += force[1]
        self.forces[2] += force[2]

    def set_forces(self, force: tuple[float]):
        self.forces[0] = force[0]
        self.forces[1] = force[1]
        self.forces[2] = force[2]

    def update_velocity_from_forces(self):
        last_velocity = self.velocity[:]
        self.velocity[0] = last_velocity[0] + (self.forces[0]/self.mass) * self.timeStep
        self.velocity[1] = last_velocity[1] + (self.forces[1]/self.mass) * self.timeStep
        self.velocity[2] = last_velocity[2] + (self.forces[2]/self.mass) * self.timeStep
        
    def update_pos_from_velocity(self):
        last_anchor_pos = self.anchor_position[:]
        self.anchor_position[0] = last_anchor_pos[0] + self.velocity[0]
        self.anchor_position[1] = last_anchor_pos[1] + self.velocity[1]
        self.anchor_position[2] = last_anchor_pos[2] + self.velocity[2]

    def apply_anchor_position_to_grid_coords(self):
        new_coords = []
        for y in range(len(self.grid_coords)):
            yGrid = self.grid_coords[y]
            new_coords1 = []
            for x in range(len(yGrid)):

                new_coords1.append(
                    (
                        self.grid_coords[y][x][0] + self.anchor_position[0],
                        self.grid_coords[y][x][1] + self.anchor_position[1],
                        self.grid_coords[y][x][2] + self.anchor_position[2]
                    )
                )

            new_coords.append(new_coords1)
        
        return new_coords

    def add_shape_to_renderer(self):
        new_coords = self.apply_anchor_position_to_grid_coords()
        self.renderer.grid_coords_list.append((new_coords, True))

    def add_color_to_renderer(self):
        self.renderer.triangle_color_list_1.append(self.color)
        self.renderer.triangle_color_list_2.append((self.color[0] * 0.75, self.color[1] * 0.75, self.color[2] * 0.75))

    def detect_collision(self, shapes: list["ShapePhysicsObject"]):
        if self.shape == "plane":
            return
        #print(shapes)
        for shapeI in range(len(shapes)):
            #print(shapeI)
            shape = shapes[shapeI]

            if shape.shape == "sphere":
                this_center_point = (self.anchor_position[0], self.anchor_position[1] - self.size, self.anchor_position[2])
                other_center_point = (shape.anchor_position[0], shape.anchor_position[1] - shape.size, shape.anchor_position[2])
                
                dx = this_center_point[0]-other_center_point[0]
                dy = this_center_point[1]-other_center_point[1]
                dz = this_center_point[2]-other_center_point[2]

                dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2) + math.pow(dz, 2))

                if dist <= self.size + shape.size:
                    if dist == 0:
                        continue
                    nx = dx / dist
                    ny = dy / dist
                    nz = dz / dist
                    self.handle_collision(shape, (nx, ny, nz))
            
            elif shape.shape == "plane":
                # Sphere center
                center = (
                    self.anchor_position[0],
                    self.anchor_position[1] - self.size,
                    self.anchor_position[2]
                )

                # Use plane's anchor_position and normal
                plane_world_point = (
                    shape.plane_point[0] + shape.anchor_position[0],
                    shape.plane_point[1] + shape.anchor_position[1],
                    shape.plane_point[2] + shape.anchor_position[2]
                )
                n = shape.plane_normal

                px = center[0] - plane_world_point[0]
                py = center[1] - plane_world_point[1]
                pz = center[2] - plane_world_point[2]
                dist = px*n[0] + py*n[1] + pz*n[2]

                # print("shape: ", shape.shape, "dist: ", dist)

                if abs(dist) <= self.size:
                    vn = self.velocity[0]*n[0] + \
                        self.velocity[1]*n[1] + \
                        self.velocity[2]*n[2]

                    if dist * vn < 0:
                        # Reflect
                        self.velocity[0] -= 2 * vn * n[0]
                        self.velocity[1] -= 2 * vn * n[1]
                        self.velocity[2] -= 2 * vn * n[2]

                        # Positional correction
                        penetration = self.size - abs(dist)
                        sign = 1 if dist > 0 else -1

                        self.anchor_position[0] += n[0] * penetration * sign
                        self.anchor_position[1] += n[1] * penetration * sign
                        self.anchor_position[2] += n[2] * penetration * sign
            
    def handle_collision(self, other_shape: "ShapePhysicsObject", n):
        if other_shape.shape == "sphere":
            rvx = self.velocity[0] - other_shape.velocity[0]
            rvy = self.velocity[1] - other_shape.velocity[1]
            rvz = self.velocity[2] - other_shape.velocity[2]

            # --- Velocity along normal (dot product) ---
            vel_along_normal = rvx*n[0] + rvy*n[1] + rvz*n[2]

            # If objects are separating, do nothing
            if vel_along_normal > 0:
                return

            m1 = self.mass
            m2 = other_shape.mass

            # --- Compute impulse scalar ---
            j = (2 * vel_along_normal) / (m1 + m2)

            # --- Store old velocities ---
            v1x, v1y, v1z = self.velocity
            v2x, v2y, v2z = other_shape.velocity

            # --- Apply impulse ---
            self.velocity[0] = v1x - j * m2 * n[0]
            self.velocity[1] = v1y - j * m2 * n[1]
            self.velocity[2] = v1z - j * m2 * n[2]

            other_shape.velocity[0] = v2x + j * m1 * n[0]
            other_shape.velocity[1] = v2y + j * m1 * n[1]
            other_shape.velocity[2] = v2z + j * m1 * n[2]
        elif other_shape.shape == "plane":
            n = other_shape.plane_normal

            # Dot product
            vn = self.velocity[0]*n[0] + \
                self.velocity[1]*n[1] + \
                self.velocity[2]*n[2]

            # Reflect velocity
            self.velocity[0] -= 2 * vn * n[0]
            self.velocity[1] -= 2 * vn * n[1]
            self.velocity[2] -= 2 * vn * n[2]


class PhysicsObjectHandler:
    def __init__(self):
        self.shapes: list[ShapePhysicsObject] = []
    
    def add_shape(self, shape: ShapePhysicsObject):
        self.shapes.append(shape)

    def handle_shapes(self):
        for shape in self.shapes:
            #print(shape.shape)
            shape.update_velocity_from_forces()
            shape.update_pos_from_velocity()
            shape.detect_collision(self.shapes)
            shape.add_shape_to_renderer()
            shape.add_color_to_renderer()
            shape.forces = [0,0,0]


