"""
Global Game Settings
"""

import os

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Chanakya Neethi - Master Strategy. Execute Victory."

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
DARK_BROWN = (70, 45, 25)
LIGHT_BROWN = (235, 225, 200)
RED = (200, 50, 50)
GREEN = (100, 200, 100)
GRAY = (128, 128, 128)

# States
GAME_STATE_MENU = "menu"
GAME_STATE_GAME = "game"
GAME_STATE_PAUSE = "pause"

# Levels
LEVEL_NAMES = {1: "Poudanapura", 2: "Bharukaccha", 3: "Vidisha", 4: "Varanasi", 5: "Pataliputra"}

# Player
PLAYER_SPEED = 250
PLAYER_MAX_HEALTH = 100

# Asset paths
ASSET_PATHS = {
    "player_idle": "assets\\player\\idle.png",
    "player_walk_up": "assets\\player\\walk_up.png",
    "player_walk_down": "assets\\player\\walk_down.png",
    "player_walk_left": "assets\\player\\walk_left.png",
    "player_walk_right": "assets\\player\\walk_right.png",
    "player_attack_up": "assets\\player\\attack_up.png",
    "player_attack_down": "assets\\player\\attack_down.png",
    "player_attack_left": "assets\\player\\attack_left.png",
    "player_attack_right": "assets\\player\\attack_right.png",
    
    "soldier": "assets\\enemies\\soldier.png",
    "soldier_right": "assets\\enemies\\soldier_right.png",
    "soldier_attack": "assets\\enemies\\soldier_attack.png",
    "archer": "assets\\enemies\\archer.png",
    "archer1": "assets\\enemies\\archer1.png",
    "archer2": "assets\\enemies\\archer2.png",
    "boss": "assets\\enemies\\boss.png",
    "boss_action": "assets\\enemies\\boss_action.png",
    "boss_attack": "assets\\enemies\\boss_attack.png",
    
    "villager": "assets\\npcs\\villager.png",
    "merchant": "assets\\npcs\\merchant.png",
    "spy": "assets\\npcs\\spy.png",
    "nanda": "assets\\npcs\\nanda.png",
    
    "level1_bg": "assets\\levels\\level1_bg.jpeg",
    "level2_bg": "assets\\levels\\level2_bg.png",
    "level3_bg": "assets\\levels\\level3_bg.png",
    "level4_bg": "assets\\levels\\level4_bg.png",
    "level5_bg": "assets\\levels\\level5_bg.png",
    
    "button": "assets\\ui\\button.png",
    "panel": "assets\\ui\\panel.png",
    "icons": "assets\\ui\\icons.png",
    
    "blood": "assets\\effects\\blood.png",
    "spark": "assets\\effects\\spark.png",
    "heal": "assets\\effects\\heal.png",
}