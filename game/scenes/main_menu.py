import sys
from pathlib import Path

import pygame

from game.constants import Window
from game.objects import FloatingObject, ImageObject, TextObject
from game.scenes.scene import Scene


class MainMenu(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """
    def __init__(self, manager):

        super().__init__(manager)
        menu_graphics = Path("game", "assets", "graphics", "main_menu")
        fonts = Path("game", "assets", "fonts")

        # Main game logo
        self.logo = ImageObject(
            (0, 0),
            menu_graphics / "logo.png",
        )

        # Move the logo to the right position, based on screen size.
        image_width = self.logo.size[0]
        logo_location = (
            (Window.width / 2) - (image_width / 2),
            40,
        )
        self.logo.move_absolute(logo_location)

        # Background image
        self.background = ImageObject(
            (0, 0),
            menu_graphics / "background.png",
        )

        # Floaty dudes
        self.flutterdude = FloatingObject(
            (980, 260),
            menu_graphics / "flutterdude.png",
            float_range=(260, 280),
            float_speed=4,
        )

        self.brainmon = FloatingObject(
            (900, 400),
            menu_graphics / "brainmon.png",
            float_range=(390, 400),
            float_speed=3,
        )

        # Text init
        self.start_game_text = TextObject(
            (90, 400),
            "Start game",
            font_path=fonts / "NANDA.TTF",
            font_size=60,
        )

        self.settings_text = TextObject(
            (90, 480),
            "Settings",
            font_path=fonts / "NANDA.TTF",
            font_size=60,
        )

        self.quit_text = TextObject(
            (90, 560),
            "Quit game",
            font_path=fonts / "NANDA.TTF",
            font_size=60,
        )

        self.menu_items = {
            "start": self.start_game_text,
            "settings": self.settings_text,
            "quit": self.quit_text,
        }

    def handle_events(self):
        for name, item in self.menu_items.items():
            if item.mouseover():
                if not item.highlighted:
                    item.highlight()
                    item.move(15, 0)

                if pygame.mouse.get_pressed()[0]:  # Left mouse button pressed
                    # Quit button
                    if name == "quit":
                        pygame.quit()
                        sys.exit()

                    # Start game
                    elif name == "start":
                        self.manager.change_scene("game")

                    # Settings
                    elif name == "settings":
                        pass
            else:
                if item.highlighted:
                    item.remove_highlight()
                    item.move(-15, 0)

    def draw(self):
        # Draw the background and the logo
        self.background.draw()
        self.logo.draw()

        # Draw the floaty entities
        self.brainmon.draw()
        self.flutterdude.draw()

        # Draw the menu
        self.start_game_text.draw()
        self.settings_text.draw()
        self.quit_text.draw()
