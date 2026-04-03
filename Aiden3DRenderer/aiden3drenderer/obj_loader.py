import numpy as np

from .material import Material
from .object_type import object_type

types = ["normal"]

def get_obj(file_path: str, material: Material, offset=(0,0,0), scale=1, type = "normal"):
    vertices = []
    tex_coords = []
    vertex_faces = []
    texture_faces = []
    scale = max(scale, 0)

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.strip().split()
                v = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(v)

            elif line.startswith("vt "):
                parts = line.strip().split()
                tex_coords.append([float(parts[1]), float(parts[2])])

            elif line.startswith("f "):
                parts = line.strip().split()[1:]

                v_idx = []
                vt_idx = []

                for p in parts:
                    vals = p.split("/")
                    v_idx.append(int(vals[0]) - 1)

                    if len(vals) > 1 and vals[1] != "":
                        vt_idx.append(int(vals[1]) - 1)

                if len(v_idx) == 3:
                    vertex_faces.append(tuple(v_idx))
                    if vt_idx:
                        texture_faces.append(tuple(vt_idx))
                else:
                    # triangulate polygons
                    for i in range(1, len(v_idx)-1):
                        vertex_faces.append((v_idx[0], v_idx[i], v_idx[i+1]))
                        if vt_idx:
                            texture_faces.append((vt_idx[0], vt_idx[i], vt_idx[i+1]))
    arr = np.array(vertices, dtype=float)
    pivot = (arr.min(axis=0) + arr.max(axis=0)) * 0.5

    vertices = ((arr - pivot) * scale + pivot + offset).tolist()

    if type=="normal":
        return [vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, material] # now need to make renderer work with material
    else:
        print(f"not a recognized type from {' '.join(types)}. Treating it as 'normal' type")
        return [vertices, vertex_faces, tex_coords, texture_faces, object_type.OBJ, material] # now need to make renderer work with material

    