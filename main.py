from Technical_Stuff import *

while running:

    mouse_pos = pg.mouse.get_pos()
    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False


# MENU =================================================================================================================

        if mode == "menu":
            #print("menu")
            screen.fill(WHITE)

            if (WIDTH - 174) // 2 < mouse_pos[0] < (WIDTH - 174) // 2 + 171:

                if (HEIGHT - 270) // 2 < mouse_pos[1] < (HEIGHT - 270) // 2 + 70:
                    PLAY_color = (255, 255, 255)
                    EDITOR_color = (0, 0, 0)
                    SETTINGS_color = (0, 0, 0)
                    pos_flag = 0

                elif (HEIGHT - 70) // 2 < mouse_pos[1] < (HEIGHT - 70) // 2 + 70:
                    PLAY_color = (0, 0, 0)
                    EDITOR_color = (255, 255, 255)
                    SETTINGS_color = (0, 0, 0)
                    pos_flag = 1

                elif (HEIGHT + 130) // 2 < mouse_pos[1] < (HEIGHT + 130) // 2 + 70:
                    PLAY_color = (0, 0, 0)
                    EDITOR_color = (0, 0, 0)
                    SETTINGS_color = (255, 255, 255)
                    pos_flag = 2

            else:
                PLAY_color = (0, 0, 0)
                EDITOR_color = (0, 0, 0)
                SETTINGS_color = (0, 0, 0)
                pos_flag = -1


            if event.type == pg.MOUSEBUTTONDOWN:

                if pos_flag == 0: mode = "game"
                elif pos_flag == 1: mode = "editor"
                elif pos_flag == 2: mode = "settings"

                transitional_animation()

            if mode == "menu":

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

# SETTINGS =============================================================================================================

        elif mode == "settings":
            #print("settings")

            screen.fill(WHITE)

            pg.draw.rect(screen, LIGHT_GRAY, (75, 75, 400, 70))
            font2 = pg.font.Font(None, 28) # "PostalShrift.ttf"

            text2 = font2.render("All changes occur after restarting the game!", True, (255, 50, 50))
            screen.blit(text2, (75, HEIGHT - 75))

            text2 = font.render("RESOLUTION" + " " * 4 +
                                str(resolutions[current][0]) + " : " + str(resolutions[current][1]), True, REZOL_color)
            screen.blit(text2, (98, 98))

            screen.blit(screen, (0, 0))

            if (75 < mouse_pos[0] < 475) and (75 < mouse_pos[1] < 145):
                REZOL_color = WHITE
                at_button = 1
            else: REZOL_color = BLACK

            if at_button == 1 and event.type == pg.MOUSEBUTTONDOWN:
                current = (current + 1) % 6

            '''config = configparser.ConfigParser()
            config.read('config.cfg', encoding="utf-8")
            config.set('Screen', 'width', str(resolutions[current][0]))
            config.set('Screen', 'heigth', str(resolutions[current][0]))

            with open('config.cfg', 'w') as cfgfile:
                config.write(cfgfile)'''

            if event.type == pg.MOUSEBUTTONDOWN:
                mode = "menu"
                transitional_animation()



# EDITOR ===============================================================================================================

        elif mode == "editor":
            #print("editor")
            screen.fill(WHITE)

            pg.draw.rect(screen, LIGHT_GRAY, ((WIDTH - 174) // 2, (HEIGHT - 270) // 2, 174, 70))
            screen.blit(screen, (0, 0))

            if event.type == pg.MOUSEBUTTONDOWN:
                mode = "menu"
                transitional_animation()


# GAME =================================================================================================================

        elif mode == "game":

            text3 = font.render("Do you want to load your map?", True, (255,255,255))
            screen.blit(text3, (98, 98))


    pg.display.flip()
