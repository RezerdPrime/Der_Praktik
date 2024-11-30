import pygame as pg

pg.init()
screen_width = 640
screen_height = 480
screen = pg.display.set_mode((screen_width, screen_height))
screen.fill((255, 255, 255))

x = 0;
y = 0
a = 0;
b = 0
xbuff = 0;
ybuff = 0
mode = 1

# Создаем поверхность для отображения объектов
objects_surface = pg.Surface((screen_width, screen_height), pg.SRCALPHA)

running = True
while running:

    xbuff = x
    ybuff = y
    x, y = pg.mouse.get_pos()

    for event in pg.event.get():

        if (event.type == pg.QUIT) and (mode == 1):
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mode = 2

        if (event.type == pg.MOUSEMOTION) and (mode == 2):
            x, y = pg.mouse.get_pos()
            a += x - xbuff
            b += y - ybuff

        if event.type == pg.MOUSEBUTTONUP:
            mode = 1

    # Отображаем объекты на отдельной поверхности
    objects_surface.fill((0, 0, 0, 0))
    pg.draw.circle(objects_surface, (255, 0, 0), (320, 240), 10)
    pg.draw.circle(objects_surface, (0, 255, 0), (320, 200), 10)
    pg.draw.circle(objects_surface, (0, 0, 255), (320, 160), 10)

    # Получаем смещение в зависимости от положения мыши
    offset_x = a % screen_width
    offset_y = b % screen_height

    # Создаем под-поверхность для отображения только части экрана
    sub_screen_rect = pg.Rect(offset_x, offset_y, screen_width, screen_height)
    sub_screen = screen.subsurface(sub_screen_rect)

    # Отображаем под-поверхность на экране
    sub_screen.blit(objects_surface.subsurface(sub_screen_rect), (0, 0))
    pg.display.update()

pg.quit()