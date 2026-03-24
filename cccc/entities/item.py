"""
Collectible Items
"""

import pygame


class Item(pygame.sprite.Sprite):
    """Base item class"""
    
    def __init__(self, item_type, x, y, sprite):
        """
        Initialize item
        
        Args:
            item_type: Type (coin, map_piece, memory_shard)
            x, y: Position
            sprite: Sprite image
        """
        super().__init__()
        
        self.type = item_type
        self.x = x
        self.y = y
        
        if sprite is None:
            raise RuntimeError(f"[ERROR] Item {item_type} sprite is None!")
        
        self.image = sprite
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.collected = False
    
    def update(self, player_rect):
        """Check if collected"""
        if self.rect.colliderect(player_rect):
            self.collected = True
    
    def draw(self, screen, camera_offset):
        """Draw item"""
        if self.collected:
            return
        
        draw_x = int(self.x - camera_offset[0])
        draw_y = int(self.y - camera_offset[1])
        screen.blit(self.image, (draw_x, draw_y))


class Coin(Item):
    """Coin collectible"""
    
    def __init__(self, x, y, sprite):
        super().__init__("coin", x, y, sprite)
        self.value = 10


class MapPiece(Item):
    """Map piece collectible"""
    
    def __init__(self, x, y, sprite):
        super().__init__("map_piece", x, y, sprite)


class MemoryShard(Item):
    """Memory shard collectible"""
    
    def __init__(self, x, y, sprite):
        super().__init__("memory_shard", x, y, sprite)