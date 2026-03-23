import numpy as np
import math

GRAVITY_SCRIPT = """
import numpy as np

# Configuration
GRAVITY = -1.5 
TERMINAL_VELOCITY = -10.0
ELASTICITY = 0.0 

def get_extents(bbox):
    arr = np.array(bbox[0], dtype=float)
    return arr.min(axis=0), arr.max(axis=0)

if entity.gravity:
    # 1. Apply Gravity to velocity
    new_y_vel = entity.velocity[1] + GRAVITY * entity.delta_time
    entity.velocity = (
        entity.velocity[0],
        max(new_y_vel, TERMINAL_VELOCITY), 
        entity.velocity[2]
    )

    # 2. Resolve Collisions (Position Resolution)
    # This prevents 'sinking' by snapping the entity to the surface
    collisions = entity.check_for_collison()
    if collisions:
        for col_idx in collisions:
            other_bbox = entity.renderer.bounding_boxes[col_idx]
            min_self, max_self = get_extents(entity.bounding_box)
            min_other, max_other = get_extents(other_bbox)

            # Calculate overlap depth
            ox = min(max_self[0], max_other[0]) - max(min_self[0], min_other[0])
            oy = min(max_self[1], max_other[1]) - max(min_self[1], min_other[1])
            oz = min(max_self[2], max_other[2]) - max(min_self[2], min_other[2])

            # If the shallowest overlap is Vertical (Y), resolve the floor/ceiling hit
            if oy < ox and oy < oz:
                half_height = (max_self[1] - min_self[1]) / 2.0
                
                if entity.velocity[1] < 0: # Falling Down
                    # Snap to top of object
                    entity.position = [entity.position[0], max_other[1] + half_height, entity.position[2]]
                    entity.velocity = (entity.velocity[0], -entity.velocity[1] * ELASTICITY, entity.velocity[2])
                
                elif entity.velocity[1] > 0: # Moving Up
                    # Snap to bottom of object
                    entity.position = [entity.position[0], min_other[1] - half_height, entity.position[2]]
                    entity.velocity = (entity.velocity[0], 0, entity.velocity[2])
"""

class Entity:
    def __init__(self, model, renderer, start_velocity:list[float]=[0,0,0], starting_rotation:list[float]=[0,0,0], bounding_box = None):
        self.model = model
        self.scripts: list[str] = []
        self.velocity = start_velocity
        self.rotation = starting_rotation
        self.renderer = renderer
        self.position = [0,0,0]
        self.variables = {"entity": self, "renderer": self.renderer}
        self.gravity = False
        self.delta_time = 0.1
        self.last_rotation =[0,0,0]
        self.bounding_box = bounding_box
    
    def add_script(self, script: str):
        self.scripts.append(script)

    def check_for_collison(self, bounding_boxes=None):
        if bounding_boxes is None:
            bounding_boxes = self.renderer.bounding_boxes

        def get_extents(bbox):
            arr = np.array(bbox[0])
            return arr.min(axis=0), arr.max(axis=0)

        collisions = []

        min_b, max_b = get_extents(self.bounding_box)

        for i, other in enumerate(bounding_boxes):
            if other is self.bounding_box:
                continue

            min_a, max_a = get_extents(other)

            if (max_a[0] < min_b[0] or max_b[0] < min_a[0] or
                max_a[1] < min_b[1] or max_b[1] < min_a[1] or
                max_a[2] < min_b[2] or max_b[2] < min_a[2]):
                continue

            collisions.append(i)

        return collisions

    def sync_bounding_box(self):
        if self.bounding_box is None:
            return
        from . import bounding_box as bb
        self.bounding_box = bb.get_bounding_box(self.model[0])

    def toggle_gravity(self):
        self.gravity = not self.gravity
        if self.gravity:
            self.scripts.append(GRAVITY_SCRIPT)
        else:
            self.scripts.remove(GRAVITY_SCRIPT)

    def apply_velocity(self):
        self.position = [
            self.position[0] + self.velocity[0] * self.delta_time,
            self.position[1] + self.velocity[1] * self.delta_time,
            self.position[2] + self.velocity[2] * self.delta_time
        ]
        if len(self.check_for_collison()) > 0:
            self.position = [
                self.position[0] - self.velocity[0] * self.delta_time,
                self.position[1] - self.velocity[1] * self.delta_time,
                self.position[2] - self.velocity[2] * self.delta_time
            ]
    
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
        self.delta_time = self.renderer.delta_time
        self.apply_velocity()
        self.model[0] = self.center_vertices() 
        self.rotate() 
        self.sync_bounding_box() 
        self.use_scripts()   
        self.last_rotation = self.rotation

    def get_entity(self):
        return self.model
    