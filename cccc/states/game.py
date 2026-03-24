"""
Game State
"""

from scenes.level1 import Level1
from scenes.level2 import Level2
from scenes.level3 import Level3
from scenes.level4 import Level4
from scenes.level5 import Level5


class GameState:
    """Game state"""
    
    def __init__(self, assets):
        """Initialize"""
        self.assets = assets
        self.current_level = None
        self.load_level(1)
    
    def load_level(self, num):
        """Load level"""
        print(f"\n[GAME] Loading Level {num}...")
        
        levels = {
            1: Level1,
            2: Level2,
            3: Level3,
            4: Level4,
            5: Level5,
        }
        
        if num in levels:
            self.current_level = levels[num](self.assets)
    
    def update(self, dt):
        """Update"""
        if self.current_level:
            self.current_level.update(dt)
    
    def draw(self, screen):
        """Draw"""
        if self.current_level:
            self.current_level.draw(screen)