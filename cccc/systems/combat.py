"""
Combat System
"""


class CombatSystem:
    """Handles combat calculations"""

    def __init__(self):
        pass

    def calculate_damage(self, attacker, defender):
        """Calculate damage"""
        if attacker is None or defender is None:
            return 0

        if hasattr(attacker, "damage"):
            return attacker.damage

        if hasattr(attacker, "attacking"):
            return 10

        return 5