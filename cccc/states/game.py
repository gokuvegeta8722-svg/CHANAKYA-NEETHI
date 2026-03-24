"""
Game State - Updated with Level Transition System
"""

from scenes.level1 import Level1
from scenes.level2 import Level2
from scenes.level3 import Level3
from scenes.level4 import Level4
from scenes.level5 import Level5


class GameState:
    """Game state with level transitions"""
    
    def __init__(self, assets):
        """Initialize"""
        self.assets = assets
        self.current_level = None
        self.current_level_num = 1
        self.load_level(1)
    
    def load_level(self, num):
        """
        Load level
        
        Args:
            num: Level number (1-5)
        """
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
            self.current_level_num = num
            print(f"[GAME] Level {num} loaded successfully!\n")
        else:
            print(f"[ERROR] Level {num} not found!")
    
    def check_level_transition(self):
        """
        Check if current level is complete and needs transition
        
        Returns:
            True if level transition occurred
        """
        if self.current_level and self.current_level.level_complete:
            next_level = self.current_level.next_level
            
            if next_level and next_level <= 5:
                print(f"\n[GAME] ===== LEVEL {self.current_level_num} COMPLETE =====")
                print(f"[GAME] Transitioning to Level {next_level}...")
                self.load_level(next_level)
                return True
            elif next_level and next_level > 5:
                print(f"\n[GAME] ===== GAME COMPLETE! =====")
                print(f"[GAME] All levels finished!")
                return "game_complete"
        
        return False
    
    def update(self, dt):
        """Update"""
        if self.current_level:
            self.current_level.update(dt)
            
            # Check for level transition
            self.check_level_transition()
    
    def draw(self, screen):
        """Draw"""
        if self.current_level:
            self.current_level.draw(screen)
