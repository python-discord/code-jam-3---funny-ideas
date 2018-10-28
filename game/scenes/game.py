from game.constants import Colors
from game.manager import SceneManager
from game.scenes import Scene


class Game(Scene):

    def __init__(self, manager: SceneManager):
        super().__init__(manager)

    def handle_events(self):
        pass

    def draw(self):
        self.screen.fill(Colors.black)
