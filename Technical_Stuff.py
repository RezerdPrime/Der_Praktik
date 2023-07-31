import pygame as pg
import configparser
from random import randint
from math import *
from clipboard import paste
from os import system


# WINDOW INIT ==========================================================================================================

pg.init()
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

WINDOW_TITLE = list(map(lambda x: x.strip(),
                    config['Splashes']['splshs'].split(";")))
#theme = bool(int(config['Screen']['is_dark']))
SPLASHES = WINDOW_TITLE[randint(0, len(WINDOW_TITLE) - 1)]
pg.display.set_caption(SPLASHES)
font40 = pg.font.Font("fnt.otf", 40)
font28 = pg.font.Font("fnt.otf", 28)
font20 = pg.font.Font(None, 20)

WIDTH = int(config['Screen']['width'])
HEIGHT = int(config['Screen']['heigth'])
WINDOW_SIZE = (WIDTH, HEIGHT)
player_count = int(ceil((WIDTH * HEIGHT / (WIDTH + HEIGHT)) ** 0.3))


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


# CLASSES ==============================================================================================================

class Circle:
    def __init__(self, color, pos, radius):
        self.color = color
        self.pos = pos
        self.radius = radius

    def draw(self, x, y, sc = screen):
        pg.draw.circle(sc, self.color, (self.pos[0] + x, self.pos[1] + y), self.radius)


class Map:
    def __init__(self):
        self.obj_list = []

    def add(self, *objs):
        self.obj_list.extend(objs)

    def __getitem__(self, item):
        return self.obj_list[item]

    def __iter__(self):
        return iter(self.obj_list)

    def generate(self):
        for i in range(HEIGHT * WIDTH // 1000): #'''HEIGHT * WIDTH // 500'''
            self.add( Circle(
                (randint(150,255), randint(150,255),randint(150,255)),
            (dx + randint(-2 * WIDTH, WIDTH), dy + randint(-2 * HEIGHT, HEIGHT)), randint(10,50)))

    def draw_all(self, x, y, sc = screen):
        for i in range(len(self.obj_list)):
            self.obj_list[i].draw(x, y)


class Player:

    def __init__(self, pos, team : pg.Color):
        self.pos = pos
        self.team = team

    def draw(self, x, y):
        pg.draw.circle(screen, self.team, (self.pos[0] + x, self.pos[1] + y), 20)

    '''def attack(self, x, y, func):
        val = 0; cur = 0
        buff = eval(func.replace("x",str(val / 20)))

        for _ in range(100):
            val += 1
            cur = 20 * eval(func.replace("x",str(val / 20)))
            print(cur)
            pg.draw.line(screen, BLACK, (val - 1, buff), (val, cur), 3)
            buff = cur
            screen.blit(screen, (0, 0))'''




class Team:

    def __init__(self, col : pg.Color):
        self.player_list = []
        self.col = col

    def add(self, *objs):
        self.player_list.extend(objs)

    def __getitem__(self, item):
        return self.player_list[item]

    def __iter__(self):
        return iter(self.player_list)

    def generate(self, mappy: Map):
        pc_buff = player_count
        newsc = pg.display.set_mode(WINDOW_SIZE)
        #Map.draw_all()

        while pc_buff:
            gen_pos = (dx + randint(-2 * WIDTH, WIDTH), dy + randint(-2 * HEIGHT, HEIGHT))
            newsc.fill(WHITE)
            mappy.draw_all(dx - gen_pos[0], dy - gen_pos[1], newsc)

            flag_lst = [ WHITE == newsc.get_at(
                (dx + int(ceil(20 * cos(pi * k / 4))), dy + int(ceil(20 * sin(pi * k / 4))))
            ) for k in range(8)] + [WHITE == newsc.get_at((dx, dy))]

            if all(flag_lst):
                self.add(Player(gen_pos, self.col))
                mappy.add(Player(gen_pos, self.col))
                pc_buff -= 1

    def draw_all(self, x, y):
        for i in range(len(self.player_list)):
            self.player_list[i].draw(x, y)


# MENU =================================================================================================================

PLAY_color = (0, 0, 0)
EDITOR_color = (0, 0, 0)
SETTINGS_color = (0, 0, 0)
pos_flag = -1 # показатель положения кнопки в меню


# SETTINGS =============================================================================================================

resolutions = [(640, 480), (800, 600), (960, 720),
               (1152, 648), (1280, 720), (1540, 790)]
current = resolutions.index(WINDOW_SIZE)
at_button = 0
REZOL_color = (0, 0, 0)
BACK_color = (0, 0, 0)


# GAME =================================================================================================================

overlay2 = pg.Surface((WIDTH, HEIGHT))
overlay2.set_alpha(0) # просто frontend
choose = True # выбор между загрузкой своей карты и рандомно сгенерированной
NO_color = (0,0,0); YES_color = (255,255,255)
YorN = 0 # флаг показывающий выбор игрока (чётен - No; нечётен - Yes)

dx = WIDTH // 2; dy = HEIGHT // 2 # Смещение координат (разница между текущим и предыдущим положениями мыши)
prevmp = mouse_pos # предыдущее положение мыши
Mappy = Map()
already_generated = False # чтобы бесконечно не генерило карту
mouse_mode = 1 # применяется для скроллинга карты

Teams = [Team(RED), Team(BLUE)]
step = randint(0, 1)
helpMap = Map()
func = ""
func_font = pg.font.Font("fnt.otf", 30)


# HELPING FUNCTIONS ====================================================================================================

def transitional_animation():
    for _ in range(1000):
        # print(i)
        screen.blit(overlay, (0, 0))
        overlay.set_alpha(1)
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


def load_data():
    system('explorer /select,"C:\\"')

    while True:
        file_path = ""
        try:
            while ".txt" != file_path[-5:][:-1] or file_path.count(".txt") != 1:
                file_path = paste()

            info = open(file_path.strip('"'), "r", encoding='utf-8').read()
            map_data = []

            exec("map_data += " + info)
            return map_data

        except SyntaxError: continue

def convert_data(data : list):
    for tupl in data:
        if len(tupl) == 6 and tupl[-1] * prod(tupl[i] for i in range(3)) >= 0:
            Mappy.add(Circle((tupl[:3]), (tupl[3:-1]), tupl[-1]))

def draw_map(x, y, func):
    screen.fill(WHITE)
    Mappy.draw_all(x, y)
    Teams[0].draw_all(x, y)
    Teams[1].draw_all(x, y)
    text_surface = func_font.render(func, True, (0, 0, 0))
    screen.blit(text_surface, (18, HEIGHT - 48))
    pg.display.flip()


'''def to_theme(*args, theme='light'):
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
            return 360 - args[0], 100 - args[1], 100 - args[2], args[3]'''
