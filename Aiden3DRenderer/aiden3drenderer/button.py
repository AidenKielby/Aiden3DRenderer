import pygame
from importlib import resources

def _get_font_path():
    # Works in source tree and installed package
    return str(resources.files("aiden3drenderer").joinpath("fonts/Jersey25-Regular.ttf"))

class Button:
    def __init__(self, screen: pygame.display, size: tuple, position: tuple, on_press, border_color = (0,0,0), color = (100,100,100), text = "", text_color = (0, 0, 0)):
        self.screen = screen
        self.size = size
        self.pos = position
        self.function = on_press
        self.border_col = border_color
        self.col = color
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        pygame.font.init()
        self.font = self.get_fitting_font(text, size, font_path=_get_font_path())
        self.text = text
        self.text_color = text_color
        self.toggled = False

    def get_fitting_font(self, text, rect_size, font_path=None):
        target_w, target_h = rect_size
        
        low = 1
        high = 300  # upper bound guess
        
        best_font = None
        
        while low <= high:
            mid = (low + high) // 2
            font = pygame.font.Font(font_path, mid)
            
            w, h = font.size(text)  # faster than render
            
            if w <= target_w and h <= target_h:
                best_font = font
                low = mid + 1
            else:
                high = mid - 1
                
        return best_font

    def update(self, mouse_pos: tuple, event):
        if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + self.size[1]:
            if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + self.size[0]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.toggled:
                    self.function()
        
    
    def draw(self):
        pygame.draw.rect(self.screen, self.col, (self.pos[0],self.pos[1],self.size[0],self.size[1]))
        pygame.draw.rect(self.screen, self.border_col, (self.pos[0],self.pos[1],self.size[0],self.size[1]), 1)
        text = self.font.render(self.text, True, self.text_color)
        # Ensure rect is up-to-date
        self.rect = pygame.Rect(int(self.pos[0]), int(self.pos[1]), int(self.size[0]), int(self.size[1]))
        self.screen.blit(text, text.get_rect(center=self.rect.center))

    def set_rect(self, size: tuple, position: tuple):
        # Update size and position and recompute layout-dependent resources
        self.size = (int(size[0]), int(size[1]))
        self.pos = (int(position[0]), int(position[1]))
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        # Recompute font to fit the new rectangle
        pygame.font.init()
        self.font = self.get_fitting_font(self.text, self.size, font_path=_get_font_path())

    def set_text(self, text: str):
        # Update text and refit font for current size
        self.text = text
        pygame.font.init()
        self.font = self.get_fitting_font(self.text, self.size, font_path=_get_font_path())
