"""
NPC Class
"""

import pygame


class NPC(pygame.sprite.Sprite):
    """Non-Player Character"""
    
    def __init__(self, npc_id, name, x, y, sprite, dialogue_lines=None):
        """
        Initialize NPC
        
        Args:
            npc_id: Unique ID
            name: NPC name
            x, y: Position
            sprite: Loaded sprite image
            dialogue_lines: List of dialogue strings
        """
        super().__init__()
        
        self.id = npc_id
        self.name = name
        self.x = x
        self.y = y
        
        if sprite is None:
            raise RuntimeError(f"[ERROR] NPC {npc_id} sprite is None!")
        
        self.image = sprite
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        
        self.dialogue_lines = dialogue_lines or [f"Hello! I'm {name}."]
        self.dialogue = self.dialogue_lines
        self.talked_to = False
        
        print(f"[NPC] Created: {name} ({npc_id}) at ({int(x)}, {int(y)})")
    
    def talk_to(self):
        """Start dialogue"""
        self.talked_to = True
        return self.dialogue_lines

    def update(self, dt=0):
        """Update NPC"""
        self.rect.topleft = (int(self.x), int(self.y))
    
    def draw(self, screen, camera_offset):
        """Draw NPC"""
        draw_x = int(self.x - camera_offset[0])
        draw_y = int(self.y - camera_offset[1])
        
        screen.blit(self.image, (draw_x, draw_y))
        
        # Draw name above NPC
        font = pygame.font.Font(None, 20)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (draw_x - 10, draw_y - 25))