# Button (UI helper)

Small pygame-backed button widget used by the `Renderer3D` pause/settings UI.

Constructor
-----------

`Button(screen: pygame.Surface, size: tuple[int,int], position: tuple[int,int], on_press: callable, border_color=(0,0,0), color=(100,100,100), text='', text_color=(0,0,0))`

Behavior
--------

- The constructor computes a fitting font using `get_fitting_font` with the packaged font `fonts/Jersey25-Regular.ttf`. The helper `_get_font_path()` uses `importlib.resources` so the font path works both in-source and from an installed package.
- The button only triggers `on_press()` when its `toggled` attribute is `True` and the left mouse button is pressed inside the rect. `Renderer3D` flips `toggled` to mark active UI state.

Public methods
--------------

- `get_fitting_font(text, rect_size, font_path=None)` — binary-search font size to best fit text inside a rect.
- `update(mouse_pos, event)` — check mouse position and call `on_press` when appropriate.
- `draw()` — draw the button rect, border, and centered text onto `self.screen`.
- `set_rect(size, position)` — update size/position and recompute a fitting font.
- `set_text(text)` — update text and recompute a fitting font.

Caveats
-------

- `pygame.font.init()` is called during font recalculation; ensure `pygame` is initialized before creating buttons.

Example
-------

```python
from aiden3drenderer import Button
import pygame

pygame.init(); screen = pygame.display.set_mode((300,200))
btn = Button(screen, (100, 40), (10,10), lambda: print('pressed'), text='Hi')
btn.draw()
```
