# Video Renderer

`video_renderer.py` provides a simple offline renderer that projects OBJ models and writes frames to a video file.

Main classes
- `VideoRendererObject` — lightweight container describing an OBJ to render: `shape_path`, `rotations_per_seccond`, `rotation`, `anchor_pos`.
- `VideoRenderer3D(width, height, fps, shapes)` — creates the renderer capable of producing `MJPG` AVI output via OpenCV.

Usage

```python
from aiden3drenderer.video_renderer import VideoRenderer3D, VideoRendererObject

obj = VideoRendererObject('assets/alloy_forge_block.obj')
obj.rotations_per_seccond = [10, 25, 0]

vr = VideoRenderer3D(800, 600, 30, [obj])
vr.render('out.avi', duration_s=5, verbose=True)
```

Notes
- The renderer uses `cv2.VideoWriter` and is intentionally simple — it rasterizes triangles on the CPU and is useful for pre-rendered clips or debugging.
