import pygame
import random

from pygame import Surface
from pygame.font import Font

from game.constants import Paths, Colors
from game.objects.graphical import GraphicalObject


class Explosion(GraphicalObject):
    """
    An explosion!

    Blits both graphics and text, and plays a sound effect.
    """

    def __init__(self, location, font_path, word):

        explosion_sets = (
            ("explosion-blue.png", Colors.orange),
            ("explosion-orange.png", Colors.blue),
            ("explosion-yellow.png", Colors.red),
            ("explosion-red.png", Colors.yellow)
        )

        filename, color = random.choice(explosion_sets)
        explosion_image: Surface = pygame.image.load(str(Paths.effects / filename))
        explosion_font: Font = Font(str(font_path), 50)
        explosion_text: Surface = explosion_font.render(word, True, color)

        # Turn around after x frames
        surface = Surface((200, 200))
        surface.fill(Colors.black)
        surface.set_colorkey(Colors.black)
        surface.blits(
            (
                (explosion_image, (0, 0)),
                (explosion_text, (0, 0))
            )
        )

        super().__init__(location, surface)
