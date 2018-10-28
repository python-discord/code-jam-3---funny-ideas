from game import screen
from game.manager import SceneManager


class Scene:
    """
    A base class for all scenes.

    Scenes are interactive views in the game, such
    as the credits screen, the settings screen, the
    main menu and the game itself.
    """
    def __init__(self, manager: SceneManager):
        self.screen = screen
        self.manager = manager

    def handle_events(self):
        pass

    def draw(self):
        pass
