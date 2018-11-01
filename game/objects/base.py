from typing import Tuple, Union

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

        # If the user has moved less than 1 pixel, we store the amount here
        self.subpixel_horizontal = 0.0
        self.subpixel_vertical = 0.0

    def _subpixel_move(self, move, subpixel_count):
        """
        Handles subpixel movement speeds for a specific direction.
        """

        if isinstance(move, float):
            num, decimals = str(move).split(".")
            _move = int(num)

            if move >= 0:
                subpixel_count += float(f"0.{decimals}")
            else:
                subpixel_count -= float(f"-0.{decimals}")

            if subpixel_count > 1.0:
                subpixel_count -= 1.0

                if move > 0:
                    _move += 1
                elif move < 0:
                    _move -= 1

            move = _move

        return move, subpixel_count

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

    def move(self, horizontal: Union[int, float] = 0, vertical: Union[int, float] = 0):
        """
        Move the object, relative to its current position. You can use either a positive or negative value for
        either parameter.

        :param horizontal: The distance to move the object on the horizontal axis.
        :param vertical: The distance to move the object on the vertical axis.
        """

        # If the move is less than a pixel, we need special handling.
        horizontal, self.subpixel_horizontal = self._subpixel_move(horizontal, self.subpixel_horizontal)
        vertical, self.subpixel_vertical = self._subpixel_move(vertical, self.subpixel_vertical)

        # Now we can actually move.
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
