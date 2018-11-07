import sys

import pygame

from game.constants import Paths
from game.objects import TextObject, ImageObject
from game.scenes.base.scene import Scene


class HighScore(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """

    name = "high_score"

    def __init__(self, manager):

        super().__init__(manager)

        # Background image
        self.background = ImageObject(
            (0, 0),
            Paths.ui / "background.png",
        )

        # High score overlay
        self.high_scores = ImageObject(
            (0, 0),
            Paths.ui / "high_scores.png"
        )

        # Get the scores

        # Render them!
        self.start_game_text = TextObject(
            (90, 400),
            "Start game",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        # Music
        self.manager.play_music("code_jam_full.ogg")

    def handle_events(self, event):
        pass

    def draw(self):
        # Draw the background and the logo
        self.background.draw()
        self.high_scores.draw()
