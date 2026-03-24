"""Level 4"""
from scenes.base_level import BaseLevel
from entities import Player, Enemy, Coin, MapPiece, MemoryShard
from systems import Camera


class Level4(BaseLevel):
    def __init__(self, assets):
        super().__init__(4, assets)
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
            
            self.player = Player(self.level_width // 2, self.level_height // 2, player_sprites)
            self.camera = Camera(self.level_width, self.level_height)
            
            archer_sprite = self.assets.load_image("archer", scale=(64, 64))
            for i in range(6):
                x = 150 + i * 200
                y = 200
                enemy = Enemy(f"archer_{i}", x, y, "archer", archer_sprite)
                self.enemies.append(enemy)
            
            icon_sprite = self.assets.load_image("icons", scale=(32, 32))
            
            for i in range(12):
                x = 150 + i * 100
                y = 500
                coin = Coin(x, y, icon_sprite)
                self.items.append(coin)
            
            map_piece = MapPiece(400, 300, icon_sprite)
            self.items.append(map_piece)
            
            print("[LEVEL 4] Ready!\n")
        except Exception as e:
            print(f"[ERROR] Level 4 setup failed: {e}")
            raise