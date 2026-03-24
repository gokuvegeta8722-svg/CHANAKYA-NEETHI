"""
Enemy Class
"""

import pygame
import math
from utils.constants import ENEMY_DATA


class Enemy(pygame.sprite.Sprite):
    """Enemy base class"""
    
    def __init__(self, enemy_id, x, y, enemy_type, sprite_dict):
        """
        Initialize enemy
        
        Args:
            enemy_id: Unique ID
            x, y: Position
            enemy_type: Type of enemy (soldier, archer, general)
            sprite_dict: Dict with sprites
        """
        super().__init__()
        
        self.id = enemy_id
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        
        # Load sprite
        sprite_key = list(sprite_dict.keys())[0] if sprite_dict else None
        if sprite_key:
            self.image = sprite_dict[sprite_key]
        else:
            raise RuntimeError(f"[ERROR] No sprite for enemy {enemy_id}")
        
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.sprites = sprite_dict
        
        # Stats from constants
        if enemy_type in ENEMY_DATA:
            data = ENEMY_DATA[enemy_type]
            self.health = data["health"]
            self.max_health = data["health"]
            self.damage = data["damage"]
            self.speed = data["speed"]
            self.coins_reward = data["coins"]
        else:
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.speed = 100
            self.coins_reward = 25
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        
        print(f"[ENEMY] Created: {enemy_id} ({enemy_type}) at ({int(x)}, {int(y)})")
    
    def update(self, dt, player):
        """Update enemy"""
        if not self.is_alive():
            return
        
        # Chase player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 300 and distance > 0:
            # Chase
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            # Stop
            self.velocity_x = 0
            self.velocity_y = 0
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.rect.topleft = (int(self.x), int(self.y))
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        print(f"[ENEMY] {self.id} took {damage} damage. Health: {self.health}/{self.max_health}")
    
    def is_alive(self):
        """Check if alive"""
        return self.health > 0
    
    def draw(self, screen, camera_offset):
        """Draw enemy"""
        if not self.is_alive():
            return
        
        draw_x = int(self.x - camera_offset[0])
        draw_y = int(self.y - camera_offset[1])
        
        screen.blit(self.image, (draw_x, draw_y))
        
        # Health bar
        bar_w = 40
        bar_h = 4
        bar_x = draw_x
        bar_y = draw_y - 10
        
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        health_w = int(bar_w * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, health_w, bar_h))