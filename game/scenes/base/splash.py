import pygame

from game.constants import Colors, Window
from game.scenes.base.scene import Scene


class Splash(Scene):
    """
    The screen that appears after the intro sequences.

    The game logo is displayed at the top.
    The user must press a button to start the game.
    """
    def __init__(self, manager):

        super().__init__(manager)
        self.alpha = 255
        self.fade_in = False

        # Number of frames to wait before fading out
        self.fade_out_time = 100

        # These need to be overwritten by all children
        self.image = None
        self.next_scene = None

        # Fade surface
        self.fade = pygame.Surface((Window.width, Window.height))
        self.fade.fill(Colors.black)

    def handle_events(self, events):
        """
        Allow the user to skip the
        splash screen by pressing
        ESC, space or enter.
        """
        for event in events:
            skip = (
                event.type == pygame.KEYDOWN
                and event.key in (
                    pygame.K_ESCAPE,
                    pygame.K_SPACE,
                    pygame.K_RETURN,
                )
            )

            if skip:
                self.manager.change_scene(self.next_scene)

    def draw(self):
        """
        Draw a single frame of the
        splash screen animation,
        gradually fading in and out the image.
        """

        self.screen.fill(Colors.black)
        self.fade.set_alpha(self.alpha)

        self.image.draw()
        self.screen.blit(self.fade, (0, 0))

        # Fade in or out
        if self.fade_in:
            self.alpha += 1
        else:
            self.alpha -= 1

        # Wait before fading out again.
        if self.alpha == -(self.fade_out_time / 2):
            self.fade_in = True

        if self.alpha == 300:
            self.manager.change_scene(self.next_scene)
