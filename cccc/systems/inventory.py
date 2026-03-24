"""Inventory"""


class Inventory:
    def __init__(self):
        self.coins = 0
        self.map_pieces = 0
        self.memory_shards = 0

    def add_coin(self, amount=1):
        self.coins += amount

    def add_map_piece(self):
        if self.map_pieces < 4:
            self.map_pieces += 1

    def add_memory_shard(self):
        if self.memory_shards < 3:
            self.memory_shards += 1