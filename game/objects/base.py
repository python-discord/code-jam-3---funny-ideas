from pathlib import Path
from typing import Tuple, Union

import pygame
from pygame.surface import Surface

from game import screen


class BaseObject:
    """
    Basic representation of an object on the game screen. Contains sizing information, as well as the location
    and image path.
    """

    def __init__(self, location: Tuple[int, int], image_path: Union[Path, str], *, size: Tuple[int, int] = None):
        """
        Construct a new game object.

        :param location: The top-left coordinate of the object on the screen
        :param image_path: The path to the image that will be displayed on the screen
        :param size: Optionally, the size of the object - if provided, will transform the image instead of
                     assuming the size of the image is correct
        """

        self.location = location
        self.image: Surface = pygame.image.load(str(image_path))
        self.size = self.image.get_size()

        if size and size != self.size:
            self.size = size
            pygame.transform.scale(self.image, size)

    def draw(self):
        """
        Draw the game object on the screen by copying its image onto the Surface.
        """

        screen_size = screen.get_size()

        off_screen = (
            self.location[0] > screen_size[0] or
            self.location[0] + self.size[0] < 0 or
            self.location[1] > screen_size[1] or
            self.location[1] + self.size[1] < 0
        )

        if off_screen:
            # No point in drawing it if it isn't visible
            return

        screen.blit(self.image, self.location)

    def move(self, horizontal: int = 0, vertical: int = 0):
        """
        Move the object, relative to its current position. You can use either a positive or negative value for
        either parameter.

        :param horizontal: The distance to move the object on the horizontal axis.
        :param vertical: The distance to move the object on the vertical axis.
        """

        self.location = (
            self.location[0] + horizontal,
            self.location[1] + vertical
        )

    def move_absolute(self, location: Tuple[int, int]):
        """
        Move the object to a specific set of coordinates.

        :param location: The coordinates to move the object to
        """

        self.location = location
