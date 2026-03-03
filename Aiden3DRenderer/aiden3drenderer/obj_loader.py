import pywavefront
import numpy as np

def get_obj(file_path: str, offset: tuple[int] = (0, 0, 0)):
    scene = pywavefront.Wavefront(file_path, collect_faces=True)

    vertices = scene.vertices
    faces = []

    for mesh in scene.mesh_list:
        for face in mesh.faces:
            # Ensure triangle
            if len(face) == 3:
                faces.append(tuple(face))
            else:
                # Triangulate polygon if needed
                for i in range(1, len(face) - 1):
                    faces.append((face[0], face[i], face[i + 1]))

    vertices = np.array(vertices) + offset
    vertices = vertices.tolist()
    return [vertices, faces]