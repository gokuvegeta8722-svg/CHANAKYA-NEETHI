"""
Chanakya Neethi - Main Game Entry Point (UPDATED WITH DOOR SYSTEM)
"""

import pygame
import sys
import os

# Initialize pygame FIRST
pygame.init()
pygame.display.init()

from settings import *
from utils.asset_loader import AssetLoader
from states.menu import MenuState
from states.game import GameState
from states.pause import PauseState


class Game:
    """Main game with door/level transition system"""
    
    def __init__(self):
        """Initialize"""
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption(TITLE)
            
            self.clock = pygame.time.Clock()
            self.running = True
            
            # Load assets
            print("\n[GAME] Loading assets...")
            self.assets = AssetLoader(".")
            
            # Verify assets
            if not self.assets.verify_all_assets():
                print("[FATAL] Missing required assets!")
                sys.exit(1)
            
            # States
            self.state = GAME_STATE_MENU
            self.menu = MenuState()
            self.game = None
            self.pause = PauseState()
            
            print("[GAME] Ready!\n")
        
        except Exception as e:
            print(f"[FATAL] Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    def handle_events(self):
        """Handle events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if self.state == GAME_STATE_MENU:
                    action = self.menu.handle_event(event)
                    if action == "start_game":
                        print("[GAME] Starting game...")
                        self.game = GameState(self.assets)  # Using updated GameState
                        self.state = GAME_STATE_GAME
                    elif action == "quit":
                        self.running = False
                        return
                
                elif self.state == GAME_STATE_GAME:
                    if event.key == pygame.K_ESCAPE:
                        print("[GAME] Pausing...")
                        self.state = GAME_STATE_PAUSE
                    elif event.key == pygame.K_SPACE:
                        if self.game and self.game.current_level:
                            self.game.current_level.handle_space()
                    elif event.key == pygame.K_e:
                        # E key for interaction (door or NPC)
                        if self.game and self.game.current_level:
                            self.game.current_level.handle_event(event)
                    else:
                        if self.game and self.game.current_level:
                            self.game.current_level.handle_event(event)
                
                elif self.state == GAME_STATE_PAUSE:
                    action = self.pause.handle_event(event)
                    if action == "resume":
                        print("[GAME] Resuming...")
                        self.state = GAME_STATE_GAME
                    elif action == "menu":
                        print("[GAME] Returning to menu...")
                        self.state = GAME_STATE_MENU
    
    def update(self, dt):
        """Update"""
        try:
            if self.state == GAME_STATE_GAME and self.game:
                self.game.update(dt)
        except Exception as e:
            print(f"[ERROR] Update failed: {e}")
    
    def draw(self):
        """Draw"""
        try:
            self.screen.fill(BLACK)
            
            if self.state == GAME_STATE_MENU:
                self.menu.draw(self.screen)
            elif self.state == GAME_STATE_GAME and self.game:
                self.game.draw(self.screen)
            elif self.state == GAME_STATE_PAUSE:
                if self.game:
                    self.game.draw(self.screen)
                self.pause.draw(self.screen)
            
            pygame.display.flip()
        except Exception as e:
            print(f"[ERROR] Draw failed: {e}")
    
    def run(self):
        """Main loop"""
        print("[GAME] Starting main loop...\n")
        
        try:
            while self.running:
                dt = self.clock.tick(FPS) / 1000.0
                
                self.handle_events()
                self.update(dt)
                self.draw()
        
        except KeyboardInterrupt:
            print("\n[GAME] Interrupted by user")
        except Exception as e:
            print(f"\n[FATAL] Game loop error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.quit()
    
    def quit(self):
        """Shutdown game"""
        print("\n[GAME] Shutting down...")
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"[FATAL] Failed to start game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
