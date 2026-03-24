"""
Camera System - Follow player
"""

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """Camera that follows player"""
    
    def __init__(self, level_width, level_height):
        """Initialize camera"""
        self.x = 0
        self.y = 0
        self.level_width = level_width
        self.level_height = level_height
    
    def update(self, player, dt):
        """Update camera"""
        # Target center on player
        target_x = player.x - SCREEN_WIDTH // 2 + player.rect.width // 2
        target_y = player.y - SCREEN_HEIGHT // 2 + player.rect.height // 2
        
        # Smooth follow
        self.x += (target_x - self.x) * dt * 3
        self.y += (target_y - self.y) * dt * 3
        
        # Clamp to level bounds
        self.x = max(0, min(self.x, self.level_width - SCREEN_WIDTH))
        self.y = max(0, min(self.y, self.level_height - SCREEN_HEIGHT))
    
    def get_offset(self):
        """Get camera offset"""
        return (self.x, self.y)