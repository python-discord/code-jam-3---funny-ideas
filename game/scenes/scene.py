from game import screen
from game.constants import Colors


class Scene:
    """
    A base class for all scenes.

    Scenes are interactive views in the game, such
    as the credits screen, the settings screen, the
    main menu and the game itself.
    """
    def __init__(self, manager):
        self.screen = screen
        self.manager = manager

    def handle_events(self):
        pass

    def draw(self):
        pass

    def teardown(self):
        self.screen.fill(Colors.black)
