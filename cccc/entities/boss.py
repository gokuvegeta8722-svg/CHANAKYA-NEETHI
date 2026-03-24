"""
Boss Enemy - King Nanda
"""

from entities.enemy import Enemy
from utils.constants import ENEMY_DATA


class Boss(Enemy):
    """Boss enemy"""
    
    def __init__(self, boss_id, x, y, sprite_dict):
        """Initialize boss"""
        super().__init__(boss_id, x, y, "boss", sprite_dict)
        
        # Boss stats override
        if "boss" in ENEMY_DATA:
            data = ENEMY_DATA["boss"]
            self.health = data["health"]
            self.max_health = data["health"]
            self.damage = data["damage"]
            self.speed = data["speed"]
            self.coins_reward = data["coins"]
        
        print(f"[BOSS] King Nanda spawned!")