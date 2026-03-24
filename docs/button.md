# UI Button

`Button` is a small Pygame UI helper used by the renderer's pause/settings UI. It provides automatic font sizing and click handling.

Constructor
- `Button(screen, size: tuple, position: tuple, on_press, border_color=(0,0,0), color=(100,100,100), text='', text_color=(0,0,0))`

Methods
- `update(mouse_pos, event)` — call each frame to process mouse clicks; `on_press` is invoked when the button is clicked.
- `draw()` — draw the button to the provided `screen` surface.

Notes
- The Button helper uses an embedded `Jersey25-Regular.ttf` font packaged with the project (works both in-source and in an installed package via `importlib.resources`).
