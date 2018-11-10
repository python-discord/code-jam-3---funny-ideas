from operator import itemgetter

import pygame
import requests

from game.constants import Paths, URLs, Window
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
            self,
            (0, 0),
            Paths.ui / "background.png",
        )

        # High score overlay
        self.high_scores = ImageObject(
            self,
            (0, 0),
            Paths.ui / "high_scores.png"
        )

        # High scores headline
        self.headline_text = TextObject(
            self,
            (0, 0),
            "High scores",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=50
        )
        self.headline_text.move_absolute((
            (Window.width / 2) - (self.headline_text.size[0] / 2),
            75
        ))

        # The icons that explain what each row is for
        self.score_headline = TextObject(
            self,
            (600, 200),
            "Score"
        )
        self.wpm_headline = TextObject(
            self,
            (850, 200),
            "WPM"
        )
        self.accuracy_headline = TextObject(
            self,
            (1000, 200),
            "Accuracy"
        )

        # Add the close button
        self.close_button = ImageObject(
            self,
            (1120, 90),
            Paths.ui / "close_window.png"
        )

        # Score attributes
        self.high_score_y = 270
        self.high_score_number = 1
        self.high_score_texts = []

        # Get the scores
        r = requests.get(URLs.scores_api)
        high_scorers = r.json()

        # Sort by score and limit to 5
        high_scorers = [
            {
                "username": name,
                "wpm": data['wpm'],
                "accuracy": data['accuracy'],
                "score": data['score']
            } for name, data in high_scorers.items()
        ]
        high_scorers = sorted(high_scorers, key=itemgetter('score'), reverse=True)[:5]

        # Build the score text objects
        for score in high_scorers:
            points = score['score']
            name = score['username']
            accuracy = score['accuracy']
            wpm = score['wpm']

            self.high_score_texts.append((
                TextObject(
                    self,
                    (180, self.high_score_y),
                    f"{self.high_score_number}.",
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                ),
                TextObject(
                    self,
                    (230, self.high_score_y),
                    name,
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                ),
                TextObject(
                    self,
                    (600, self.high_score_y),
                    str(points),
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                ),
                TextObject(
                    self,
                    (850, self.high_score_y),
                    str(wpm),
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                ),
                TextObject(
                    self,
                    (1000, self.high_score_y),
                    f"{accuracy}%",
                    font_path=Paths.fonts / "NANDA.TTF",
                    font_size=60
                ),
            ))
            self.high_score_y += 80
            self.high_score_number += 1

        self.start_game_text = TextObject(
            self,
            (90, 400),
            "Start game",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        # Music
        if self.manager.previous_scene and not self.manager.previous_scene.name == "main_menu":
            self.manager.play_music("code_jam_full.ogg")

    def handle_events(self, events):
        for event in events:

            # Escape goes back to the main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_scene("main_menu")

        if self.close_button.mouseover():
            if not self.close_button.highlighted:
                self.close_button.highlight()

            if pygame.mouse.get_pressed()[0]:
                self.manager.change_scene("main_menu")
        else:
            if self.close_button.highlighted:
                self.close_button.remove_highlight()

    def draw(self):
        # Draw the background and the logo
        self.background.draw()
        self.high_scores.draw()
        self.headline_text.draw()
        self.close_button.draw()

        # Draw the icons
        self.wpm_headline.draw()
        self.score_headline.draw()
        self.accuracy_headline.draw()

        for score in self.high_score_texts:
            for attribute in score:
                attribute.draw()
