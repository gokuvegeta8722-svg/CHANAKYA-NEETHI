"""
Combat System
"""

import math


class CombatSystem:
    """Handle combat"""
    
    def __init__(self):
        """Initialize"""
        self.player_attack_active = False
        self.player_attack_damage = 20
        self.player_attack_range = 60
        self.player_attack_cooldown = 0.5
        self.player_attack_timer = 0
    
    def update(self, dt):
        """Update combat"""
        if self.player_attack_timer > 0:
            self.player_attack_timer -= dt
        else:
            self.player_attack_active = False
    
    def can_attack(self):
        """Can player attack?"""
        return self.player_attack_timer <= 0
    
    def attack(self):
        """Perform attack"""
        if self.can_attack():
            self.player_attack_active = True
            self.player_attack_timer = self.player_attack_cooldown
            return True
        return False
    
    def check_hit(self, attacker_pos, defender_pos):
        """Check if attack hits"""
        dx = defender_pos[0] - attacker_pos[0]
        dy = defender_pos[1] - attacker_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < self.player_attack_range