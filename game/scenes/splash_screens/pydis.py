from game.constants import Paths, Window
from game.objects import ImageObject
from game.scenes.base.splash import Splash


class PyDisSplash(Splash):
    """
    This shows the Python Discord logo,
    fading in an out splash screen style.
    """

    name = "pydis"

    def __init__(self, manager):

        super().__init__(manager)

        # PyDis logo
        self.image = ImageObject(
            (0, 0),
            Paths.splash / "pydis_logo.png",
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
        self.next_scene = "jetbrains"
