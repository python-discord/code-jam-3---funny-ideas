import random

import pygame

from game.constants import Paths
from game.objects import ImageObject, TextShootObject
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.missiles = []
        self.texts = []
        self.new_missile_timer = 0

        # Background image
        self.background = ImageObject(
            (0, 0),
            Paths.levels / "level_bg.png",
        )

        # Music
        pygame.mixer.music.load(str(Paths.music / "pskov_loop.ogg"))
        pygame.mixer.music.play(-1)

    def handle_events(self, event):
        pass

    def draw(self):
        self.background.draw()

        if self.new_missile_timer == 0:
            new_missile = ImageObject(
                (980, 260),
                Paths.items / "kickmissile.png",
            )

            self.missiles.append(new_missile)
            self.texts.append(
                TextShootObject((0, 0), new_missile)
            )

            self.new_missile_timer = 1500
        else:
            self.new_missile_timer -= 1

        for missile in self.missiles:
            y_direction = random.choice([-1, 1])
            missile.move(0.1 * y_direction, 0.1)

        for text in self.texts:
            text.draw()
