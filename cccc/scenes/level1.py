"""
Level 1: Poudanapura (Sama - Diplomacy)
"""

from scenes.base_level import BaseLevel
from entities import *
from systems import Camera
from settings import LEVEL_NAMES
from utils.constants import NPC_DATA


class Level1(BaseLevel):
    """Level 1: Poudanapura"""
    
    def __init__(self, assets_loader):
        """Initialize Level 1"""
        super().__init__(1, assets_loader)
        self.setup_level()
    
    def setup_level(self):
        """Setup Level 1"""
        print("\n" + "="*70)
        print(f"[LEVEL 1] {LEVEL_NAMES[1]} - Sama (Diplomacy)")
        print("Quest: Find the spy and gather intelligence")
        print("="*70 + "\n")
        
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
            
            # Load and create NPCs
            print("[LEVEL] Creating NPCs...")
            
            # Elder
            elder_sprite = self.assets.load_image("villager", scale=(64, 64))
            elder_dialogue = NPC_DATA["elder"]["dialogue"]
            elder = NPC("elder", NPC_DATA["elder"]["name"], 300, 400, elder_sprite, elder_dialogue)
            self.npcs.append(elder)
            
            # Spy
            spy_sprite = self.assets.load_image("spy", scale=(64, 64))
            spy_dialogue = NPC_DATA["spy"]["dialogue"]
            spy = NPC("spy", NPC_DATA["spy"]["name"], 1000, 200, spy_sprite, spy_dialogue)
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
            
            # Coins
            coin_sprite = self.assets.load_image("icons", scale=(32, 32))
            coin_positions = [
                (250, 300), (450, 350), (650, 280), (850, 400), (1050, 320),
                (300, 550), (700, 600), (1150, 450)
            ]
            
            for x, y in coin_positions:
                coin = Coin(x, y, coin_sprite)
                self.items.append(coin)
            
            # Map piece
            map_sprite = self.assets.load_image("icons", scale=(32, 32))
            map_piece = MapPiece(1000, 250, map_sprite)
            self.items.append(map_piece)
            
            # Memory shard
            shard_sprite = self.assets.load_image("icons", scale=(32, 32))
            shard = MemoryShard(600, 200, shard_sprite)
            self.items.append(shard)
            
            print("[LEVEL 1] Setup complete!")
            
        except (FileNotFoundError, RuntimeError, KeyError) as e:
            print(f"\n{'='*70}")
            print("[FATAL ERROR] Failed to load Level 1!")
            print(f"{e}")
            print(f"{'='*70}\n")
            raise