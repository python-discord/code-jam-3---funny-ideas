from operator import itemgetter

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

        # Score attributes
        self.high_score_y = 120
        self.high_score_texts = []

        # Get the scores
        r = requests.get(URLs.scores_api)
        high_scorers = r.json()

        # Sort by score and limit to 10
        high_scorers = [
            {
                "username": name,
                "wpm": data['wpm'],
                "accuracy": data['accuracy'],
                "score": data['score']
            } for name, data in high_scorers.items()
        ]
        high_scorers = sorted(high_scorers, key=itemgetter('score'))[:10]

        # Build the score text objects
        for score in high_scorers:
            name = score['username']
            accuracy = score['accuracy']
            wpm = score['wpm']

            self.high_score_texts.append(
                TextObject(
                    (250, self.high_score_y),
                    f"{name}: wpm: {wpm}  accuracy: {accuracy}%",
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                )
            )
            self.high_score_y += 80
            self.high_score_texts.append(
                TextObject(
                    (250, self.high_score_y),
                    f"{name}: wpm: {wpm}  accuracy: {accuracy}%",
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                )
            )
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

        for score in self.high_score_texts:
            score.draw()
