from pathlib import Path

import pygame

from game.constants import Window
from .scene import Scene


class MainMenu(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """
    def __init__(self):
        super().__init__()

        # Main game logo
        logo_path = Path("game", "assets", "graphics", "megalomaniac_logo.png")
        self.logo = pygame.image.load(str(logo_path))
        self.logo = pygame.transform.scale(self.logo, (762, 266))

    def draw(self):

        # Center the image
        image_width = self.logo.get_rect().width
        image_height = self.logo.get_rect().height

        # Draw the main game logo
        center = (
            (Window.width / 2) - (image_width / 2),
            (Window.height / 2) - (image_height / 2),
        )

        self.screen.blit(self.logo, center)
