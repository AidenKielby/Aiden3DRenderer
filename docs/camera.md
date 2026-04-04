# Camera

Purpose & integration
---------------------

`Camera` is a small utility class that encapsulates first‑person style controls used by `Renderer3D`. It is intentionally minimal: it tracks position, rotation (pitch, yaw, roll), and mouse/key-driven updates.

Constructor
-----------

`Camera(position: Optional[list[float]] = None, rotation: Optional[list[float]] = None)`

- `position` defaults to `[0, 0, 0]` when omitted.
- `rotation` defaults to `[0, 0, 0]` (pitch, yaw, roll) when omitted.

Fields (not exhaustive)
- `position` (list[float]) — camera world position.
- `rotation` (list[float]) — Euler rotation: pitch (X), yaw (Y), roll (Z).
- `speed`, `base_speed` (float) — per-frame movement speed; `base_speed` is the regular speed and `speed_mult` is used for sprinting.
- `fov` (float) — field of view in degrees. Default: `100`.

Public methods
--------------

`handle_mouse_events(event: pygame.event.Event) -> None`
	- Monitors mouse events used by this camera.
	- Right mouse button down (`button == 3`) begins mouse-look; right mouse up ends it.
	- Mouse wheel (`MOUSEWHEEL`) adjusts `fov` in +/- increments (clamped between ~10 and ~170 degrees).

`update_mouse_look() -> None`
	- If mouse-look is active, computes delta from the initial mouse-down position and updates `rotation[0]` (pitch) and `rotation[1]` (yaw).

`update(keys: Sequence[bool]) -> None`
	- Apply keyboard-driven motion based on the `keys` mapping (as returned by `pygame.key.get_pressed()`).
	- Controls implemented:
		- `W/S/A/D`: forward/back/strafe
		- `Space` / `LShift`: move up/down
		- Arrow keys: small pitch/yaw adjustments
		- `LCTRL`: temporarily multiplies speed by `speed_mult`

Side effects and caveats
------------------------
- This module depends on `pygame` for events and constants; calling `handle_mouse_events` or `update` without a `pygame` event loop or an initialized display may be inappropriate.
- Angles in `rotation` are stored in radians internally in renderer computations (the renderer converts where necessary).

Example
-------

```python
from aiden3drenderer import Camera

cam = Camera()
# within a pygame loop:
# for event in pygame.event.get(): cam.handle_mouse_events(event)
# keys = pygame.key.get_pressed(); cam.update(keys)
```

See also: [Renderer](renderer.md) — the renderer owns a `Camera` instance and wires it to input events.
