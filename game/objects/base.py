from typing import Tuple

import pygame
from pygame.surface import Surface

from game import screen


class BaseObject:
    """
    Basic representation of an object on the game screen.
    Contains size information, as well as the location
    and the surface object to draw.
    """

    def __init__(self, location: Tuple[int, int], surface: Surface):
        """
        Construct a new game object.

        :param location: The top-left coordinate of the object on the screen
        :param surface: A Surface object that can be blitted to the screen.
        """

        self.location = location
        self.surface = surface
        self.size = self.surface.get_size()

    def draw(self):
        """
        Draw the game object on the screen by copying its image onto the Surface.
        """

        screen_size = screen.get_size()

        off_screen = (
            self.location[0] > screen_size[0]
            or self.location[0] + self.size[0] < 0
            or self.location[1] > screen_size[1]
            or self.location[1] + self.size[1] < 0
        )

        if off_screen:
            # No point in drawing it if it isn't visible
            return

        screen.blit(self.surface, self.location)

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

    def mouseover(self) -> bool:
        """
        Returns True if the mouse is currently hovering
        above the location of this object.
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_location, y_location = self.location
        width, height = self.size

        intersection = (
            x_location < mouse_x < (x_location + width)
            and y_location < mouse_y < (y_location + height)
        )
        if intersection:
            return True
        return False
