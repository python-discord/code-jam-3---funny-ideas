import sys

import pygame

from game import screen
from game.constants import Colors, Window


class Sequence:
    """
    The base class for a sequence.

    A sequence is a non-interactive,
    skippable sequence of events, such
    as the intro splash, and the credits
    sequence.
    """

    def __init__(self):
        self.screen = screen

    @staticmethod
    def _skip_fade(event):
        """Returns True if the user wants the skip the sequence"""
        return (
            event.type == pygame.KEYDOWN
            and event.key in (
                pygame.K_ESCAPE,
                pygame.K_SPACE,
                pygame.K_RETURN
            )
        )

    def _fade_image(self, speed, image, reverse):
        """
        Fades in or out with an image in the center of the screen.
        """

        if self.skip and reverse:
            self.skip = False
            return

        fade = pygame.Surface((Window.width, Window.height))
        fade.fill(Colors.black)

        # Center the image
        image_width = image.get_rect().width
        image_height = image.get_rect().height

        center = (
            (Window.width / 2) - (image_width / 2),
            (Window.height / 2) - (image_height / 2),
        )

        # Fade in or out?
        alpha_values = reversed(range(0, 255)) if reverse else range(0, 255)

        for alpha in alpha_values:
            # Check for skip and quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self._skip_fade(event):
                    return False  # This is used to signal that the user wants to skip

            fade.set_alpha(alpha)

            # Draw the window
            self.screen.blit(image, center)
            self.screen.blit(fade, (0, 0))

            pygame.display.update()
            pygame.time.delay(speed)

    def fade_in_image(self, speed, image):
        """Fades a centered image in."""
        return self._fade_image(speed, image, reverse=True)

    def fade_out_image(self, speed, image):
        """Fades a centered image out."""
        return self._fade_image(speed, image, reverse=False)
