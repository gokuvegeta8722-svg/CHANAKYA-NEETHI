"""Dialogue"""


class DialogueManager:
    def __init__(self):
        self.active = False
        self.lines = []
        self.index = 0
        self.speaker = ""

    def start(self, lines, speaker="NPC"):
        if isinstance(lines, str):
            lines = [lines]
        self.lines = lines
        self.index = 0
        self.active = True
        self.speaker = speaker

    def next(self):
        self.index += 1
        if self.index >= len(self.lines):
            self.active = False

    def next_line(self):
        self.next()

    def get_line(self):
        if not self.active or self.index >= len(self.lines):
            return None
        return self.lines[self.index]

    def get_current_line(self):
        return self.get_line()

    def update(self, dt):
        pass