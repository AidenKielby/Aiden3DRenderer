import numpy as np
import math

class Entity:
    def __init__(self, model, renderer, start_velocity=(0,0,0), starting_rotation=(0,0,0)):
        self.model = model
        self.scripts: list[str] = []
        self.velocity = start_velocity
        self.rotation = starting_rotation
        self.renderer = renderer
        self.position = (0,0,0)
        self.variables = {"entity": self, "renderer": self.renderer}
        self.gravity = False
        self.delta_time = 0.1
        self.last_rotation = (0,0,0)
    
    def add_script(self, script: str):
        self.scripts.append(script)

    def toggle_gravity(self):
        self.gravity = not self.gravity
        if self.gravity:
            self.scripts.append("""""")
        else:
            self.scripts.remove("""""")

    def apply_velocity(self):
        self.position = (np.array(self.position) + np.array(self.velocity)*self.delta_time).tolist()
    
    def center_vertices(self):
        pos = self.position
        vertices = self.model[0]
        cx = sum(v[0] for v in vertices) / len(vertices)
        cy = sum(v[1] for v in vertices) / len(vertices)
        cz = sum(v[2] for v in vertices) / len(vertices)
        return [(v[0] - cx + pos[0], v[1] - cy + pos[1], v[2] - cz + pos[2]) for v in vertices]
    
    def rotate(self):
        verts = self.model[0]
        pos = self.position
        verts = (np.array(verts) - np.array(pos)).tolist()

        r = (np.array(self.rotation) - np.array(self.last_rotation)).tolist()

        cos_y = math.cos(math.radians(r[1]))
        sin_y = math.sin(math.radians(r[1]))
        cos_x = math.cos(math.radians(r[0]))
        sin_x = math.sin(math.radians(r[0]))
        cos_z = math.cos(math.radians(r[2]))
        sin_z = math.sin(math.radians(r[2]))

        for i in range(len(verts)):
            x, y, z = verts[i]

            # pitch first (X axis)
            x1 = x
            y1 = y * cos_x - z * sin_x
            z1 = y * sin_x + z * cos_x

            # then yaw (Y axis)
            x2 = x1 * cos_y - z1 * sin_y
            y2 = y1
            z2 = x1 * sin_y + z1 * cos_y

            # roll (Z axis)
            x3 = x2 * cos_z - y2 * sin_z
            y3 = x2 * sin_z + y2 * cos_z
            z3 = z2

            verts[i] = (x3 + pos[0], y3 + pos[1], z3 + pos[2])
        self.model[0] = verts

    def get_face_center(self, vertices):
        n = len(vertices)
        x = sum(v[0] for v in vertices) / n
        y = sum(v[1] for v in vertices) / n
        z = sum(v[2] for v in vertices) / n
        return (x, y, z)
    
    def add_entity_variable(self, name: str, variable):
        if name not in ("entity", "renderer"):
            self.variables[name] = variable
    
    def add_entity_function(self, name: str, function):
        if name not in ("entity", "renderer"):
            self.variables[name] = function

    def use_scripts(self):
        for script in self.scripts:
            exec(script, self.variables)

    def update(self):
        #self.position = self.get_face_center(self.model[0])
        self.delta_time = self.renderer.delta_time
        self.use_scripts()
        self.apply_velocity()
        self.model[0] = self.center_vertices()
        self.rotate()
        self.last_rotation = self.rotation

    def get_entity(self):
        return self.model
    