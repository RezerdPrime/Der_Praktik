import pygame as pg
import configparser
from random import randint
from math import *


# WINDOW INIT ==========================================================

pg.init()
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

WINDOW_TITLE = list(map(lambda x: x.strip(),
                    config['Splashes']['splshs'].split(";")))
SPLASHES = WINDOW_TITLE[randint(0, len(WINDOW_TITLE) - 1)]
pg.display.set_caption(SPLASHES)
font40 = pg.font.Font("fnt.otf", 40)
font28 = pg.font.Font("fnt.otf", 28)
font20 = pg.font.Font(None, 20)

WIDTH = int(config['Screen']['width'])
HEIGHT = int(config['Screen']['height'])
WINDOW_SIZE = (WIDTH, HEIGHT)

theme = bool(int(config['Screen']['is_dark']))

# SOME COLORS ==========================================================
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (125, 125, 125)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
ORANGE = (255, 123, 0)
YELLOW = (255, 225, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (225, 0, 255)


# VARIABLES FOR MODES MANAGING =========================================

screen = pg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)
overlay = pg.Surface((WIDTH, HEIGHT))
overlay.set_alpha(0)

mode = "menu"  # menu game editor settings
running = True
animation_was_played = False
mouse_pos = (0, 0)


# MENU =================================================================

PLAY_color = (0, 0, 0)
EDITOR_color = (0, 0, 0)
SETTINGS_color = (0, 0, 0)
pos_flag = -1


# SETTINGS =============================================================

resolutions = [(640, 480), (800, 600), (960, 720),
               (1152, 648), (1280, 720), (1540, 790)]
current = resolutions.index(WINDOW_SIZE)
at_button = 0
REZOL_color = (0, 0, 0)
BACK_color = (0, 0, 0)


# HELPING FUNCTIONS ====================================================
def transitional_animation():
    for _ in range(750):
        # print(i)
        screen.blit(overlay, (0, 0))
        overlay.set_alpha(1)
        # screen.blit(screen, (0, 0))
        pg.display.flip()


def menu_interface(PLAY_color, EDITOR_color, SETTINGS_color):
    butts = [((WIDTH - 185) // 2, (HEIGHT - 255) // 2,
              200, 80),
             ((WIDTH - 185) // 2, (HEIGHT - 55) // 2,
              200, 80),
             ((WIDTH - 185) // 2, (HEIGHT + 145) // 2,
              200, 80),
             ((WIDTH - 200) // 2, (HEIGHT - 270) // 2,
              200, 80),
             ((WIDTH - 200) // 2, (HEIGHT - 70) // 2,
              200, 80),
             ((WIDTH - 200) // 2, (HEIGHT + 130) // 2,
              200, 80)]

    pg.draw.rect(screen, GRAY, butts[0])
    pg.draw.rect(screen, GRAY, butts[1])
    pg.draw.rect(screen, GRAY, butts[2])
    
    pg.draw.rect(screen, LIGHT_GRAY, butts[3])
    pg.draw.rect(screen, LIGHT_GRAY, butts[4])
    pg.draw.rect(screen, LIGHT_GRAY, butts[5])
    
    text1 = font40.render("PLAY", True, PLAY_color)
    screen.blit(text1, ((WIDTH - text1.get_width()) // 2,
                        (HEIGHT - 240) // 2))
    text1 = font40.render("EDITOR", True, EDITOR_color)
    screen.blit(text1, ((WIDTH - text1.get_width()) // 2,
                        (HEIGHT - 40) // 2))
    text1 = font40.render("SETTINGS", True, SETTINGS_color)
    screen.blit(text1, ((WIDTH - text1.get_width()) // 2,
                        (HEIGHT + 160) // 2))
    screen.blit(screen, (0, 0))


def to_theme(*args, theme='light'):
    assert 1 < len(args) < 5
    if theme == 'dark':
        if isinstance(args[0], pg.Color):
            return 255 - args[0].r, 255 - args[0].g, 255 - args[0].b
        
        if len(args) == 1:
            if len(args[0]) == 3:
                return tuple(255 - c for c in args[0])
            elif len(args[0]) == 4:
                return (360 - args[0][0], 100 - args[0][1],
                        100 - args[0][2], args[0][3])
            
        elif len(args) == 3:
            return tuple(255 - c for c in args)
        else:
            return 360 - args[0], 100 - args[1], 100 - args[2], args[3]
