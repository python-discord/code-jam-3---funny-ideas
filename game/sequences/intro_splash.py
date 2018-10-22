from pathlib import Path

import pygame

from game import screen
from game.sequences import Sequence


class IntroSplashSequence(Sequence):
    def __init__(self):
        self.screen = screen

        logo_path = Path("game", "assets", "logo.png")
        self.logo = pygame.image.load(str(logo_path))
        self.logo = pygame.transform.scale(self.logo, (762, 266))

    def run(self):
        self.fade_in_image(5, self.logo)
        pygame.time.delay(1000)
        self.fade_out_image(5, self.logo)



