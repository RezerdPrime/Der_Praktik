import pygame as pg

pg.init()
pg.display.set_caption("Task - A")

W, N = list(map(int,input().split()))
sqr_size = W // N

screen = pg.display.set_mode((W, W))
screen.fill((255, 255, 255))

for i in range(sqr_size // 2):
    for j in range(sqr_size // 2):
        pg.draw.rect(screen, (0, 0, 0),
                     (i * 2 * sqr_size + sqr_size * (j % 2 != 0), j * sqr_size, sqr_size, sqr_size))
running = True
while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

    pg.display.flip()


'''import pygame as pg

pg.init()
pg.display.set_caption("a")
WIDTH = 640
HEIGHT = 480
WINDOW_SIZE = (WIDTH, HEIGHT)

screen = pg.display.set_mode(WINDOW_SIZE)
font = pg.font.Font(None, 22)

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

running = True
while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

    screen.fill(WHITE)

    pg.draw.circle(screen, RED, (WIDTH // 2, HEIGHT // 2), 10)
    text_surface = font.render("test", True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    pg.draw.rect(screen, GRAY, ((WIDTH - 160) // 2, (HEIGHT - 70) // 2, 160, 70))

    pg.display.flip()
'''