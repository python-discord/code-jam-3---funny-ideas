from pathlib import Path
from typing import Tuple, Union

from game.objects.image import ImageObject


class FloatingObject(ImageObject):
    """
    A BaseObject that floats up and down.
    """

    def __init__(
            self,
            scene,
            location: Tuple[int, int],
            image_path: Union[Path, str],
            float_range: Tuple[int, int],
            float_speed: float,
            *,
            size: Tuple[int, int] = None
    ):
        """
        Constructs a new game object that floats up and down.

        :param location: The top-left coordinate of the object on the screen
        :param image_path: The path to the image that will be displayed on the screen
        :param float_range: The y coordinate range within which to float up and down.
        :param float_speed: The speed at which to float.
        :param size: Optionally, the size of the object - if provided, will transform the image instead of
                     assuming the size of the image is correct
        """

        self.min_y = float_range[0]
        self.max_y = float_range[1]
        self.float_speed = float_speed
        self.float_wait = 5
        self.float_up = False

        super().__init__(scene, location, image_path, size=size)

    def draw(self):

        # First float the object up or down
        y_location = self.location[1]
        if y_location >= self.max_y:
            self.float_up = True
        elif y_location <= self.min_y:
            self.float_up = False

        if self.float_up and self.float_wait <= 0:
            self.move(0, -1)
            self.float_wait = 5
        elif not self.float_up and self.float_wait <= 0:
            self.move(0, 1)
            self.float_wait = 5
        else:
            self.float_wait -= self.float_speed

        # Now draw the object
        super().draw()
