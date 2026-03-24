"""
Inventory System
"""


class InventorySystem:
    """Manage player inventory"""
    
    def __init__(self):
        """Initialize"""
        self.coins = 0
        self.map_pieces = 0
        self.memory_shards = 0
    
    def add_coins(self, amount):
        """Add coins"""
        self.coins += amount
    
    def add_map_piece(self):
        """Add map piece"""
        self.map_pieces = min(self.map_pieces + 1, 4)
    
    def add_memory_shard(self):
        """Add memory shard"""
        self.memory_shards = min(self.memory_shards + 1, 3)