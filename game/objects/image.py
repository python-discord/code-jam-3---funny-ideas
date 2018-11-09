from pathlib import Path
from typing import Tuple, Union

import pygame
from pygame.surface import Surface

from game import Colors
from game.objects.graphical import GraphicalObject


class ImageObject(GraphicalObject):
    """
    Basic representation of a sprite on the game screen.
    Constructs a BaseObject with an image
    """

    def __init__(self, scene, location: Tuple[int, int], image_path: Union[Path, str], *, size: Tuple[int, int] = None):
        """
        Construct a new game object.

        :param location: The top-left coordinate of the object on the screen
        :param image: The path to the image that will be displayed on the screen, or a Surface object
        :param size: Optionally, the size of the object - if provided, will transform the image instead of
                     assuming the size of the image is correct
        """

        self.image_path = image_path
        self.image: Surface = pygame.image.load(str(image_path))

        self.size = size
        if size and size != self.image.get_size():
            self.image = pygame.transform.smoothscale(self.image, size)

        self.highlight_color = Colors.yellow
        self.highlighted = False

        super().__init__(scene, location, self.image)

    def highlight(self):
        """
        Changes the blit color,
        in order to "highlight" the element
        for example during mouseover.
        """

        if not self.highlighted:

            self.surface = self.surface.copy()
            self.surface.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            self.surface.fill(Colors.orange + (0,), None, pygame.BLEND_RGBA_ADD)
            self.highlighted = True

    def remove_highlight(self):
        """
        Changes the font color back,
        in order to remove the highlight.
        """

        if self.highlighted:
            self.image = pygame.image.load(str(self.image_path))
            self.surface = pygame.transform.smoothscale(self.image, self.size)
            self.highlighted = False
