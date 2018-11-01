from pathlib import Path
from typing import NamedTuple


class Colors(NamedTuple):
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


class Window(NamedTuple):
    width = 1280
    height = 800
    depth = 32
    title = "Code Jam III: Funny Ideas"


class Paths(NamedTuple):
    """
    Path objects that define the various
    paths we need to interact with for this
    project.
    """
    assets = Path("game", "assets")

    # assets subfolders
    music = assets / "music"
    sfx = assets / "sfx"
    graphics = assets / "graphics"
    fonts = assets / "fonts"

    # Graphics subfolders
    avatars = graphics / "avatars"
    effects = graphics / "effects"
    enemies = graphics / "enemies"
    headless = graphics / "headless"
    items = graphics / "items"
    levels = graphics / "levels"
    main_menu = graphics / "main_menu"
    splash = graphics / "splash"
