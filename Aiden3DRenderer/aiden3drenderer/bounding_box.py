import numpy as np
from .object_type import object_type

def get_bounding_box(vertices, offset=(0,0,0)):
    arr = np.array(vertices, dtype=float)
    mn = arr.min(axis=0)
    mx = arr.max(axis=0)

    # Pad zero-thickness axes so AABB overlap actually works
    for i in range(3):
        if abs(mx[i] - mn[i]) < 1e-2:
            mn[i] -= 0.3
            mx[i] += 0.3

    x0, y0, z0 = mn
    x1, y1, z1 = mx

    box_vertices = [
        [x0, y0, z0],
        [x1, y0, z0],
        [x1, y1, z0], 
        [x0, y1, z0],
        [x0, y0, z1], 
        [x1, y0, z1], 
        [x1, y1, z1], 
        [x0, y1, z1], 
    ]

    box_faces = [
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 4, 7), (0, 7, 3),
        (1, 2, 6), (1, 6, 5),
        (0, 1, 5), (0, 5, 4),
        (3, 7, 6), (3, 6, 2),
    ]

    box_vertices = (np.array(box_vertices) + offset).tolist()

    return [box_vertices, box_faces, [], [], object_type.OBJ]