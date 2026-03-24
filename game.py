class Game:
    def __init__(self):
        self.running = True
        self.current_scene = None
        self.scenes = {}

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        self.current_scene = self.scenes.get(name)

    def game_loop(self):
        while self.running:
            if self.current_scene:
                self.current_scene.update()
                self.current_scene.render()

    def stop(self):
        self.running = False

# Example of how to use the Game class
if __name__ == '__main__':
    game = Game()
    game.add_scene('main_menu', MainMenuScene())  # Ensure MainMenuScene is defined
    game.set_scene('main_menu')
    game.game_loop()