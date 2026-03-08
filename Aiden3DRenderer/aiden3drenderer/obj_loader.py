import pywavefront
import numpy as np

def get_obj(file_path: str, offset=(0,0,0)):
    vertices = []
    tex_coords = []
    vertex_faces = []
    texture_faces = []

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.strip().split()
                v = [float(parts[1]), float(parts[2]), float(parts[3])]
                v = (np.array(v) + offset).tolist()
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

    return [vertices, vertex_faces, tex_coords, texture_faces]