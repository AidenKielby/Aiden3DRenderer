import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiden3drenderer.renderer import Renderer3D, renderer_type
from aiden3drenderer.dae_loader import get_dae

def main():
    renderer = Renderer3D(width=800, height=800, title="DAE Loader Test")
    
    renderer.camera.position = [0, 0, -5]
    renderer.camera.rotation = [0, 0, 0]
    renderer.render_type = renderer_type.MESH
    renderer.using_obj_filetype_format = True
    
    # Load a COLLADA file
    dae_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'test_cube.dae')
    dae = get_dae(dae_path, texture_index=0, offset=(0, 0, 0), scale=1)
    
    print(f"Loaded {len(dae[0])} vertices, {len(dae[1])} faces")
    
    renderer.vertices_faces_list.append(dae)
    
    while True:
        renderer.loopable_run()


if __name__ == "__main__":
    main()
