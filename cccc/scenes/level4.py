"""Level 4"""

import pygame

from scenes.base_level import BaseLevel
from entities import Player, Enemy, Coin, MapPiece
from systems import Camera
from entities.door import Door


class Level4(BaseLevel):
    def __init__(self, assets):
        super().__init__(4, assets)

        self.objective_complete = False
        self.door = None

        self.setup()
    
    def setup(self):
        print("\n[LEVEL 4] Varanasi - Danda (Force)\n")
        try:
            self.background = self.assets.load_image("level4_bg")
            self.level_width = self.background.get_width()
            self.level_height = self.background.get_height()
            
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
            
            self.player = Player(
                self.level_width // 2,
                self.level_height // 2,
                player_sprites
            )
            self.camera = Camera(self.level_width, self.level_height)
            
            archer_sprite = self.assets.load_image("archer", scale=(64, 64))
            archer_sprites = {"archer": archer_sprite}

            for i in range(6):
                x = 150 + i * 200
                y = 200
                enemy = Enemy(f"archer_{i}", x, y, "archer", archer_sprites)
                self.enemies.append(enemy)
            
            icon_sprite = self.assets.load_image("icons", scale=(32, 32))
            
            for i in range(12):
                x = 150 + i * 100
                y = 500
                coin = Coin(x, y, icon_sprite)
                self.items.append(coin)
            
            map_piece = MapPiece(400, 300, icon_sprite)
            self.items.append(map_piece)
            
            print("[LEVEL 4] Defeat all archers to unlock the door to Level 5!\n")

        except Exception as e:
            print(f"[ERROR] Level 4 setup failed: {e}")
            raise

    def update(self, dt):
        super().update(dt)

        if not self.objective_complete and len(self.enemies) == 0:
            self.objective_complete = True
            print("[LEVEL 4] Objective complete!")
            self._spawn_door()

        if self.player and self.door:
            door_rect = pygame.Rect(self.door.x, self.door.y, self.door.width, self.door.height)

            if self.player.rect.colliderect(door_rect):
                print("[LEVEL 4] Entering Level 5...")
                self.next_level = 5
                self.level_complete = True

    def _spawn_door(self):
        try:
            door_sprite = self.assets.load_image("door", scale=(80, 120))
        except Exception:
            door_sprite = None

        self.door = Door(
            x=self.level_width - 150,
            y=self.level_height // 2,
            width=80,
            height=120,
            next_level=5,
            sprite=door_sprite
        )

        print("[LEVEL 4] Door to Level 5 unlocked!")

    def draw(self, screen):
        super().draw(screen)

        if self.door:
            cam = self.camera.get_offset()
            self.door.draw(screen, cam)