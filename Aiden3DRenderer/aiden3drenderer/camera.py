"""
Camera controls for 3D renderer
"""
import pygame
import math


class Camera:
    
    def __init__(self, position=None, rotation=None):
        self.position = position if position else [00, 00, 00]
        self.rotation = rotation if rotation else [0, 0, 0]  # pitch, yaw, roll
        
        self.speed = 0.1
        self.base_speed = 0.1
        self.speed_mult = 2
        
        self.mouse_start_pos = None
        self.mouse_start_rotation = None
        self.holding_mouse = False

        self.fov = 100
        
    def handle_mouse_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                self.mouse_start_pos = event.pos
                self.mouse_start_rotation = self.rotation[:]
                self.holding_mouse = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.holding_mouse = False
        elif event.type == pygame.MOUSEWHEEL:
            if self.fov < 170 and event.y<0:
                self.fov -= event.y * 1.1
            if self.fov > 10 and event.y>0:
                self.fov -= event.y * 1.1
    
    def update_mouse_look(self):
        if self.holding_mouse and self.mouse_start_pos:
            current_pos = pygame.mouse.get_pos()
            x_diff = current_pos[0] - self.mouse_start_pos[0]
            y_diff = current_pos[1] - self.mouse_start_pos[1]
            
            self.rotation[0] = self.mouse_start_rotation[0] + y_diff * 0.002  # Pitch
            self.rotation[1] = self.mouse_start_rotation[1] + x_diff * 0.002  # Yaw
    
    def update(self, keys):
        self.update_mouse_look()
        
        forward_x = math.sin(self.rotation[1])
        forward_z = -math.cos(self.rotation[1])
        right_x = math.cos(self.rotation[1])
        right_z = math.sin(self.rotation[1])

        if keys[pygame.K_w]:
            self.position[0] -= forward_x * self.speed
            self.position[2] -= forward_z * self.speed
        if keys[pygame.K_s]:
            self.position[0] += forward_x * self.speed
            self.position[2] += forward_z * self.speed
        if keys[pygame.K_a]:
            self.position[0] += right_x * self.speed
            self.position[2] += right_z * self.speed
        if keys[pygame.K_d]:
            self.position[0] -= right_x * self.speed
            self.position[2] -= right_z * self.speed

        if keys[pygame.K_SPACE]:
            self.position[1] += self.speed
        if keys[pygame.K_LSHIFT]:
            self.position[1] -= self.speed

        if keys[pygame.K_DOWN]:
            self.rotation[0] -= 0.001  # Pitch down
        if keys[pygame.K_UP]:
            self.rotation[0] += 0.001  # Pitch up
        if keys[pygame.K_RIGHT]:
            self.rotation[1] += 0.001  # Yaw right
        if keys[pygame.K_LEFT]:
            self.rotation[1] -= 0.001  # Yaw left
        
        if keys[pygame.K_LCTRL]:
            self.speed = self.base_speed * self.speed_mult
        else:
            self.speed = self.base_speed
