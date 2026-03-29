# Camera

Documentation for the `Camera` helper.

Overview
- `Camera` encapsulates position, rotation (pitch, yaw, roll), movement speeds, and simple mouse-look handling.

API
- `Camera(position=None, rotation=None)` — create a camera. Defaults to `[0,0,0]` position and `[0,0,0]` rotation.
- `handle_mouse_events(event)` — process `pygame` mouse events for right-button drag and wheel FOV changes.
- `update_mouse_look()` — internal helper to update camera rotation while dragging.
- `update(keys)` — update camera position and rotation based on keyboard input (`W/A/S/D`, `Space`, `LShift`, arrow keys) and mouse drag.

Attributes
- `position` — [x, y, z] world position.
- `rotation` — [pitch, yaw, roll] in radians (camera uses radians internally for rotation math).
- `speed`, `base_speed`, `speed_mult` — movement speed controls (hold `LCTRL` to get `base_speed * speed_mult`).
- `fov` — field-of-view in degrees; mouse wheel adjusts it.

Usage notes
- Call `handle_mouse_events()` from your event loop and `update(keys)` each frame.
