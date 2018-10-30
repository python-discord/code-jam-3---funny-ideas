from game.constants import Colors
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

    def handle_events(self, event):
        pass

    def draw(self):
        self.screen.fill(Colors.black)
