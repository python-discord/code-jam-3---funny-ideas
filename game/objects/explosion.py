import random
from typing import Tuple

import pygame
from pygame import Surface
from pygame.font import Font

from game.constants import Colors, Paths
from game.objects.graphical import GraphicalObject


class Explosion(GraphicalObject):
    """
    An explosion!

    Blits both graphics and text, and plays a sound effect.
    """

    def __init__(self, location: Tuple[int, int], font_path, word, frame_length: int = 60):
        self.frame_length = frame_length
        self.frame_count = 0

        self.sound = pygame.mixer.Sound(str(Paths.sfx / "explosion.ogg"))
        self.sound.play()

        explosion_sets = (
            ("explosion-blue.png", Colors.orange),
            ("explosion-orange.png", Colors.blue),
            ("explosion-yellow.png", Colors.red),
            ("explosion-red.png", Colors.yellow)
        )

        filename, color = random.choice(explosion_sets)
        explosion_image: Surface = pygame.image.load(str(Paths.effects / filename))
        explosion_font_size: int = 26 - (len(word) - 5)
        explosion_font: Font = Font(str(font_path), explosion_font_size)
        explosion_text: Surface = explosion_font.render(word, True, color)

        explosion_image = pygame.transform.smoothscale(explosion_image, (175, 175))

        # Turn around after x frames
        surface = Surface((200, 200))
        surface.fill(Colors.black)
        surface.set_colorkey(Colors.black)
        surface.blits(
            (
                (explosion_image, (0, 0)),
                (
                    explosion_text,
                    (
                        (explosion_image.get_width() / 2) - explosion_text.get_width() / 2,
                        (explosion_image.get_height() / 2) - explosion_text.get_height() / 2
                    )
                )
            )
        )

        super().__init__(location, surface)

    def draw(self):
        if self.frame_count >= self.frame_length:
            return

        self.frame_count += 1
        super().draw()
