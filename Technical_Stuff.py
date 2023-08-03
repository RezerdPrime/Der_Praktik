import pygame as pg
import configparser
from random import randint
from math import *
import clipboard
from os import system
from datetime import datetime
from sys import exc_info


# WINDOW INIT ==========================================================================================================

pg.init()
config = configparser.ConfigParser()
config.read("config.cfg", encoding="utf-8")

WINDOW_TITLE = list(map(lambda x: x.strip(),
                    config['Splashes']['splshs'].split(";")))
#theme = bool(int(config['Settings']['is_dark']))
SPLASHES = WINDOW_TITLE[randint(0, len(WINDOW_TITLE) - 1)]
pg.display.set_caption(SPLASHES)
font48 = pg.font.Font("fnt.otf", 48)
font40 = pg.font.Font("fnt.otf", 40)
font28 = pg.font.Font("fnt.otf", 28)
font20 = pg.font.Font(None, 20)

WIDTH = int(config['Settings']['width'])
HEIGHT = int(config['Settings']['height'])
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

mode = "menu" # menu game editor settings endscreen
running = True
mouse_pos = (0, 0)

func_speed = 3
fs_list = [0.25, 0.5, 0.75, 1, 2, 4, 8]


# CLASSES ==============================================================================================================

class Circle:
    def __init__(self, color, pos, radius):
        self.color = color
        self.pos = pos
        self.radius = radius

    def draw(self, x, y, sc = screen):
        pg.draw.circle(sc, self.color, (self.pos[0] + x, self.pos[1] + y), self.radius)


class Line:
    def __init__(self, startpos, endpos):
        self.startpos = startpos
        self.endpos = endpos

    def draw(self, x, y):
        pg.draw.line(screen, BLACK,
                     (self.startpos[0] + x, self.startpos[1] + y),
                     (self.endpos[0] + x, self.endpos[1] + y), 3)


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
    def __init__(self, pos, team : pg.Color, indx):
        self.pos = pos
        self.team = team
        self.indx = indx
        self.direction = 0

    def draw(self, x, y):
        pg.draw.circle(screen, self.team, (self.pos[0] + x, self.pos[1] + y), 20)
        #num = font28.render(str(self.indx + 1), True, BLACK)
        #screen.blit(num, (self.pos[0] + x - 7, self.pos[1] + y - 19))

        if self.direction == 1:
            text = font40.render("<", True, BLACK)
            screen.blit(text, (self.pos[0] + x - 48, self.pos[1] + y - 28))
        elif self.direction == 2:
            text = font40.render(">", True, BLACK)
            screen.blit(text, (self.pos[0] + x + 28, self.pos[1] + y - 28))

    def attack(self, x, y, func, func_dir, fs = func_speed):
        self.direction = 0
        val = func_dir
        cur = 0
        dcur = 0
        indx = len(Mappy.obj_list)
        avaliable_colors[0] = self.team
        # buff = -eval(func.replace("x", str(val / 20)))
        buff = evaluated_value(func, val)

        #print(buff, lasterr)
        if isinstance(buff, str):
            while ((isinstance(buff, str) and
                    lasterr in ("Complex", "Value", "ZeroDiv"))
                   and abs(val) < 1.5 * WIDTH):
                val += func_dir
                buff = evaluated_value(func, val)

            buff = 0
            if abs(val) >= 1.5 * WIDTH):
                val = func_dir * 21

        if not isinstance(buff, str):
            dcur = buff
            buff = 0

        while is_not_collided() and \
                abs(val - x + WIDTH // 2) < WIDTH * 2 and \
                abs(cur - y + HEIGHT // 2) < HEIGHT * 2:

            pg.time.delay(round(4 / fs_list[fs]))
            val += func_dir
            cur = evaluated_value(func, val)
            if isinstance(cur, str):
                cur = buff
                break

            cur -= dcur
            #print(cur - buff)
            if abs(val) <= 5 and abs(buff - cur) > 1:
                continue

            Mappy.add(Line((val - func_dir - x + WIDTH // 2,
                            buff - y + HEIGHT // 2),
                           (val - x + WIDTH // 2,
                            cur - y + HEIGHT // 2)))
            draw_map(x - val, y - cur, func, 0, fs, self.team != RED, True)
            buff = cur

        Mappy.obj_list = Mappy.obj_list[:indx]
        detonated_pos = (val - x + WIDTH // 2,
                         cur - y + HEIGHT // 2)

        Teams[self.team != RED].kill_counts[self.indx] \
            += kill_players(detonated_pos)

        Mappy.add(Circle(WHITE, detonated_pos, 30))

        draw_map(x - val, y - cur, func, 0, fs, self.team != RED, True)
        pg.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), 30)
        screen.blit(screen, (0, 0))
        pg.display.flip()
        pg.time.delay(1500)


class Team(Map):
    def __init__(self, col : pg.Color):
        super().__init__()
        self.col = col
        self.kill_counts = [0 for _ in range(player_count)]

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
                self.add(Player(gen_pos, self.col, player_count - pc_buff))
                mappy.add(Player(gen_pos, self.col,  player_count - pc_buff))
                pc_buff -= 1


# MENU =================================================================================================================

PLAY_color = (0, 0, 0)
EDITOR_color = (0, 0, 0)
SETTINGS_color = (0, 0, 0)
pos_flag = -1 # показатель положения кнопки в меню


# SETTINGS =============================================================================================================

resolutions = [(640, 480), (800, 600), (960, 720),
               (1152, 648), (1280, 720), (1540, 790)]
fps_list = [0, 10, 15, 20, 30, 45, 60, 75, 90, 100, 120, 150, 200, 1000]

current = resolutions.index(WINDOW_SIZE)
at_button = 0
REZOL_color = (0, 0, 0)
BACK_color = (0, 0, 0)
FPS_color = (0, 0, 0)
FPS = fps_list.index(int(config['Settings']['fps']))

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
mouse_mode = False # применяется для скроллинга карты

Teams = [Team(RED), Team(BLUE)]
step = randint(0, 1)
helpMap = Map()
func = ""
func_font = pg.font.Font("fnt.otf", 30)
avaliable_colors = [Teams[step % 2].col, WHITE, BLACK]
func_dir = 1

xxx = ("max", "exp", "frexp", "ldexp")
fconvert = {"arcsin": "asin", "arccos": "acos", "arctg": "atan",
            "arcctg": "pi/2 - atan", "tg": "tan", "ctg": "1/tan",
            "^": "**", "ln(": "log(e, "}
you_god_damn_right = tuple(("abs ceil gcd lcm trunc log log2 "
                            "log10 pow sqrt sin cos gamma lgamma pi e "
                            "tau sum round for in range i j k t s u v "
                            "+ - ** * // / % , ( )").split())
lasterr = ""


# ENDSCREEN ============================================================================================================

ES_font = pg.font.Font("fnt.otf", 60)


# HELPING FUNCTIONS ====================================================================================================

def transitional_animation():
    for _ in range(1000):
        # print(i)
        screen.blit(overlay, (0, 0))
        overlay.set_alpha(1)
        pg.display.flip()


def menu_interface(PLAY_color, EDITOR_color, SETTINGS_color):
    butns = [((WIDTH - 185) // 2, (HEIGHT - 255) // 2,
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

    pg.draw.rect(screen, GRAY, butns[0])
    pg.draw.rect(screen, GRAY, butns[1])
    pg.draw.rect(screen, GRAY, butns[2])

    pg.draw.rect(screen, LIGHT_GRAY, butns[3])
    pg.draw.rect(screen, LIGHT_GRAY, butns[4])
    pg.draw.rect(screen, LIGHT_GRAY, butns[5])

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
            while ".gpht" != file_path[-6:-1] or file_path.count(".gpht") != 1:
                file_path = paste()

            info = open(file_path.strip('"'), "r", encoding='utf-8').read()
            map_data = []

            exec("map_data += " + info)
            return map_data

        except SyntaxError: continue


def convert_data(data : list):
    for tupl in data:
        if len(tupl) == 6 and all([tupl[-1] >= 0] + [tupl[i] >= 0 for i in range(3)]) >= 0:
            Mappy.add(Circle((tupl[:3]), (tupl[3:-1]), tupl[-1]))


def draw_map(x, y, func, speed_choice, fs=func_speed, step=step, flag = False):
    screen.fill(WHITE)
    Mappy.draw_all(x, y)
    Teams[0].draw_all(x, y)
    Teams[1].draw_all(x, y)

    text_surface = func_font.render('f(x) = ' + func, True, (0, 0, 0))
    screen.blit(text_surface, (50, HEIGHT - 68))
    pg.draw.rect(screen, BLACK, (30, HEIGHT - 80, WIDTH - 60, 60), 3)

    error = evaluated_value(func, 0)
    if func and isinstance(error, str):
        text_surface = font28.render(error, True, RED)
        screen.blit(text_surface, (WIDTH - 400, HEIGHT - 68))

    LEFTARROW = (BLACK,)
    RIGHTARROW = (BLACK,)
    if speed_choice == 1:
        LEFTARROW = (WHITE, LIGHT_BLUE)
    elif speed_choice == 2:
        RIGHTARROW = (WHITE, LIGHT_BLUE)

    text_surface = font28.render('Speed:', True, BLACK)
    screen.blit(text_surface, (WIDTH - 140, 20))
    text_surface = font28.render(' < ', True, *LEFTARROW)
    screen.blit(text_surface, (WIDTH - 170, 60))
    text_surface = font28.render(f'x{fs_list[fs]: <4}',
                                 True, BLACK)
    screen.blit(text_surface, (WIDTH - 130, 60))
    text_surface = font28.render(' > ', True, *RIGHTARROW)
    screen.blit(text_surface, (WIDTH - 50, 60))

    # Показатель ходящей команды
    text_surface = font48.render(("RED" if step % 2 == 0 else "BLUE")
                                 + " team's turn",
                                 True, Teams[step % 2].col)
    screen.blit(text_surface,
                (WIDTH // 2 - text_surface.get_width() // 2, 25))
    
    pg.draw.rect(screen, LIGHT_GRAY,
                 (30, HEIGHT - 118, 4 + player_count * 14, 28))
    pg.draw.rect(screen, LIGHT_GRAY,
                 (WIDTH - 34 - player_count * 14, HEIGHT - 118,
                  4 + player_count * 14, 28))
    
    for i in range(len(Teams[1].obj_list)):
        pg.draw.rect(screen, Teams[1].col,
                     (34 + 14 * (player_count - i - 1), HEIGHT - 114, 10, 20))
    
    for i in range(len(Teams[0].obj_list)):
        pg.draw.rect(screen, Teams[0].col,
                     (WIDTH - 30 - (player_count - i) * 14,
                      HEIGHT - 114, 10, 20))
  
    if flag:
        pg.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), 5)

    pg.display.flip()


def is_not_collided():
    flag_lst = [screen.get_at((
        WIDTH // 2 + int(ceil(5 * cos(pi * k / 4))),
        HEIGHT // 2 + int(ceil(5 * sin(pi * k / 4)))

    )) in avaliable_colors for k in range(8)] + \
               [screen.get_at((WIDTH // 2, HEIGHT // 2)) in avaliable_colors]

    return all(flag_lst)


def kill_players(det_pos):
    kills = 0
    dist = lambda P, Q: ((P[0] - Q[0])**2 + (P[1] - Q[1])**2)**.5

    dist_lst = [[],[]]
    dist_lst[0] = [dist(pl.pos, det_pos) for pl in Teams[0].obj_list]
    dist_lst[1] = [dist(pl.pos, det_pos) for pl in Teams[1].obj_list]

    for k in [0, 1]:
        for i in range(len(dist_lst[k])):
            if dist_lst[k][i] <= 50:
                killed = Teams[k].obj_list[i]
                Teams[k].obj_list.remove(killed)
                kills += 1
    return kills


def evaluated_value(func: str, val):
    global lasterr

    lasterr = ""
    for f in xxx:
        if f in func:
            func = func.replace(f, f[:f.index('x')] + " "
                                + f[f.index('x') + 1:])

    func = func.replace("x", str(val / 40))
    for f in xxx:
        fx = f[:f.index('x')] + " " + f[f.index('x') + 1:]
        func = func.replace(fx, f)

    func = func.replace('^', '**')

    for f in fconvert:
        func = func.replace(f, fconvert[f])

    try:
        if '|' in func:
            if func.count('|') % 2 == 0:
                func = func.replace("|", "abs(",
                                    func.count('|') // 2)
                func = func.replace("|", ")")
            else:
                raise SyntaxError("unmatched '|' (1 line)")

        # Проверка на допустимые слова и символы
        fnc = func
        for x in (list(xxx) + list(fconvert.values())
                  + list(you_god_damn_right)):
            fnc = fnc.replace(x, " ")

        for c in fnc:
            if c not in "01234567890. \t\r":
                raise SyntaxError("Undefined syntax (1 line)")

        return -int(40 * eval(func))
    except (ZeroDivisionError, NameError):
        lasterr = "ZeroDiv" if 'Zero' in str(exc_info()[0]) else "Name"
        return str(exc_info()[1])
    except SyntaxError:
        lasterr = "Syntax"
        return str(exc_info()[1])[:str(exc_info()[1]).index(' (')]
    except TypeError:
        lasterr = "Type"
        if 'complex' in str(exc_info()[1]):
            return "Complex numbers are forbidden!"

        return str(exc_info()[1])
    except ValueError:
        lasterr = "Value"
        return "Forbidden value!"


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
