"""
Collision Detection
"""

import math


class CollisionSystem:
    """Handle collisions"""
    
    @staticmethod
    def check_rect(rect1, rect2):
        """Check rect collision"""
        return rect1.colliderect(rect2)
    
    @staticmethod
    def check_distance(pos1, pos2, distance):
        """Check distance between two points"""
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        actual_distance = math.sqrt(dx*dx + dy*dy)
        return actual_distance < distance