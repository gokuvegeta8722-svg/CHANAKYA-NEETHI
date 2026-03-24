"""
Level 1: Poudanapura (Sama - Diplomacy)
"""

import pygame
from scenes.base_level import BaseLevel
from entities import Player, NPC, Enemy, Coin, MapPiece, MemoryShard
from systems import Camera
from settings import LEVEL_NAMES
from utils.constants import NPC_DATA
from entities.door import Door


class Level1(BaseLevel):
    """Level 1: Poudanapura - with door to Level 2"""

    def __init__(self, assets_loader):
        """Initialize Level 1"""
        super().__init__(1, assets_loader)
        self.door = None
        self.setup_level()

    def setup_level(self):
        """Setup Level 1"""
        print("\n" + "=" * 70)
        print(f"[LEVEL 1] {LEVEL_NAMES[1]} - Sama (Diplomacy)")
        print("Quest: Find the spy and gather intelligence")
        print("=" * 70 + "\n")

        try:
            # Load background
            print("[LEVEL] Loading background...")
            self.background = self.assets.load_image("level1_bg")
            self.level_width = self.background.get_width()
            self.level_height = self.background.get_height()
            print(f"[LEVEL] Background loaded: {self.level_width}x{self.level_height}")

            # Load player sprites
            print("[LEVEL] Loading player sprites...")
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

            # Create player
            self.player = Player(
                self.level_width // 2,
                self.level_height // 2,
                player_sprites
            )

            # Create camera
            self.camera = Camera(self.level_width, self.level_height)

            # Create NPCs
            print("[LEVEL] Creating NPCs...")

            elder_sprite = self.assets.load_image("villager", scale=(64, 64))
            elder = NPC(
                "elder",
                NPC_DATA["elder"]["name"],
                300,
                400,
                elder_sprite,
                NPC_DATA["elder"]["dialogue"]
            )
            self.npcs.append(elder)

            spy_sprite = self.assets.load_image("spy", scale=(64, 64))
            spy = NPC(
                "spy",
                NPC_DATA["spy"]["name"],
                1000,
                200,
                spy_sprite,
                NPC_DATA["spy"]["dialogue"]
            )
            self.npcs.append(spy)

            # Create enemies
            print("[LEVEL] Creating enemies...")
            soldier_sprite = self.assets.load_image("soldier", scale=(64, 64))
            for i in range(3):
                x = 200 + i * 400
                y = 150
                enemy = Enemy(f"soldier_{i}", x, y, "soldier", {"soldier": soldier_sprite})
                self.enemies.append(enemy)

            # Create items
            print("[LEVEL] Creating items...")
            icon_sprite = self.assets.load_image("icons", scale=(32, 32))

            coin_positions = [
                (250, 300), (450, 350), (650, 280), (850, 400),
                (1050, 320), (300, 550), (700, 600), (1150, 450)
            ]
            for x, y in coin_positions:
                self.items.append(Coin(x, y, icon_sprite))

            self.items.append(MapPiece(1000, 250, icon_sprite))
            self.items.append(MemoryShard(600, 200, icon_sprite))

            # Door to level 2
            print("[LEVEL] Creating door to Level 2...")
            try:
                door_sprite = self.assets.load_image("door", scale=(80, 120))
            except Exception:
                print("[LEVEL] Door sprite not found, using placeholder")
                door_sprite = None

            self.door = Door(
                x=self.level_width - 150,
                y=self.level_height // 2 - 60,
                width=80,
                height=120,
                next_level=2,
                sprite=door_sprite
            )

            print("[LEVEL 1] Setup complete!")
            print(f"[LEVEL 1] Door placed at ({self.door.x}, {self.door.y})")
            print("[LEVEL 1] Go explore and find the spy! Then reach the door to Level 2.\n")

        except (FileNotFoundError, RuntimeError, KeyError) as e:
            print("\n" + "=" * 70)
            print("[FATAL ERROR] Failed to load Level 1!")
            print(e)
            print("=" * 70 + "\n")
            raise

    def update(self, dt):
        """Update level"""
        super().update(dt)

        # Door check: player can proceed only after getting map piece
        if self.player and self.door:
            door_rect = pygame.Rect(self.door.x, self.door.y, self.door.width, self.door.height)
            if self.player.rect.colliderect(door_rect):
                if self.inventory.map_pieces > 0:
                    print("[LEVEL 1] Door reached. Proceeding to Level 2...")
                    self.next_level = self.door.activate()
                    self.level_complete = True

    def draw(self, screen):
        """Draw level"""
        super().draw(screen)

        if self.door:
            cam = self.camera.get_offset() if self.camera else (0, 0)
            self.door.draw(screen, cam)