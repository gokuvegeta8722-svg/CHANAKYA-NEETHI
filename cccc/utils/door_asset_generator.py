"""
Door Asset Generator
Creates a simple door PNG image for testing
Run this if you don't have door.png in assets/ui/
"""

import pygame
import os

def create_door_asset(output_path="assets/ui/door.png"):
    """
    Create a simple door asset
    
    Args:
        output_path: Where to save the door image
    """
    
    # Create assets/ui directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Door dimensions
    width = 80
    height = 120
    
    # Create surface
    door_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw door frame (brown wooden door)
    pygame.draw.rect(door_surface, (139, 69, 19), (0, 0, width, height))  # Dark brown background
    
    # Door panels
    pygame.draw.line(door_surface, (101, 50, 15), (width//2, 5), (width//2, height-5), 2)  # Vertical divider
    pygame.draw.line(door_surface, (101, 50, 15), (5, height//2), (width-5, height//2), 2)  # Horizontal divider
    
    # Door frame border
    pygame.draw.rect(door_surface, (205, 133, 63), (0, 0, width, height), 3)  # Light brown border
    
    # Door handle (golden knob)
    pygame.draw.circle(door_surface, (255, 215, 0), (width - 15, height // 2), 6)  # Golden knob
    
    # Door hinge (small circles on left side)
    pygame.draw.circle(door_surface, (169, 169, 169), (3, 15), 2)  # Top hinge
    pygame.draw.circle(door_surface, (169, 169, 169), (3, height - 15), 2)  # Bottom hinge
    
    # Save
    pygame.image.save(door_surface, output_path)
    print(f"\n✅ Door asset created: {output_path}")
    return output_path


def create_door_with_lock(output_path="assets/ui/door_locked.png"):
    """
    Create a locked door asset
    
    Args:
        output_path: Where to save the locked door image
    """
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    width = 80
    height = 120
    
    door_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Door (lighter shade indicating locked)
    pygame.draw.rect(door_surface, (120, 60, 20), (0, 0, width, height))  # Darker brown
    
    # Door panels
    pygame.draw.line(door_surface, (80, 40, 15), (width//2, 5), (width//2, height-5), 2)
    pygame.draw.line(door_surface, (80, 40, 15), (5, height//2), (width-5, height//2), 2)
    
    # Door frame
    pygame.draw.rect(door_surface, (185, 113, 43), (0, 0, width, height), 3)
    
    # Lock icon (padlock)
    pygame.draw.rect(door_surface, (192, 192, 192), (width//2 - 8, height//2 - 5, 16, 10), 1)  # Lock body
    pygame.draw.arc(door_surface, (192, 192, 192), (width//2 - 10, height//2 - 15, 20, 15), 0, 3.14, 2)  # Shackle
    
    pygame.image.save(door_surface, output_path)
    print(f"✅ Locked door asset created: {output_path}")


if __name__ == "__main__":
    pygame.init()
    
    print("\n" + "="*70)
    print("DOOR ASSET GENERATOR")
    print("="*70)
    
    # Create normal door
    create_door_asset("assets/ui/door.png")
    
    # Create locked door variant
    create_door_with_lock("assets/ui/door_locked.png")
    
    print("\n" + "="*70)
    print("✅ Door assets generated successfully!")
    print("="*70 + "\n")
