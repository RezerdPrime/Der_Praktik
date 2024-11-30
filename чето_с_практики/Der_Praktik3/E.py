import pygame as pg
from math import *

pg.init()
pg.display.set_caption("Task - E")

W = 640
H = 480
val = 0; valfl = 1
k = 2; a = 0.01; counter = 0
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
fps = 60

color = pg.Color(100, 100, 100)
color.hsva = (100, 100, 100, 100)

mode = 0
running = True
while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_SPACE]:
                counter += 1
                if counter % 2 != 0: a = 0
                else: a = 0.01

    screen.fill((0, 0, 0))
    for i in range(0, 360):
        color.hsva = (i, val, 100, 100)
        pg.draw.line(screen, color,
                     (int(cos(radians(i)) * 200) + W // 2, int(sin(radians(i)) * 200) + H // 2),
                     (int(cos(radians(i * k)) * 200) + W // 2, int(sin(radians(i * k)) * 200) + H // 2))
    k += a
    if counter % 2 == 0:
        val += valfl
        if val == 100: valfl = -1
        if val == 0: valfl = 1

    pg.draw.circle(screen, (255, 255, 255), (W // 2, H // 2), 200, 2)
    pg.display.flip()
    clock.tick(fps)