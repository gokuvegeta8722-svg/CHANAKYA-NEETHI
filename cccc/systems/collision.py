"""
Collision Detection
"""

import math
import pygame


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
        actual_distance = math.sqrt(dx * dx + dy * dy)
        return actual_distance < distance

    @staticmethod
    def check_collision(obj1, obj2):
        """Check collision between two game objects"""
        if obj1 is None or obj2 is None:
            return False

        rect1 = CollisionSystem.get_rect(obj1)
        rect2 = CollisionSystem.get_rect(obj2)

        if rect1 is None or rect2 is None:
            return False

        return rect1.colliderect(rect2)

    @staticmethod
    def get_rect(obj):
        """Get rect from object"""
        if hasattr(obj, "rect"):
            return obj.rect

        if hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "width") and hasattr(obj, "height"):
            return pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))

        return None