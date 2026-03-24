"""Base Level Class"""

import math
import pygame

from settings import *
from systems.dialogue import DialogueManager
from systems.inventory import Inventory
from systems.collision import CollisionSystem
from systems.combat import CombatSystem
from entities import Coin, MapPiece, MemoryShard


class BaseLevel:
    """Base class for all levels"""

    def __init__(self, level_id, assets):
        """Initialize base level"""
        self.level_id = level_id
        self.assets = assets

        self.background = None
        self.level_width = SCREEN_WIDTH
        self.level_height = SCREEN_HEIGHT

        self.player = None
        self.camera = None

        self.npcs = []
        self.enemies = []
        self.items = []

        self.dialogue = DialogueManager()
        self.inventory = Inventory()
        self.collision_system = CollisionSystem()
        self.combat_system = CombatSystem()

        self.font = pygame.font.Font(None, 24)
        self.dialog_font = pygame.font.Font(None, 20)

        self.game_over = False
        self.level_complete = False

    def setup(self):
        """Setup level - override in subclass"""
        pass

    def handle_event(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            if self.dialogue.active:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_e):
                    self.dialogue.next()
                return

            if event.key == pygame.K_e:
                self._handle_interact()

    def handle_space(self):
        """Handle space key"""
        if not self.player:
            return

        if self.dialogue.active:
            self.dialogue.next()
        else:
            self.player.attack()

    def _handle_interact(self):
        """Handle interaction with NPCs"""
        if not self.player:
            return

        for npc in self.npcs:
            dist = math.sqrt((self.player.x - npc.x) ** 2 + (self.player.y - npc.y) ** 2)
            if dist < 100:
                npc_lines = getattr(npc, "dialogue", None)

                if npc_lines is None:
                    npc_lines = getattr(npc, "dialogue_lines", None)

                if npc_lines is None and hasattr(npc, "talk_to"):
                    npc_lines = npc.talk_to()

                if npc_lines is None:
                    npc_lines = ["..."]

                if isinstance(npc_lines, str):
                    npc_lines = [npc_lines]

                self.dialogue.start(npc_lines, getattr(npc, "name", "NPC"))
                break

    def update(self, dt):
        """Update level"""
        if self.game_over or self.level_complete:
            return

        # Update player
        if self.player:
            self.player.update(dt, self.level_width, self.level_height)

            if self.camera:
                self.camera.update(self.player, dt)

        # Update NPCs
        for npc in self.npcs:
            if hasattr(npc, "update"):
                try:
                    npc.update(dt)
                except TypeError:
                    try:
                        npc.update()
                    except TypeError:
                        pass

        # Update enemies
        for enemy in self.enemies:
            if hasattr(enemy, "update") and self.player:
                try:
                    enemy.update(dt, self.player)
                except TypeError:
                    try:
                        enemy.update(dt)
                    except TypeError:
                        try:
                            enemy.update()
                        except TypeError:
                            pass

        # Update items
        for item in self.items[:]:
            if hasattr(item, "update"):
                try:
                    if self.player:
                        item.update(dt, self.player.rect)
                    else:
                        item.update(dt, None)
                except TypeError:
                    try:
                        item.update(self.player.rect if self.player else None)
                    except TypeError:
                        try:
                            item.update(dt)
                        except TypeError:
                            try:
                                item.update()
                            except TypeError:
                                pass

        # Handle collisions and combat
        self._handle_collisions()
        self._handle_combat()

        # Update dialogue
        if hasattr(self.dialogue, "update"):
            self.dialogue.update(dt)

    def _handle_collisions(self):
        """Handle collisions"""
        if not self.player:
            return

        for item in self.items[:]:
            if self.collision_system.check_collision(self.player, item):
                self._collect_item(item)

        for enemy in self.enemies:
            if self.collision_system.check_collision(self.player, enemy):
                if hasattr(self.player, "take_damage"):
                    self.player.take_damage(5)

    def _collect_item(self, item):
        """Collect item"""
        if isinstance(item, Coin):
            self.inventory.add_coin()
        elif isinstance(item, MapPiece):
            self.inventory.add_map_piece()
        elif isinstance(item, MemoryShard):
            self.inventory.add_memory_shard()

        if item in self.items:
            self.items.remove(item)

    def _handle_combat(self):
        """Handle combat"""
        if not self.player:
            return

        if not getattr(self.player, "attacking", False):
            return

        attack_rect = self.player.get_attack_rect()

        for enemy in self.enemies[:]:
            if hasattr(enemy, "rect") and attack_rect.colliderect(enemy.rect):
                damage = self.combat_system.calculate_damage(self.player, enemy)

                if hasattr(enemy, "take_damage"):
                    enemy.take_damage(damage)

                if getattr(enemy, "health", 1) <= 0:
                    self.enemies.remove(enemy)
    def draw(self, screen):
        """Draw level"""
        cam = self.camera.get_offset() if self.camera else (0, 0)

        if self.background:
            screen.blit(self.background, (-int(cam[0]), -int(cam[1])))
        else:
            screen.fill(DARK_BROWN)

        for item in self.items:
            item.draw(screen, cam)

        for npc in self.npcs:
            npc.draw(screen, cam)

        for enemy in self.enemies:
            enemy.draw(screen, cam)

        if self.player:
            self.player.draw(screen, cam)

        self._draw_waypoint_marker(screen, cam)

        if self.dialogue.active:
            self._draw_dialogue(screen)

        if self.player:
            self._draw_hud(screen)

    def _draw_waypoint_marker(self, screen, cam):
        """Draw objective marker"""
        objectives = {
            1: (1000, 200),
            2: (800, 250),
            3: (600, 300),
            4: (400, 300),
            5: (600, 250),
        }

        if self.level_id not in objectives:
            return

        target_x, target_y = objectives[self.level_id]
        screen_x = int(target_x - cam[0])
        screen_y = int(target_y - cam[1])

        if 0 < screen_x < SCREEN_WIDTH and 0 < screen_y < SCREEN_HEIGHT:
            pygame.draw.circle(screen, GOLD, (screen_x, screen_y), 20, 3)
            pygame.draw.circle(screen, (255, 255, 0), (screen_x, screen_y), 15, 2)

            pulse = math.sin(pygame.time.get_ticks() / 500) * 5
            pygame.draw.circle(screen, RED, (screen_x, screen_y), int(25 + pulse), 1)

    def _draw_dialogue(self, screen):
        """Draw dialogue box"""
        box_width = 600
        box_height = 150
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = SCREEN_HEIGHT - box_height - 20

        pygame.draw.rect(screen, DARK_BROWN, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, GOLD, (box_x, box_y, box_width, box_height), 3)

        name_text = self.font.render(f"{self.dialogue.speaker}:", True, GOLD)
        screen.blit(name_text, (box_x + 10, box_y + 10))

        current_line = None
        if hasattr(self.dialogue, "get_current_line"):
            current_line = self.dialogue.get_current_line()
        elif hasattr(self.dialogue, "get_line"):
            current_line = self.dialogue.get_line()

        if current_line:
            lines = str(current_line).split("\n")
            for i, line in enumerate(lines):
                text = self.dialog_font.render(line, True, WHITE)
                screen.blit(text, (box_x + 10, box_y + 45 + i * 25))

    def _draw_hud(self, screen):
        """Draw HUD"""
        health_percent = 0
        if self.player.max_health > 0:
            health_percent = self.player.health / self.player.max_health

        health_width = 200
        pygame.draw.rect(screen, RED, (10, 10, health_width, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, int(health_width * health_percent), 20))
        pygame.draw.rect(screen, WHITE, (10, 10, health_width, 20), 2)

        health_text = self.font.render(
            f"HP: {int(self.player.health)}/{int(self.player.max_health)}",
            True,
            WHITE
        )
        screen.blit(health_text, (15, 35))

        level_text = self.font.render(
            f"Level {self.level_id}: {LEVEL_NAMES.get(self.level_id, 'Unknown')}",
            True,
            GOLD
        )
        screen.blit(level_text, (10, 65))

        coins_text = self.font.render(f"Coins: {self.inventory.coins}", True, GOLD)
        screen.blit(coins_text, (SCREEN_WIDTH - 250, 10))

        map_text = self.font.render(f"Map Pieces: {self.inventory.map_pieces}/4", True, GOLD)
        screen.blit(map_text, (SCREEN_WIDTH - 250, 40))

        shards_text = self.font.render(f"Memory Shards: {self.inventory.memory_shards}/3", True, GOLD)
        screen.blit(shards_text, (SCREEN_WIDTH - 250, 70))

        self._draw_compass(screen)

    def _draw_compass(self, screen):
        """Draw compass"""
        compass_x = SCREEN_WIDTH // 2 - 80
        compass_y = 20
        compass_width = 160
        compass_height = 50

        pygame.draw.rect(screen, (50, 50, 50), (compass_x, compass_y, compass_width, compass_height))
        pygame.draw.rect(screen, GOLD, (compass_x, compass_y, compass_width, compass_height), 3)

        comp_font = pygame.font.Font(None, 18)
        compass_text = comp_font.render("OBJECTIVE:", True, GOLD)
        screen.blit(compass_text, (compass_x + 10, compass_y + 5))

        directions = {
            1: ("→ Find Spy (East)", "→"),
            2: ("↓ Collect Items", "↓"),
            3: ("↓ Defeat Enemies", "↓"),
            4: ("↑ Archers North", "↑"),
            5: ("● Defeat Boss", "●"),
        }

        direction_text, arrow = directions.get(self.level_id, ("→ Unknown", "?"))

        arrow_text = comp_font.render(arrow, True, RED)
        screen.blit(arrow_text, (compass_x + 140, compass_y + 10))

        dir_label = comp_font.render(direction_text, True, WHITE)
        screen.blit(dir_label, (compass_x + 10, compass_y + 25))