"""
Door Entity - Level Transition Point
"""

import pygame


class Door:
    """
    Door entity for transitioning between levels
    
    The player can walk up to the door and press E to go to next level
    """
    
    def __init__(self, x, y, width, height, next_level, sprite=None):
        """
        Initialize door
        
        Args:
            x: X position
            y: Y position
            width: Door width
            height: Door height
            next_level: Level number to transition to (e.g., 2)
            sprite: Door image (pygame.Surface)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.next_level = next_level
        self.sprite = sprite
        
        # Collision rect
        self.rect = pygame.Rect(x, y, width, height)
        
        # Interaction distance
        self.interaction_range = 100
        
        # State
        self.is_interactable = False
        self.is_activated = False
    
    def update(self, player_pos):
        """
        Update door state based on player position
        
        Args:
            player_pos: Tuple of (x, y) player position
        """
        px, py = player_pos
        dx = px - self.x
        dy = py - self.y
        distance = (dx*dx + dy*dy) ** 0.5
        
        # Player is in interaction range
        self.is_interactable = distance < self.interaction_range
    
    def check_activation(self):
        """
        Check if door should activate
        
        Returns:
            True if player is in range and ready to interact
        """
        return self.is_interactable
    
    def activate(self):
        """Activate door transition"""
        self.is_activated = True
        return self.next_level
    
    def draw(self, screen, camera_offset=(0, 0)):
        """
        Draw door
        
        Args:
            screen: pygame display surface
            camera_offset: Camera offset (x, y)
        """
        draw_x = self.x - camera_offset[0]
        draw_y = self.y - camera_offset[1]
        
        
        if self.sprite:
            # Draw sprite if available
            screen.blit(self.sprite, (draw_x, draw_y))
        else:
            # Draw placeholder door
            pygame.draw.rect(screen, (139, 69, 19), (draw_x, draw_y, self.width, self.height))
            pygame.draw.rect(screen, (205, 133, 63), (draw_x, draw_y, self.width, self.height), 3)
            
            # Draw door handle (circle)
            pygame.draw.circle(screen, (255, 215, 0), (int(draw_x + self.width - 10), int(draw_y + self.height // 2)), 4)
        
        # Draw interaction hint if player is near
        if self.is_interactable:
            pygame.draw.rect(screen, (255, 215, 0), (draw_x, draw_y - 30, self.width, 25), 2)
            font = pygame.font.Font(None, 20)
            hint = font.render("Press E", True, (255, 215, 0))
            screen.blit(hint, (draw_x + 5, draw_y - 25))
