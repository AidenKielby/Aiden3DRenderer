# Video Renderer (offline rendering)

Small helper classes to render simple rotating OBJ models into an AVI using `cv2.VideoWriter`. This module is intended for offline, non-interactive exports and is separate from the main `Renderer3D` pipeline.

Classes
-------

`VideoRendererObject(obj_path: str)`
	- Lightweight container for a single OBJ model path and per-object animation parameters.
	- Public fields:
		- `shape_path` (str): path given at construction.
		- `rotations_per_seccond` (list[float]): degrees-per-second per axis (note misspelling preserved in the code).
		- `rotation` (list[float]): current rotation in degrees.
		- `anchor_pos` (list[float]): model translation in world space.

`VideoRenderer3D(width: int, height: int, fps: int, shapes: list[VideoRendererObject])`
	- Builds an offline renderer that loads OBJ meshes (via `obj_loader.get_obj`) and projects them into frames written with OpenCV.

Constructor behavior and caveats
--------------------------------

- The constructor calls `get_obj(shape_path)` for each provided `VideoRendererObject`.
- Current source mismatch: `obj_loader.get_obj` now requires a `Material` argument and returns a 6-item model list. `video_renderer.py` still calls `get_obj(shape_path)` and unpacks into two variables (`shape_verts, shape_faces`).
- In current package source this typically raises `TypeError` at initialization before rendering begins.

Methods of interest
-------------------

- `add_shape(shape_path: str)` — load another OBJ and append to the internal list.
- `project_3d_to_2d_flat(inList, object_rotation, anchor_pos, fov, camera_pos, camera_facing, center=None)` — projects vertex lists similar to the renderer's flat projection; returns a list of `(x,y,z)` or `None` for culled vertices.
- `render(file_path: str, duration_s: int, verbose: bool = False)` — render `duration_s * fps` frames into a video file using OpenCV. The method rasterizes triangles on the CPU by testing each pixel against triangle coverage (slow but deterministic). Writes MJPG AVI files.

Performance and correctness notes
--------------------------------

- The per-pixel triangle fill is O(width*height*triangles) and will be slow for large frames or many triangles. This module is suited to small example renders as included in `examples/`.
- `add_shape(shape_path)` has the same loader mismatch as the constructor and is affected by the same issue.

Legacy example (may fail in current source)
-------------------------------------------

```python
from aiden3drenderer import VideoRenderer3D, VideoRendererObject

vO1 = VideoRendererObject('./assets/cobe.obj')
vO1.rotations_per_seccond = [1,1,0]
vO1.anchor_pos = [0,0,2]

vr = VideoRenderer3D(300, 250, 5, [vO1])
vr.render('test.avi', 5, verbose=True)
```

See also: [OBJ Loader](obj_loader.md) and [Audit Report](audit_report.md) for the exact drift details.
