import re

from . import shapes
from .obj_loader import get_obj
import cv2
import numpy as np
import math

class VideoRendererObject:
    def __init__(self, obj_path: str):
        self.shape_path = obj_path
        self.rotations_per_seccond = [0, 0, 0]
        self.rotation = [0, 0, 0]
        self.anchor_pos = [0, 0, 0]

class VideoRenderer3D:
    def __init__(self, width: int, height: int, fps: int, shapes: list[VideoRendererObject]):
        self.width = width
        self.height = height
        self.fps = fps

        self.half_w = width // 2
        self.half_h = height // 2

        self.shapes = []
        for shapePathI in range(len(shapes)):
            shape_path = shapes[shapePathI].shape_path
            shape_verts, shape_faces = get_obj(shape_path)
            # compute geometric center of the model so rotations occur about its center
            if shape_verts:
                sx = sum(v[0] for v in shape_verts) / len(shape_verts)
                sy = sum(v[1] for v in shape_verts) / len(shape_verts)
                sz = sum(v[2] for v in shape_verts) / len(shape_verts)
                center = (sx, sy, sz)
            else:
                center = (0.0, 0.0, 0.0)

            # rotations_per_seccond is degrees-per-second; compute per-frame increment
            rps = shapes[shapePathI].rotations_per_seccond
            rot_per_f = [rps[0] * self.fps, rps[1] * self.fps, rps[2] * self.fps]

            anchor_pos = shapes[shapePathI].anchor_pos

            self.shapes.append({
                "verts": shape_verts,
                "faces": shape_faces,
                "rot": shapes[shapePathI].rotation,
                "rot_per_f": rot_per_f,
                "center": center,
                "anchor_pos": anchor_pos,
            })
    
    def add_shape(self, shape_path):
        shape_verts, shape_faces = get_obj(shape_path)
        self.shapes.append({"verts": shape_verts, "faces": shape_faces})

    def project_3d_to_2d_flat(self, inList, object_rotation, anchor_pos, fov, camera_pos, camera_facing, center=None):
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

            # rotate around provided center (model-space centroid) so the object spins about its own axis
            if center is None:
                object_center = (0.0, 0.0, 0.0)
            else:
                object_center = center

            # shift to center, rotate, then shift back
            x -= object_center[0]
            y -= object_center[1]
            z -= object_center[2]

            object_rotation1 = [0, 0, 0]
            object_rotation1[0] = math.radians(object_rotation[0])
            object_rotation1[1] = math.radians(object_rotation[1])
            object_rotation1[2] = math.radians(object_rotation[2])

            x11 = x * math.cos(object_rotation1[1]) + z * math.sin(object_rotation1[1])
            y11 = y
            z11 = -x * math.sin(object_rotation1[1]) + z * math.cos(object_rotation1[1])

            x21 = x11
            y21 = y11 * math.cos(object_rotation1[0]) - z11 * math.sin(object_rotation1[0])
            z21 = y11 * math.sin(object_rotation1[0]) + z11 * math.cos(object_rotation1[0])

            x31 = x21 * math.cos(object_rotation1[2]) - y21 * math.sin(object_rotation1[2])
            y31 = x21 * math.sin(object_rotation1[2]) + y21 * math.cos(object_rotation1[2])
            z31 = z21

            # shift back from object center into model/world space before camera transform
            x31 += object_center[0]
            y31 += object_center[1]
            z31 += object_center[2]

            x31 += anchor_pos[0]
            y31 += anchor_pos[1]
            z31 += anchor_pos[2]

            x = x31 - camera_pos[0]
            y = y31 - camera_pos[1]
            z = z31 - camera_pos[2]

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
            
        
            projected.append((px, py, z3))

        return projected
    
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

        if d1 >= 0 and d2 >= 0 and d3 >= 0:
            return True
        
        return False

    
    # ik, ik... such a great idea to have a verbose param
    # no glaze
    def render(self, file_path: str, duration_s: int, verbose: bool = False):
        frames = duration_s * self.fps
        if verbose:
            print(f"Starting render to path '{file_path}'")
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(file_path, fourcc, self.fps, (self.width, self.height))

        """for i in range(len(self.shapes)):
            shape = self.shapes[i]
            verts = shape["verts"]
            flattened_verts = self.project_3d_to_2d_flat(verts, math.radians(90), (0, 1, -2), (0, 0, 0))
            flattened_shapes.append({"verts": flattened_verts, "faces": shape["faces"], "rot": shape["rot"], "rot_per_f": shape["rot_per_f"]})"""

        for frameI in range(frames):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for shapeI in range(len(self.shapes)):
                shape = self.shapes[shapeI]
                verts = shape["verts"]
                center = shape["center"]
                faces = shape["faces"]
                rotation = shape["rot"]
                rpf = shape["rot_per_f"]
                anchor_pos = shape["anchor_pos"]

                rotation[0] += rpf[0]
                rotation[1] += rpf[1]
                rotation[2] += rpf[2]
                shape["rot"] = rotation
                flattened_verts = self.project_3d_to_2d_flat(verts, rotation, anchor_pos, math.radians(90), (0, 1, -2), (0, 0, 0), center)

                for face in faces:
                    gone = False
                    col = np.random.randint(0, 255, (3), dtype=int)
                    p0 = flattened_verts[face[0]]
                    p1 = flattened_verts[face[1]]
                    p2 = flattened_verts[face[2]]
                    if p0 == None or p1 == None or p2 == None:
                        gone = True
                    for yI in range(self.height):
                        for xI in range(self.width):
                            if not gone:
                                if self.is_point_inside_triangle(p0, p1, p2, (xI, yI)):
                                    frame[yI, xI] = col
            out.write(frame)

            if verbose:
                print(f"Frame {frameI} complete")
        
        out.release()
        if verbose:
            print(f"Render complete at: '{file_path}'")
        