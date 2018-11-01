from pathlib import Path
from typing import Tuple, Union

import pygame
from pygame.surface import Surface

from game.objects.graphical import GraphicalObject


class ImageObject(GraphicalObject):
    """
    Basic representation of a sprite on the game screen.
    Constructs a BaseObject with an image
    """

    def __init__(self, location: Tuple[int, int], image_path: Union[Path, str], *, size: Tuple[int, int] = None):
        """
        Construct a new game object.

        :param location: The top-left coordinate of the object on the screen
        :param image: The path to the image that will be displayed on the screen, or a Surface object
        :param size: Optionally, the size of the object - if provided, will transform the image instead of
                     assuming the size of the image is correct
        """

        image: Surface = pygame.image.load(str(image_path))

        if size and size != image.get_size():
            self.image = pygame.transform.smoothscale(self.image, size)

        super().__init__(location, image)
