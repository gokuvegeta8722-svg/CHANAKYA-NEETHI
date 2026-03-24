"""Level 2"""

import math
import pygame

from scenes.base_level import BaseLevel
from entities import Player, NPC, Enemy, Coin
from systems import Camera
from utils.constants import NPC_DATA
from entities.door import Door


class Level2(BaseLevel):
    def __init__(self, assets):
        super().__init__(2, assets)

        self.traded_with_merchant = False
        self.door = None   # door starts locked

        self.setup()

    def setup(self):
        print("\n[LEVEL 2] Bharukaccha - Dana (Trade)\n")

        self.background = self.assets.load_image("level2_bg")
        self.level_width = self.background.get_width()
        self.level_height = self.background.get_height()

        # Player
        player_sprites = {
            "idle": self.assets.load_image("player_idle", scale=(64, 64)),
            "walk_up": self.assets.load_image("player_walk_up", scale=(64, 64)),
            "walk_down": self.assets.load_image("player_walk_down", scale=(64, 64)),
            "walk_left": self.assets.load_image("player_walk_left", scale=(64, 64)),
            "walk_right": self.assets.load_image("player_walk_right", scale=(64, 64)),
            "attack_up": self.assets.load_image("player_attack_up", scale=(64, 64)),
            "attack_down": self.assets.load_image("player_attack_down", scale=(64, 64)),
            "attack_left": self.assets.load_image("player_attack_left", scale=(64, 64)),
            "attack_right": self.assets.load_image("player_attack_right", scale=(64, 64)),
        }

        self.player = Player(self.level_width // 2, self.level_height // 2, player_sprites)
        self.camera = Camera(self.level_width, self.level_height)

        # Merchant NPC
        merchant_sprite = self.assets.load_image("merchant", scale=(64, 64))
        merchant = NPC(
            "merchant",
            NPC_DATA["merchant"]["name"],
            300,
            400,
            merchant_sprite,
            NPC_DATA["merchant"]["dialogue"]
        )
        self.npcs.append(merchant)

        # Enemies
        soldier_sprite = self.assets.load_image("soldier_right", scale=(64, 64))
        soldier_sprites = {"soldier": soldier_sprite}

        for i in range(4):
            x = 200 + i * 300
            y = 200
            enemy = Enemy(f"soldier_{i}", x, y, "soldier", soldier_sprites)
            self.enemies.append(enemy)

        # Coins
        icon = self.assets.load_image("icons", scale=(32, 32))
        for i in range(8):
            self.items.append(Coin(200 + i * 150, 500, icon))

        print("[LEVEL 2] Collect coins and trade with merchant!")

    # =========================================
    # 🧠 MERCHANT TRADE SYSTEM
    # =========================================
    def _handle_interact(self):
        if not self.player:
            return

        for npc in self.npcs:
            dist = math.sqrt((self.player.x - npc.x) ** 2 + (self.player.y - npc.y) ** 2)

            if dist < 100:
                if npc.id == "merchant":

                    if not self.traded_with_merchant:

                        if self.inventory.coins >= 5:
                            # TRADE SUCCESS
                            self.inventory.coins -= 5
                            self.traded_with_merchant = True

                            self.dialogue.start([
                                "Merchant: A fair trade!",
                                "You gave 5 coins.",
                                "The gate is now open."
                            ], npc.name)

                            print("[LEVEL 2] Trade complete!")

                            # 🚪 SPAWN DOOR AFTER TRADE
                            self._spawn_door()

                        else:
                            self.dialogue.start([
                                "Merchant: Bring me 5 coins.",
                                f"You have: {self.inventory.coins}"
                            ], npc.name)

                    else:
                        self.dialogue.start([
                            "Merchant: The gate is open.",
                            "Proceed forward."
                        ], npc.name)

                break

    # =========================================
    # 🚪 DOOR SPAWN AFTER TRADE
    # =========================================
    def _spawn_door(self):
        try:
            door_sprite = self.assets.load_image("door", scale=(80, 120))
        except:
            door_sprite = None

        self.door = Door(
            x=self.level_width - 150,
            y=self.level_height // 2,
            width=80,
            height=120,
            next_level=3,
            sprite=door_sprite
        )

        print("[LEVEL 2] Door to Level 3 unlocked!")

    # =========================================
    # UPDATE (CHECK DOOR COLLISION)
    # =========================================
    def update(self, dt):
        super().update(dt)

        if self.player and self.door:
            door_rect = pygame.Rect(self.door.x, self.door.y, self.door.width, self.door.height)

            if self.player.rect.colliderect(door_rect):
                print("[LEVEL 2] Entering Level 3...")
                self.next_level = 3
                self.level_complete = True

    # =========================================
    # DRAW DOOR
    # =========================================
    def draw(self, screen):
        super().draw(screen)

        if self.door:
            cam = self.camera.get_offset()
            self.door.draw(screen, cam)