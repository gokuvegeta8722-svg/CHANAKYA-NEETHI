"""
Player Character - Chandragupta
"""

import pygame
from settings import PLAYER_SPEED, PLAYER_MAX_HEALTH


class Player(pygame.sprite.Sprite):
    """Player character"""
    
    def __init__(self, x, y, sprites_dict):
        """
        Initialize player
        
        Args:
            x, y: Starting position
            sprites_dict: Dict of loaded sprite images
        """
        super().__init__()
        
        self.x = x
        self.y = y
        self.sprites = sprites_dict  # All player sprites
        
        # Start with idle down sprite
        self.image = self.sprites.get("idle", None)
        if self.image is None:
            raise RuntimeError("[ERROR] Player idle sprite not loaded!")
        
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        
        # Stats
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.speed = PLAYER_SPEED
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = "down"
        self.is_moving = False
        
        # Animation
        self.animation_frame = 0
        self.animation_timer = 0
        
        # Combat
        self.is_attacking = False
        self.attack_timer = 0
        
        # Inventory
        self.coins = 0
        self.map_pieces = 0
        self.memory_shards = 0
        
        print(f"[PLAYER] Created at ({int(x)}, {int(y)})")
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_moving = False
        
        # Movement
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.speed
            self.direction = "up"
            self.is_moving = True
            self.image = self.sprites.get("walk_up", self.sprites.get("idle"))
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
            self.direction = "down"
            self.is_moving = True
            self.image = self.sprites.get("walk_down", self.sprites.get("idle"))
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.direction = "left"
            self.is_moving = True
            self.image = self.sprites.get("walk_left", self.sprites.get("idle"))
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.direction = "right"
            self.is_moving = True
            self.image = self.sprites.get("walk_right", self.sprites.get("idle"))
        else:
            # Idle
            idle_key = f"idle"
            self.image = self.sprites.get(idle_key, self.sprites.get("idle"))
    
    def update(self, dt, level_width, level_height):
        """Update player"""
        # Handle input
        self.handle_input()
        
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Boundary check
        self.x = max(0, min(self.x, level_width - self.rect.width))
        self.y = max(0, min(self.y, level_height - self.rect.height))
        
        # Update rect
        self.rect.topleft = (int(self.x), int(self.y))
        
        # Update attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= dt
        else:
            self.is_attacking = False
    
    def attack(self):
        """Perform attack"""
        attack_key = f"attack_{self.direction}"
        if attack_key in self.sprites:
            self.image = self.sprites[attack_key]
            self.is_attacking = True
            self.attack_timer = 0.5
            return True
        return False
    
    def draw(self, screen, camera_offset):
        """Draw player"""
        draw_x = int(self.x - camera_offset[0])
        draw_y = int(self.y - camera_offset[1])
        
        screen.blit(self.image, (draw_x, draw_y))
        
        # Draw health bar
        bar_w = 64
        bar_h = 5
        bar_x = draw_x
        bar_y = draw_y - 10
        
        # Background (red)
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, bar_w, bar_h))
        
        # Health (green)
        health_w = int(bar_w * (self.health / self.max_health))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, health_w, bar_h))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 1)
    
    def take_damage(self, damage):
        """Take damage"""
        self.health = max(0, self.health - damage)
        print(f"[PLAYER] Took {damage} damage. Health: {self.health}/{self.max_health}")
    
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def add_coin(self, amount):
        """Add coin"""
        self.coins += amount
    
    def add_map_piece(self):
        """Add map piece"""
        if self.map_pieces < 4:
            self.map_pieces += 1
            print(f"[PLAYER] Map piece collected! ({self.map_pieces}/4)")
    
    def add_memory_shard(self):
        """Add memory shard"""
        if self.memory_shards < 3:
            self.memory_shards += 1
            print(f"[PLAYER] Memory shard collected! ({self.memory_shards}/3)")