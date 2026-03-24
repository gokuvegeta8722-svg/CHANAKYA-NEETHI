"""Level 3"""

import pygame

from scenes.base_level import BaseLevel
from entities import Player, Enemy, Coin, MapPiece
from systems import Camera
from entities.door import Door


class Level3(BaseLevel):
    def __init__(self, assets):
        super().__init__(3, assets)

        self.objective_complete = False
        self.door = None

        self.setup()
    
    def setup(self):
        print("\n[LEVEL 3] Vidisha - Bheda (Strategy)\n")

        self.background = self.assets.load_image("level3_bg")
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
        
        soldier_sprite = self.assets.load_image("soldier_attack", scale=(64, 64))
        soldier_sprites = {"soldier": soldier_sprite}

        for i in range(5):
            x = 150 + i * 250
            y = 200
            enemy = Enemy(f"soldier_{i}", x, y, "soldier", soldier_sprites)
            self.enemies.append(enemy)
        
        icon_sprite = self.assets.load_image("icons", scale=(32, 32))
        
        for i in range(10):
            x = 150 + i * 120
            y = 500
            coin = Coin(x, y, icon_sprite)
            self.items.append(coin)
        
        self.items.append(MapPiece(600, 300, icon_sprite))

        print("[LEVEL 3] Defeat all enemies to unlock door!")

    def update(self, dt):
        super().update(dt)

        if not self.objective_complete and len(self.enemies) == 0:
            self.objective_complete = True
            print("[LEVEL 3] Objective complete!")
            self._spawn_door()

        if self.player and self.door:
            door_rect = pygame.Rect(self.door.x, self.door.y, self.door.width, self.door.height)

            if self.player.rect.colliderect(door_rect):
                print("[LEVEL 3] Entering Level 4...")
                self.next_level = 4
                self.level_complete = True

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
            next_level=4,
            sprite=door_sprite
        )

        print("[LEVEL 3] Door unlocked!")

    def draw(self, screen):
        super().draw(screen)

        if self.door:
            cam = self.camera.get_offset()
            self.door.draw(screen, cam)