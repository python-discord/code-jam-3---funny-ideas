import random
from typing import List, Tuple

import pygame
import requests

from game.constants import Explosions, Paths, URLs, Window
from game.objects import Explosion, ImageObject, TextObject, TextShootObject, Timer
from game.objects.flutterdude import Flutterdude
from game.objects.npc import NPC
from game.objects.pyjet import PyJet
from game.objects.text_shoot import TextShootState
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.max_bombs = 8
        self.game_over_screen = None
        self.accuracy = None
        self.timer = None
        self.speed_multiplier = 3
        self.explosions: List[Explosion] = []
        self.texts: List[TextShootObject] = []
        self.new_missile_timer = 200
        self.new_jet_timer = random.randint(450, 1200)
        self.start_ticks = pygame.time.get_ticks()
        self.game_running = True
        self.sent_scores = False

        self.lock = None
        self.wpm = None
        self.letters_typed = 0
        self.letters_missed = 0
        self.pyjet = None

        self.restart_game_text = TextObject(
            self,
            (0, 0),
            "Play again",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=60
        )
        self.high_scores_text = TextObject(
            self,
            (0, 0),
            "High scores",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=60
        )
        self.restart_game_text.move_absolute((
            (Window.width / 2) - (self.restart_game_text.size[0] / 2),
            450
        ))
        self.high_scores_text.move_absolute((
            (Window.width / 2) - (self.high_scores_text.size[0] / 2),
            550
        ))
        self.wpm_text = None
        self.accuracy_text = None

        # Background image
        background_path = Paths.levels / random.choice(["level_bg.png", "level_bg_2.png"])

        self.background = ImageObject(
            self,
            (0, 0), background_path,
        )

        # SFX
        self.gunshot = pygame.mixer.Sound(str(Paths.sfx / "gunshot.ogg"))
        self.gunshot.set_volume(0.4)
        self.wrong = pygame.mixer.Sound(str(Paths.sfx / "wrong_letter.ogg"))
        self.you_lose_sfx = pygame.mixer.Sound(str(Paths.sfx / "you_lose.ogg"))
        self.you_win_sfx = pygame.mixer.Sound(str(Paths.sfx / "you_win.ogg"))

        # Some random NPCs
        number_of_npcs = 7

        npc_slots = [
            (123, 550),
            (211, 550),
            (284, 550),
            (450, 550),
            (570, 550),
            (800, 550),
            (990, 550),
        ]
        random.shuffle(npc_slots)
        self.npcs = []
        for _ in range(number_of_npcs):
            self.npcs.append(
                NPC(self, npc_slots.pop(-1))
            )

        # Enemies
        self.flutterdude = Flutterdude(
            self,
            (0, 75),
            1.5
        )

        # Play some music
        self.manager.play_music("pskov_loop.ogg", loop=True)

    def _build_game_over_screen(self):
        """
        Builds a screen that can be displayed
        when the game is over, showing WINNER
        or YOU LOSE graphics, score, a retry
        button and playing sfx.
        """

        # Calculate WPM
        total_letters = self.letters_typed + self.letters_missed
        self.wpm = int((total_letters / 5) / self.timer.minutes_passed)
        self.wpm_text = TextObject(
            self,
            (1045, 15),
            f"WPM: {self.wpm}",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=35
        )

        # Calculate accuracy
        total_letters = self.letters_typed + self.letters_missed

        if total_letters:
            self.accuracy = int(
                100 - ((self.letters_missed / total_letters) * 100)
            )
        else:
            self.accuracy = 0

        self.accuracy_text = TextObject(
            self,
            (938, 70),
            f"Accuracy: {self.accuracy}%",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=35
        )

        # Display the right images and play SFX
        if not self.npcs:
            self.game_over_screen = ImageObject(
                self,
                (0, 0),
                Paths.ui / "you_lose.png"
            )
            move_height = 220
            self.you_lose_sfx.play()
        else:
            self.game_over_screen = ImageObject(
                self,
                (0, 0),
                Paths.ui / "winner.png"
            )
            move_height = 100
            self.you_win_sfx.play()

        image_width = self.game_over_screen.size[0]
        center_x = (Window.width / 2) - (image_width / 2)
        self.game_over_screen.move_absolute((center_x, move_height))

        # Play game over music
        self.manager.play_music("code_jam_full.ogg")

    def _draw_timer(self):
        """
        Draws the timer that counts down from
        ten minutes in the top right corner
        """
        self.timer = Timer(
            self,
            (1080, 20),
            self.start_ticks,
            speed_multiplier=self.speed_multiplier,
            font_path=Paths.fonts / "ObelixPro-Cry-cyr.ttf"
        )
        self.timer.draw()

    def _draw_npcs(self):
        """
        Draws all the NPCs to
        the play area.
        """
        for npc in self.npcs:
            if npc.frames_until_turn <= 0:
                npc.flip()
                npc.frames_until_turn = random.randint(100, 3000)
            if npc.frames_until_walk <= 0:
                move = random.uniform(-3, 3)

                # Gotta make sure they don't walk off the screen
                if npc.location[0] > (Window.width - 300):
                    move = -abs(move)
                elif npc.location[0] < 300:
                    move = abs(move)

                npc.move(move, 0)
                npc.frames_until_walk = random.randint(10, 150)
            else:
                npc.frames_until_walk -= 1
                npc.frames_until_turn -= 1
            npc.draw()

    def _fly_pyjet(self):
        """
        Flies the pyjet across the screen!
        Also handles dropping bombs from it.
        """
        pyjet_x = self.pyjet.location[0]
        pyjet_width = self.pyjet.size[0]
        off_screen = (
            (pyjet_x + pyjet_width) <= 0
            and not self.pyjet.left_to_right
            or pyjet_x >= Window.width
            and self.pyjet.left_to_right
        )

        if off_screen:
            self.pyjet = None
        else:
            if not self.pyjet.bombs_dropped == len(self.pyjet.bomb_drop_locations):
                drop_bomb_left = (
                    (pyjet_x + (pyjet_width / 2)) >= self.pyjet.bomb_drop_locations[self.pyjet.bombs_dropped]
                    and self.pyjet.left_to_right
                )

                drop_bomb_right = (
                    (pyjet_x - (pyjet_width / 2)) <= self.pyjet.bomb_drop_locations[-(self.pyjet.bombs_dropped + 1)]
                    and not self.pyjet.left_to_right
                )

                if drop_bomb_left or drop_bomb_right:
                    new_missile = self.pyjet.create_bomb(random.uniform(0.6, 1.2))

                    self.texts.append(
                        TextShootObject(self, (0, 0), new_missile, short=True)
                    )

                    self.pyjet.bombs_dropped += 1

            self.pyjet.draw()

    def _draw_missiles(self, text):
        """
        Draws all the missiles that are
        currently in play, and explodes
        them and murders NPCs if they
        go too low.
        """

        text_x, text_y = text.location
        y_loc = text_y + text.surface.get_rect().bottomleft[1]

        if y_loc > Window.height:
            return
        elif y_loc >= 550:

            # Murder the NPC, if he's nearby.
            closest_npc = None
            for npc in self.npcs:
                if not closest_npc:
                    closest_npc = npc
                elif abs(npc.location[0] - text_x) < abs(closest_npc.location[0] - text_x):
                    closest_npc = npc

            if closest_npc and abs(closest_npc.location[0] - text_x) < 100:
                self.npcs.remove(closest_npc)

                # Explode the missile!
                self._add_explosion(
                    text.location,
                    random.choice(Explosions.ban_text),
                    size=250
                )
                self.texts.remove(text)

                # Remove it from lock if it was locked.
                if text == self.lock:
                    self.lock = None

        text.draw()

    def _add_explosion(self, location: Tuple[int, int], text: str, size: int = 175):
        """
        Adds an explosion with the provided text.

        Optionally takes a size argument to determine
        what size the graphics should scale to.
        """
        explosion = Explosion(
            self,
            location,
            Paths.fonts / "ObelixPro-Cry-cyr.ttf",
            text,
            size,
        )

        self.explosions.append(explosion)

    def _commit_score_to_api(self):
        """
        Commits the users score to the
        database via the Megalomaniac API.
        """
        if not self.sent_scores:
            requests.post(
                URLs.add_score_api,
                json={
                    "username": self.manager.player_name,
                    "wpm": self.wpm,
                    "accuracy": self.accuracy,
                }
            )
            self.sent_scores = True

    def handle_events(self, events):
        """
        Handles all game input events,
        such as mouse movement and keypresses.
        """

        for event in events:
            if not self.game_running:
                for button in (self.restart_game_text, self.high_scores_text):
                    if button.mouseover():
                        if not button.highlighted:
                            button.highlight()

                        if pygame.mouse.get_pressed()[0] and button.word == "High scores":
                            self.manager.change_scene("high_score")
                        elif pygame.mouse.get_pressed()[0] and button.word == "Play again":
                            self.manager.change_scene("game")

                    elif not self.game_running and not button.mouseover():
                        button.remove_highlight()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.change_scene("main_menu")
                elif event.key == pygame.K_F5:  # YOU LOSE
                    self.game_running = False
                    self.npcs = []

                    self._commit_score_to_api()
                elif event.key == pygame.K_F6:  # YOU WIN
                    self.game_running = False
                    self.npcs = ["something"]
                    self._build_game_over_screen()
                    self._commit_score_to_api()
                elif event.key == pygame.K_BACKSPACE and self.lock:
                    if self.lock.typed > 0:
                        self.lock.typed -= 1
                    else:
                        self.lock = None

                if not self.lock:
                    for text in self.texts:
                        result = text.key_input(event.key)

                        # If the user hit the right key, lock the word
                        if result == TextShootState.SUCCESS:
                            self.letters_typed += 1
                            self.gunshot.play()
                            self.lock = text

                            # Move the locked element to the end so it always renders on top of everything else.
                            self.texts.append(self.texts.pop(self.texts.index(self.lock)))

                            break
                        elif result == TextShootState.WORD_END:
                            self.letters_typed += 1
                            self.gunshot.play()
                            self.texts.remove(text)
                            self._add_explosion(
                                text.location,
                                random.choice(Explosions.destroy_text),
                                size=125
                            )
                            self.lock = None

                else:
                    result = self.lock.key_input(event.key)

                    if result == TextShootState.SUCCESS:
                        self.letters_typed += 1
                        self.gunshot.play()
                    elif result == TextShootState.WORD_END:
                        self.letters_typed += 1
                        self.gunshot.play()
                        self.texts.remove(self.lock)
                        self._add_explosion(
                            self.lock.location,
                            random.choice(Explosions.destroy_text),
                            size=125
                        )
                        self.lock = None
                    elif result == TextShootState.WRONG_KEY:
                        self.letters_missed += 1
                        self.wrong.play()

    def draw(self):
        """
        Draws everything to the screen.
        """
        self.background.draw()

        if self.game_running:
            self._draw_timer()
            self._draw_npcs()
            self.flutterdude.draw()

            # Create new flutterdude missiles periodically
            if (self.new_missile_timer == 0 and len(self.texts) < self.max_bombs) or not self.texts:
                new_missile = self.flutterdude.create_bomb(random.uniform(0.1, 0.4))

                self.texts.append(
                    TextShootObject(self, (0, 0), new_missile)
                )

                if self.new_missile_timer == 0:
                    self.new_missile_timer = 200
            else:
                self.new_missile_timer -= 1

            # Create jet periodically
            if self.new_jet_timer == 0:
                self.pyjet = PyJet(
                    self,
                    left_to_right=random.choice((True, False))
                )
                self.new_jet_timer = random.randint(450, 1200)
            else:
                self.new_jet_timer -= 1

            # Fly the jet! Rocket maaan!
            if self.pyjet:
                self._fly_pyjet()

            # Draw all the explosions
            for explosion in self.explosions.copy():
                explosion.draw()

                if explosion.frame_count >= explosion.frame_length:
                    self.explosions.remove(explosion)

            # Draw the missiles
            for text in self.texts:
                self._draw_missiles(text)

            # Check if we've lost yet
            if not self.npcs:
                self.game_running = False

            # Check if we've won (timer finished)
            if self.timer.milliseconds_left <= 0:
                self.game_running = False

        # Game is over, and we need to draw some UI.
        else:
            if not self.game_over_screen:
                self._build_game_over_screen()

            self.game_over_screen.draw()
            self._commit_score_to_api()
            self.restart_game_text.draw()
            self.high_scores_text.draw()
            self.wpm_text.draw()
            self.accuracy_text.draw()
