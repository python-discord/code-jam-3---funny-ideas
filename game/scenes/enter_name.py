import pygame

from game.constants import Paths, Window, Colors
from game.objects import ImageObject, TextObject, TextInputObject
from game.scenes.base.scene import Scene


class EnterName(Scene):
    """
    The screen that appears after the intro sequences,
    asking the player to enter their name so we can use
    it for high scores.
    """

    name = "enter_name"

    def __init__(self, manager):

        super().__init__(manager)

        # Background image
        self.background = ImageObject(
            self,
            (0, 0),
            Paths.ui / "background.png",
        )

        # Box overlay
        self.enter_name_box = ImageObject(
            self,
            (0, 0),
            Paths.ui / "enter_name_box.png"
        )
        self.enter_name_box.move_absolute((
            (Window.width / 2) - (self.enter_name_box.size[0] / 2),
            (Window.height / 2) - (self.enter_name_box.size[1] / 2)
        ))

        # Instructions
        self.please_enter_name = TextObject(
            self,
            (0, 0),
            "Who are you?",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=50
        )
        self.please_enter_name.move_absolute((
            (Window.width / 2) - (self.please_enter_name.size[0] / 2),
            200
        ))

        # InputBox
        self.input_field = TextInputObject(
            self,
            (450, 315),
            font_path=Paths.fonts / "FiraMono-Regular.ttf",
            font_size=40,
            max_length=15,
            text_color=Colors.white,
            cursor_color=Colors.white,
        )

        # Explanation text below input
        self.explanation_line_1 = TextObject(
            self,
            (0, 0),
            "We need this information for high scores.",
            font_path=Paths.fonts / "FiraMono-Regular.ttf",
            font_size=20
        )
        self.explanation_line_1.move_absolute((
            (Window.width / 2) - (self.explanation_line_1.size[0] / 2),
            400
        ))
        self.explanation_line_2 = TextObject(
            self,
            (0, 0),
            "Feel free to input a nickname, or a made-up name.",
            font_path=Paths.fonts / "FiraMono-Regular.ttf",
            font_size=20
        )
        self.explanation_line_2.move_absolute((
            (Window.width / 2) - (self.explanation_line_2.size[0] / 2),
            440
        ))

        # OK Button
        self.ok_button = TextObject(
            self,
            (880, 530),
            "OK",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=50,
            disabled=True
        )

        # Music
        self.manager.play_music("code_jam_loop.ogg", loop=True)

    def handle_events(self, events):
        return_event = self.input_field.update(events)

        # Check whether to enable the button
        if len(self.input_field.get_text()) >= 1 and self.ok_button.disabled:
            self.ok_button.enable()
        elif len(self.input_field.get_text()) < 1 and not self.ok_button.disabled:
            self.ok_button.disable()

        # Handle the OK button
        if not self.ok_button.disabled:

            # User hit RETURN and has typed something
            if return_event:
                self.manager.player_name = self.input_field.get_text()
                self.manager.change_scene("main_menu")

            # Handle mouse interaction with OK button
            if self.ok_button.mouseover():
                if not self.ok_button.highlighted:
                    self.ok_button.highlight()

                if pygame.mouse.get_pressed()[0]:
                    self.manager.player_name = self.input_field.get_text()
                    self.manager.change_scene("main_menu")

            # No mouseover event
            else:
                if self.ok_button.highlighted:
                    self.ok_button.remove_highlight()

    def draw(self):
        self.background.draw()
        self.enter_name_box.draw()
        self.please_enter_name.draw()
        self.explanation_line_1.draw()
        self.explanation_line_2.draw()
        self.ok_button.draw()
        self.input_field.draw()
