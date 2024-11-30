import pygame as pg

pg.init()
pg.display.set_caption("Task - C")

screen = pg.display.set_mode((640, 480))

running = True
mode = 0 # not drawing
old_pos = (0, 0); new_pos = (0, 0)
stack = []; area = (0, 0, 0, 0)
while running:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

# If pressed mouse button: mode changing ===============================================================================

        if event.type == pg.MOUSEBUTTONDOWN:
            mode = 1 # drawing
            old_pos = pg.mouse.get_pos()

# Then it moves: reading the area of rect (tuple of 4 integers) ========================================================

        if event.type == pg.MOUSEMOTION and mode == 1:
            new_pos = pg.mouse.get_pos()

            if new_pos[0] > old_pos[0] and new_pos[1] > old_pos[1]:
                area = (old_pos[0], old_pos[1], new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])

            elif new_pos[0] < old_pos[0] and new_pos[1] < old_pos[1]:
                area = (new_pos[0], new_pos[1], -new_pos[0] + old_pos[0], -new_pos[1] + old_pos[1])

            elif new_pos[0] > old_pos[0] and new_pos[1] < old_pos[1]:
                area = (old_pos[0], new_pos[1], new_pos[0] - old_pos[0], -new_pos[1] + old_pos[1])

            elif new_pos[0] < old_pos[0] and new_pos[1] > old_pos[1]:
                area = (new_pos[0], old_pos[1], -new_pos[0] + old_pos[0], new_pos[1] - old_pos[1])

            screen.fill((0, 0, 0))
            for ar in stack:
                pg.draw.rect(screen, (255, 255, 255), ar, 2)
                screen.blit(screen, (0, 0))

            pg.draw.rect(screen, (255, 255, 255), area, 2)

# Then stoped pressing of mouse button: appending area in stack ========================================================

        if event.type == pg.MOUSEBUTTONUP:
            mode = 0
            stack.append(area)

# Keyboard event (rect deleting from stack) ============================================================================

        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if keys[pg.K_LCTRL] and keys[pg.K_z]:
                stack = stack[:-1]

                screen.fill((0, 0, 0))
                for ar in stack:
                    pg.draw.rect(screen, (255, 255, 255), ar, 2)
                    screen.blit(screen, (0, 0))

    pg.display.flip()