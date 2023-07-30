import pygame as pg
import configparser
from random import randint
from math import *


# WINDOW INIT ==========================================================================================================

pg.init()
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

WINDOW_TITLE = map(lambda x: x.strip(), config['Splashes']['splshs'].split(";")); WINDOW_TITLE = list(WINDOW_TITLE)
SPLASHES = WINDOW_TITLE[randint(0, len(WINDOW_TITLE) - 1)]
pg.display.set_caption(SPLASHES)
font = pg.font.Font("fnt.otf", 40)

WIDTH = int(config['Screen']['width'])
HEIGHT = int(config['Screen']['heigth'])
WINDOW_SIZE = (WIDTH, HEIGHT)

# SOME COLORS ==========================================================================================================

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


# VARIABLES FOR MODES MANAGING =========================================================================================

screen = pg.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)
overlay = pg.Surface((WIDTH, HEIGHT))
overlay.set_alpha(0)

mode = "menu" # menu game editor settings
running = True
mouse_pos = (0, 0)


# MENU =================================================================================================================

PLAY_color = (0, 0, 0)
EDITOR_color = (0, 0, 0)
SETTINGS_color = (0, 0, 0)
pos_flag = -1


# SETTINGS =============================================================================================================

resolutions = [(640, 480), (960, 720), (1152, 864), (1600, 900), (1600, 1024), (1920, 1080)]
current = 1
at_button = 1
REZOL_color = (0, 0, 0)


# GAME =================================================================================================================




# HELPING FUNCTIONS ====================================================================================================
def transitional_animation():
    for _ in range(1000):
        # print(i)
        screen.blit(overlay, (0, 0))
        overlay.set_alpha(1)
        screen.blit(screen, (0, 0))
        pg.display.flip()