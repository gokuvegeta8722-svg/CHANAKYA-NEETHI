"""Level 5"""

import pygame

from scenes.base_level import BaseLevel
from entities import Player, Boss, Coin
from systems import Camera


class Level5(BaseLevel):
    def __init__(self, assets):
        super().__init__(5, assets)

        self.objective_complete = False
        self.setup()
    
    def setup(self):
        print("\n[LEVEL 5] Pataliputra - Final Confrontation\n")
        try:
            self.background = self.assets.load_image("level5_bg")
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
            
            # FIX: boss sprite must be passed as a dict
            boss_sprite = self.assets.load_image("boss", scale=(96, 96))
            boss_sprites = {"boss": boss_sprite}

            self.boss = Boss("nanda", 600, 250, boss_sprites)
            self.enemies.append(self.boss)
            
            icon_sprite = self.assets.load_image("icons", scale=(32, 32))
            
            for i in range(15):
                x = 150 + i * 80
                y = 500
                coin = Coin(x, y, icon_sprite)
                self.items.append(coin)
            
            print("[LEVEL 5] Defeat the boss to win the game!\n")

        except Exception as e:
            print(f"[ERROR] Level 5 setup failed: {e}")
            raise

    def update(self, dt):
        super().update(dt)

        if not self.objective_complete and len(self.enemies) == 0:
            self.objective_complete = True
            print("\n🎉 GAME COMPLETED! YOU DEFEATED NANDA! 🎉\n")
            self.level_complete = True
            self.next_level = None

    def draw(self, screen):
        super().draw(screen)

        if self.objective_complete:
            font = pygame.font.Font(None, 50)
            text = font.render("YOU WIN!", True, (255, 215, 0))
            screen.blit(text, (self.level_width // 2 - 100, 100))