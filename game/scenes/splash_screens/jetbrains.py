from pathlib import Path

from game.constants import Window
from game.objects import ImageObject
from game.scenes.base.splash import Splash


class JetBrainsSplash(Splash):
    """
    This shows "sponsored by Jetbrains",
    fading in an out splash screen style.
    """

    name = "jetbrains"

    def __init__(self, manager):

        super().__init__(manager)

        # JetBrains logo
        self.image = ImageObject(
            (0, 0),
            Path("game", "assets", "graphics", "jetbrains_logo.png"),
        )

        # Center the image
        image_width = self.image.surface.get_rect().width
        image_height = self.image.surface.get_rect().height

        center = (
            (Window.width / 2) - (image_width / 2),
            (Window.height / 2) - (image_height / 2),
        )

        # Move the logo to the right position, based on screen size.
        self.image.move_absolute(center)

        # What scene should be loaded after this finishes?
        self.next_scene = "main_menu"
