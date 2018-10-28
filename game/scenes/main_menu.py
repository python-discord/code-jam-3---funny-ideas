from pathlib import Path

from game.constants import Colors, Window
from game.manager import SceneManager
from game.objects import BaseObject, FloatingObject
from game.scenes.scene import Scene


class MainMenu(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """
    def __init__(self, manager: SceneManager):

        super().__init__(manager)
        menu_graphics = Path("game", "assets", "graphics", "main_menu")

        # Main game logo
        self.logo = BaseObject(
            (0, 0),
            menu_graphics / "logo.png",
        )

        # Move the logo to the right position, based on screen size.
        image_width = self.logo.size[0]
        logo_location = (
            (Window.width / 2) - (image_width / 2),
            40,
        )
        self.logo.move_absolute(logo_location)

        # Background image
        self.background = BaseObject(
            (0, 0),
            menu_graphics / "background.png",
        )

        # Flutterdude
        self.flutterdude = FloatingObject(
            (980, 260),
            menu_graphics / "flutterdude.png",
            float_range=(260, 280),
            float_speed=4,
        )

        # Brainmon
        self.brainmon = FloatingObject(
            (900, 400),
            menu_graphics / "brainmon.png",
            float_range=(390, 400),
            float_speed=3,
        )

    def handle_events(self):
        pass

    def draw(self):
        self.screen.fill(Colors.black)
        self.background.draw()
        self.logo.draw()
        self.brainmon.draw()
        self.flutterdude.draw()
