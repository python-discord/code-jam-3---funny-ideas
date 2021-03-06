import sys

import pygame

from game.constants import Paths, Window
from game.objects import FloatingObject, ImageObject, TextObject
from game.scenes.base.scene import Scene


class MainMenu(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """

    name = "main_menu"

    def __init__(self, manager):

        super().__init__(manager)

        # Main game logo
        self.logo = ImageObject(
            self,
            (0, 0),
            Paths.ui / "logo.png",
        )

        # Move the logo to the right position, based on screen size.
        image_width = self.logo.size[0]
        logo_location = (
            (Window.width / 2) - (image_width / 2),
            40,
        )
        self.logo.move_absolute(logo_location)

        # How to play
        self.how_to_play_open = False
        self.how_to_play = ImageObject(
            self,
            (0, 0),
            Paths.ui / "how_to_play.png"
        )
        self.close_how_to_play = ImageObject(
            self,
            (1060, 300),
            Paths.ui / "close_window.png"
        )

        # Background image
        self.background = ImageObject(
            self,
            (0, 0),
            Paths.ui / "background.png",
        )

        # Floaty dudes
        self.flutterdude = FloatingObject(
            self,
            (980, 260),
            Paths.enemies / "flutterdude.png",
            float_range=(260, 280),
            float_speed=4,
        )

        self.brainmon = FloatingObject(
            self,
            (900, 400),
            Paths.enemies / "brainmon_firing.png",
            float_range=(390, 400),
            float_speed=3,
        )

        # Text init
        self.start_game_text = TextObject(
            self,
            (90, 400),
            "Start game",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        self.how_to_play_text = TextObject(
            self,
            (90, 480),
            "How to play",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        self.high_scores_text = TextObject(
            self,
            (90, 560),
            "High scores",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        self.quit_text = TextObject(
            self,
            (90, 640),
            "Quit game",
            font_path=Paths.fonts / "NANDA.TTF",
            font_size=60,
        )

        self.menu_items = {
            "start": self.start_game_text,
            "how_to_play": self.how_to_play_text,
            "high_scores": self.high_scores_text,
            "quit": self.quit_text,
            "close": self.close_how_to_play,
        }

        # SFX
        if self.manager.previous_scene.name == "jetbrains":
            self.sound = pygame.mixer.Sound(str(Paths.sfx / "megalomaniac.ogg"))
            self.sound.play()

        # Music
        self.manager.play_music("code_jam_loop.ogg", loop=True)

    def handle_events(self, events):

        for event in events:
            for name, item in self.menu_items.items():

                if event.type == pygame.KEYDOWN:
                    if self.how_to_play_open and event.key == pygame.K_ESCAPE:
                        self.how_to_play_open = False
                        break

                if item.mouseover():
                    if not item.highlighted:
                        item.highlight()

                        if not name == "close":
                            item.move(15, 0)

                    if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                        # Quit button
                        if name == "quit":
                            pygame.quit()
                            sys.exit()

                        # Start game
                        elif name == "start":
                            self.manager.change_scene("game")

                        elif name == "high_scores":
                            self.manager.change_scene("high_score")

                        # How to play
                        elif name == "how_to_play":
                            self.how_to_play_open = True

                        # Close "How to play" menu
                        elif name == "close":
                            self.how_to_play_open = False
                else:
                    if item.highlighted:
                        item.remove_highlight()

                        if not name == "close":
                            item.move(-15, 0)

    def draw(self):
        # Draw the background and the logo
        self.background.draw()
        self.logo.draw()

        if not self.how_to_play_open:
            # Draw the floaty entities
            self.brainmon.draw()
            self.flutterdude.draw()

            # Draw the menu
            self.start_game_text.draw()
            self.how_to_play_text.draw()
            self.high_scores_text.draw()
            self.quit_text.draw()
        else:
            self.how_to_play.draw()
            self.close_how_to_play.draw()
