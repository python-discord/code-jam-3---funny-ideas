import pygame
import requests

from game.constants import Paths, URLs
from game.objects import ImageObject, TextObject
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
        r = requests.get(URLs.scores_api)
        print(r.json())

        # Render them!
        self.start_game_text = TextObject(
            (90, 400),
            "Start game",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        # Music
        if not self.manager.previous_scene.name == "main_menu":
            self.manager.play_music("code_jam_full.ogg")

    def handle_events(self, events):
        for event in events:

            # Escape goes back to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_scene("main_menu")

    def draw(self):
        # Draw the background and the logo
        self.background.draw()
        self.high_scores.draw()
