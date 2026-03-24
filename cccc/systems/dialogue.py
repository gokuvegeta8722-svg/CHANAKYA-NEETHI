"""
Dialogue System
"""


class DialogueManager:
    """Manage NPC dialogue"""
    
    def __init__(self):
        """Initialize"""
        self.current_dialogue = None
        self.index = 0
        self.active = False
        self.speaker = ""
    
    def start(self, lines, speaker="NPC"):
        """Start dialogue"""
        self.current_dialogue = lines
        self.index = 0
        self.active = True
        self.speaker = speaker
        print(f"[DIALOGUE] {speaker} started talking")
    
    def next_line(self):
        """Go to next line"""
        self.index += 1
        if self.index >= len(self.current_dialogue):
            self.active = False
            print(f"[DIALOGUE] Conversation ended")
    
    def get_current_line(self):
        """Get current line"""
        if not self.active or not self.current_dialogue:
            return None
        if self.index < len(self.current_dialogue):
            return self.current_dialogue[self.index]
        return None