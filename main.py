from Technical_Stuff import *

while running:

    prevmp = mouse_pos
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

                if pos_flag == 0: # На кнопке "Play"
                    mode = "game"
                    menu_interface(PLAY_color, EDITOR_color, SETTINGS_color)
                    overlay2.set_alpha(100)
                    screen.blit(overlay2, (0, 0))

                    while choose:

                        pg.draw.rect(screen, WHITE, (WIDTH // 2 - 340, HEIGHT // 2 - 160, 700, 150))
                        pg.draw.rect(screen, LIGHT_GRAY, (WIDTH // 2 - 350, HEIGHT // 2 - 170, 700, 150))
                        text3 = font.render("Do you want to load your map?", True, (0, 0, 0))
                        screen.blit(text3, (WIDTH // 2 - 292, HEIGHT // 2 - 140))

                        text3 = font.render("Yes", True, YES_color)
                        screen.blit(text3, (WIDTH // 2 - 292, HEIGHT // 2 - 86))
                        text3 = font.render("No", True, NO_color)
                        screen.blit(text3, (WIDTH // 2 + 234, HEIGHT // 2 - 86))

                        screen.blit(screen, (0, 0))

                        pg.display.flip()
                        for ev in pg.event.get(): # Я сам ахуел, что пришлось снова бегать по циклу
                            if ev.type == pg.KEYDOWN:

                                YorN += 1
                                if YorN % 2 == 0:
                                    YES_color = WHITE
                                    NO_color = BLACK
                                else:
                                    YES_color = BLACK
                                    NO_color = WHITE

                                keys = pg.key.get_pressed()
                                if keys[pg.K_RETURN]:
                                    choose = False

                                    if YorN % 2 != 0: #yes
                                        pass # не готово
                                        # по сути должно вызывать проводник с выбором файла

                                    #else: тупо идём дальше

                elif pos_flag == 1: mode = "editor" # Соответственно на кнопке "Editor"
                elif pos_flag == 2: mode = "settings" # На кнопке "Settings"

                transitional_animation()

            if mode == "menu":
                menu_interface(PLAY_color, EDITOR_color, SETTINGS_color)

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
            #print(YorN)
            if not already_generated:

                if YorN % 2 == 0:
                    Map.generate()
                else: #load the map
                   Map.generate() # пока пусть будет рандомная генерация
                already_generated = True
                #print(Map.obj_list)

            '''if event.type == pg.MOUSEBUTTONDOWN:
                mode = 2

            if (event.type == pg.MOUSEMOTION) and (mode == 2):
                x, y = pg.mouse.get_pos()
                a += x - xbuff
                b += y - ybuff

            if event.type == pg.MOUSEBUTTONUP:
                mode = 1'''






    pg.display.flip()


# Вот только попробуй сказать мне, что код кринж, я и без тебя это знаю
