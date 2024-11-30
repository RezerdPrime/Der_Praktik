import pygame as pg
import random

pg.init()
width = 640
height = 480
pg.display.set_caption("Task - A")
screen = pg.display.set_mode((width, height))
all_sprites = pg.sprite.Group()
sprite = pg.sprite.Sprite()
clock = pg.time.Clock()
fps = 60

pos = (0, 0)

horizontal_borders = pg.sprite.Group()
vertical_borders = pg.sprite.Group()

class Border(pg.sprite.Sprite):

    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)

Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

class Ball(pg.sprite.Sprite):

    def __init__(self, radius, x, y, flag = 1):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pg.Surface((2 * radius, 2 * radius),
                                    pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color("red"),
                           (radius, radius), radius)
        self.rect = pg.Rect(x, y, 2 * radius - 5, 2 * radius - 5)
        self.vx = random.randint(-10,11)
        self.vy = random.randint(-10,11)
        self.flag = flag
        self.x = x
        self.y = y

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        x1 = horizontal_borders.copy(); x1.remove(list(x1)[0])
        x2 = horizontal_borders.copy(); x2.remove(list(x2)[1])
        y1 = vertical_borders.copy(); y1.remove(list(y1)[0])
        y2 = vertical_borders.copy(); y2.remove(list(y2)[1])

        if pg.sprite.spritecollide(self, x1, 0) and self.vy > 0: # Lower
            self.vy = -self.vy
            self.y += 10
            self.flag = 0

        if pg.sprite.spritecollide(self, x2, 0) and self.vy < 0: # Higher
            self.vy = -self.vy
            self.y -= 10
            self.flag = 0

        if pg.sprite.spritecollide(self, y1, 0) and self.vx > 0: # Right
            self.vx = -self.vx
            self.x -= 10
            self.flag = 0

        if pg.sprite.spritecollide(self, y2, 0) and self.vx < 0: # Left
            self.vx = -self.vx
            self.x += 10
            self.flag = 0

        all_sp_buff = all_sprites.copy(); all_sp_buff.remove(self)

        if pg.sprite.spritecollide(self, all_sp_buff, 0) and not self.flag:
            self.vy = -self.vy
            self.vx = -self.vx

all_sprites = pg.sprite.Group()
for _ in range(5):
    B = Ball(20, 100, 100)

running = True
while running:

    pos = pg.mouse.get_pos()
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            Ball(20, *pos, 0)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pg.display.flip()
    clock.tick(fps)
