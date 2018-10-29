from pathlib import Path

import pygame

from game import screen
from game.sequences.sequence import Sequence


class IntroSplashSequence(Sequence):
    def __init__(self):
        self.screen = screen
        self.skip = False

        # Logo
        logo_path = Path("game", "assets", "graphics", "logo.png")
        self.logo = pygame.image.load(str(logo_path))
        self.logo = pygame.transform.scale(self.logo, (762, 266))

    def run(self):
        skip = self.fade_in_image(5, self.logo)
        if skip is not False:
            pygame.time.delay(1000)
            self.fade_out_image(5, self.logo)
