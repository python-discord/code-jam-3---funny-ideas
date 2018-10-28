from game.constants import Colors
from game.scenes.scene import Scene


class Game(Scene):

    def __init__(self, manager):
        super().__init__(manager)

    def handle_events(self):
        pass

    def draw(self):
        self.screen.fill(Colors.black)
