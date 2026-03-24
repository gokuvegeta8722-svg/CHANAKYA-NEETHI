"""
Base Level Class
"""

import pygame
from settings import *
from systems import *
from entities import *


class BaseLevel:
    """Base class for all levels"""
    
    def __init__(self, level_id, assets_loader):
        """
        Initialize level
        
        Args:
            level_id: Level number (1-5)
            assets_loader: AssetLoader instance
        """
        self.level_id = level_id
        self.assets = assets_loader
        
        # Systems
        self.dialogue_manager = DialogueManager()
        self.combat_system = CombatSystem()
        self.collision_system = CollisionSystem()
        self.inventory = InventorySystem()
        self.camera = None
        
        # Entities
        self.player = None
        self.npcs = []
        self.enemies = []
        self.items = []
        
        # Level data
        self.background = None
        self.level_width = SCREEN_WIDTH
        self.level_height = SCREEN_HEIGHT
        
        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
    
    def setup_level(self):
        """Setup level - override in subclasses"""
        raise NotImplementedError("Subclass must implement setup_level()")
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self._try_interact()
    
    def handle_space(self):
        """Handle space key"""
        if self.dialogue_manager.active:
            self.dialogue_manager.next_line()
        else:
            if self.combat_system.attack():
                self._check_combat()
    
    def _try_interact(self):
        """Try to interact with NPC"""
        for npc in self.npcs:
            dx = npc.x - self.player.x
            dy = npc.y - self.player.y
            dist = (dx*dx + dy*dy) ** 0.5
            
            if dist < 100:
                lines = npc.talk_to()
                self.dialogue_manager.start(lines, npc.name)
                break
    
    def _check_combat(self):
        """Check if attack hits enemies"""
        for enemy in self.enemies:
            if enemy.is_alive():
                if self.collision_system.check_distance(
                    (self.player.x, self.player.y),
                    (enemy.x, enemy.y),
                    self.combat_system.player_attack_range
                ):
                    enemy.take_damage(self.combat_system.player_attack_damage)
    
    def _check_item_collection(self):
        """Check if player collects items"""
        for item in self.items[:]:
            if item.collected:
                if item.type == "coin":
                    self.player.add_coin(item.value)
                    self.inventory.add_coins(item.value)
                elif item.type == "map_piece":
                    self.player.add_map_piece()
                    self.inventory.add_map_piece()
                elif item.type == "memory_shard":
                    self.player.add_memory_shard()
                    self.inventory.add_memory_shard()
                
                self.items.remove(item)
    
    def update(self, dt):
        """Update level"""
        if not self.player:
            return
        
        # Update player
        self.player.update(dt, self.level_width, self.level_height)
        
        # Update NPCs
        for npc in self.npcs:
            pass  # NPCs don't move
        
        # Update enemies
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.update(dt, self.player)
        
        # Update items
        for item in self.items:
            item.update(self.player.rect)
        
        self._check_item_collection()
        
        # Update camera
        if self.camera:
            self.camera.update(self.player, dt)
        
        # Update combat
        self.combat_system.update(dt)
    
    def draw(self, screen):
        """Draw level"""
        camera_offset = self.camera.get_offset() if self.camera else (0, 0)
        
        # Draw background
        if self.background:
            screen.blit(self.background, (-int(camera_offset[0]), -int(camera_offset[1])))
        else:
            screen.fill(DARK_BROWN)
        
        # Draw items
        for item in self.items:
            item.draw(screen, camera_offset)
        
        # Draw NPCs
        for npc in self.npcs:
            npc.draw(screen, camera_offset)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen, camera_offset)
        
        # Draw player
        if self.player:
            self.player.draw(screen, camera_offset)
        
        # Draw dialogue
        if self.dialogue_manager.active:
            self._draw_dialogue(screen)
        
        # Draw HUD
        self._draw_hud(screen)
    
    def _draw_dialogue(self, screen):
        """Draw dialogue box"""
        line = self.dialogue_manager.get_current_line()
        if not line:
            return
        
        # Dialogue box
        box_h = 100
        box_y = SCREEN_HEIGHT - box_h - 20
        pygame.draw.rect(screen, (50, 50, 50), (20, box_y, SCREEN_WIDTH - 40, box_h))
        pygame.draw.rect(screen, (200, 200, 200), (20, box_y, SCREEN_WIDTH - 40, box_h), 2)
        
        # Speaker name
        speaker_text = self.font_medium.render(self.dialogue_manager.speaker, True, GOLD)
        screen.blit(speaker_text, (40, box_y + 10))
        
        # Dialogue text
        text = self.font_medium.render(line, True, WHITE)
        screen.blit(text, (40, box_y + 35))
        
        # Continue hint
        hint = self.font_small.render("[SPACE or E to continue]", True, GRAY)
        screen.blit(hint, (SCREEN_WIDTH - 300, box_y + 70))
    
    def _draw_hud(self, screen):
        """Draw heads-up display"""
        texts = [
            (f"Level {self.level_id}: {LEVEL_NAMES.get(self.level_id, 'Unknown')}", 10, 10),
            (f"Health: {int(self.player.health)}/{int(self.player.max_health)}", 10, 40),
            (f"Coins: {self.inventory.coins}", SCREEN_WIDTH - 200, 10),
            (f"Map Pieces: {self.inventory.map_pieces}/4", SCREEN_WIDTH - 200, 40),
            (f"Memory Shards: {self.inventory.memory_shards}/3", SCREEN_WIDTH - 200, 70),
            ("Controls: WASD/Arrows=Move | E=Talk | SPACE=Attack | ESC=Menu", 10, SCREEN_HEIGHT - 30),
        ]
        
        for text_str, x, y in texts:
            text_surface = self.font_medium.render(text_str, True, WHITE)
            screen.blit(text_surface, (x, y))