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
pos_flag = -1 # показатель положения кнопки в меню


# SETTINGS =============================================================================================================

resolutions = [(640, 480), (960, 720), (1152, 864), (1600, 900), (1600, 1024), (1920, 1080)]
current = 1 # позиция в resolutions
at_button = 1 # по сути тоже самое, что и pos_flag, только для настроек
REZOL_color = (0, 0, 0)


# GAME =================================================================================================================

overlay2 = pg.Surface((WIDTH, HEIGHT))
overlay2.set_alpha(0) # просто frontend
choose = True # выбор между загрузкой своей карты и рандомно сгенерированной
NO_color = (0,0,0); YES_color = (255,255,255)


# HELPING FUNCTIONS ====================================================================================================
def transitional_animation():
    for _ in range(1000):
        # print(i)
        screen.blit(overlay, (0, 0))
        overlay.set_alpha(1)
        screen.blit(screen, (0, 0))
        pg.display.flip()


def menu_interface(PLAY_color, EDITOR_color, SETTINGS_color):
    pg.draw.rect(screen, GRAY, ((WIDTH - 146) // 2, (HEIGHT - 250) // 2, 171, 70))
    pg.draw.rect(screen, GRAY, ((WIDTH - 146) // 2, (HEIGHT - 50) // 2, 171, 70))
    pg.draw.rect(screen, GRAY, ((WIDTH - 146) // 2, (HEIGHT + 150) // 2, 171, 70))

    pg.draw.rect(screen, LIGHT_GRAY, ((WIDTH - 174) // 2, (HEIGHT - 270) // 2, 174, 70))
    pg.draw.rect(screen, LIGHT_GRAY, ((WIDTH - 174) // 2, (HEIGHT - 70) // 2, 174, 70))
    pg.draw.rect(screen, LIGHT_GRAY, ((WIDTH - 174) // 2, (HEIGHT + 130) // 2, 174, 70))

    text1 = font.render("PLAY", True, PLAY_color)
    screen.blit(text1, (WIDTH // 2 - 34, HEIGHT // 2 - 110))
    text1 = font.render("EDITOR", True, EDITOR_color)
    screen.blit(text1, (WIDTH // 2 - 52, HEIGHT // 2 - 10))
    text1 = font.render("SETTINGS", True, SETTINGS_color)
    screen.blit(text1, (WIDTH // 2 - 68, HEIGHT // 2 + 90))
    screen.blit(screen, (0, 0))
