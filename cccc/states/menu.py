"""
Menu State
"""

import pygame
from settings import *


class MenuState:
    """Main menu"""
    
    def __init__(self):
        """Initialize"""
        self.options = ["PLAY", "OPTIONS", "EXIT"]
        self.selected = 0
        self.title_font = pygame.font.Font(None, 80)
        self.option_font = pygame.font.Font(None, 50)
        self.subtitle_font = pygame.font.Font(None, 30)
    
    def handle_event(self, event):
        """Handle events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    return "start_game"
                elif self.selected == 2:
                    return "quit"
        return None
    
    def draw(self, screen):
        """Draw"""
        try:
            screen.fill(DARK_BROWN)
            
            # Title
            title = self.title_font.render("CHANAKYA NEETHI", True, GOLD)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.subtitle_font.render("Master Strategy. Execute Victory.", True, WHITE)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 180))
            screen.blit(subtitle, subtitle_rect)
            
            # Options
            for i, opt in enumerate(self.options):
                color = GOLD if i == self.selected else LIGHT_BROWN
                text = self.option_font.render(f"[{opt}]", True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 300 + i*80))
                screen.blit(text, text_rect)
        except Exception as e:
            print(f"[ERROR] Menu draw failed: {e}")