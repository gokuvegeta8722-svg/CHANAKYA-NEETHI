"""
Pause State
"""

import pygame
from settings import *


class PauseState:
    """Pause menu"""
    
    def __init__(self):
        """Initialize"""
        self.options = ["RESUME", "MENU"]
        self.selected = 0
        self.font = pygame.font.Font(None, 50)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return "resume" if self.selected == 0 else "menu"
        return None
    
    def draw(self, screen):
        """Draw"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        title = self.font.render("PAUSED", True, GOLD)
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 150)))
        
        for i, opt in enumerate(self.options):
            color = GOLD if i == self.selected else WHITE
            text = self.font.render(opt, True, color)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, 300 + i*80)))