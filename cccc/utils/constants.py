"""
Game Constants
"""

# NPC Dialogue Data
NPC_DATA = {
    "elder": {
        "name": "Village Elder",
        "dialogue": [
            "Welcome, young warrior!",
            "Dark times have come under King Nanda.",
            "A mysterious man was seen in the northern forest.",
            "He holds information about Nanda's weakness.",
            "Find him and gather what you can.",
            "May your journey be safe!"
        ]
    },
    "spy": {
        "name": "Mysterious Spy",
        "dialogue": [
            "You found me at last!",
            "I am a resistance fighter.",
            "King Nanda grows more tyrannical each day.",
            "His capital, Pataliputra, is heavily fortified.",
            "Here, take this map piece.",
            "It shows one route to the palace.",
            "Collect all four pieces to see the full picture.",
            "Go to Bharukaccha next.",
            "My contact awaits you there.",
            "May Chanakya's wisdom guide you..."
        ]
    },
    "merchant": {
        "name": "Merchant",
        "dialogue": [
            "Welcome to my shop!",
            "I sell weapons and supplies.",
            "Gold coins are always welcome here.",
            "Map pieces? Those are very valuable...",
            "Perhaps we can trade?"
        ]
    },
    "nanda": {
        "name": "King Nanda",
        "dialogue": [
            "So, you have come to challenge me?",
            "I am the rightful king of Magadha!",
            "None shall defeat the Nanda dynasty!",
            "Prepare to meet your doom!"
        ]
    }
}

# Level Objectives
LEVEL_OBJECTIVES = {
    1: [
        "Explore Poudanapura village",
        "Talk to the villagers",
        "Find the mysterious spy",
        "Collect map pieces"
    ],
    2: [
        "Navigate the trading city",
        "Make strategic choices",
        "Gather allies and resources",
        "Defeat enemy guards"
    ],
    3: [
        "Meet military strategists",
        "Plan the army composition",
        "Gather resources for battle",
        "Prepare for final confrontation"
    ],
    4: [
        "Fight through the city",
        "Defeat enemy generals",
        "Collect final map piece",
        "Ready yourself for palace assault"
    ],
    5: [
        "Infiltrate the palace",
        "Defeat King Nanda",
        "Choose your ending",
        "Save or destroy the kingdom"
    ]
}

# Enemy Data
ENEMY_DATA = {
    "soldier": {
        "health": 30,
        "damage": 10,
        "speed": 100,
        "coins": 25
    },
    "archer": {
        "health": 20,
        "damage": 15,
        "speed": 120,
        "coins": 35
    },
    "general": {
        "health": 50,
        "damage": 20,
        "speed": 100,
        "coins": 100
    },
    "boss": {
        "health": 200,
        "damage": 30,
        "speed": 80,
        "coins": 500
    }
}