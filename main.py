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
                        text3 = font40.render("Do you want to load your map?", True, (0, 0, 0))
                        screen.blit(text3, (WIDTH // 2 - 292, HEIGHT // 2 - 140))

                        text3 = font40.render("Yes", True, YES_color)
                        screen.blit(text3, (WIDTH // 2 - 292, HEIGHT // 2 - 86))
                        text3 = font40.render("No", True, NO_color)
                        screen.blit(text3, (WIDTH // 2 + 234, HEIGHT // 2 - 86))

                        screen.blit(screen, (0, 0))

                        pg.display.flip()
                        for ev in pg.event.get():

                            if event.type == pg.QUIT: exit()

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

                elif pos_flag == 1: mode = "editor" # Соответственно на кнопке "Editor"
                elif pos_flag == 2: mode = "settings" # На кнопке "Settings"

                if pos_flag != -1: transitional_animation()

            if mode == "menu":
                menu_interface(PLAY_color, EDITOR_color, SETTINGS_color)


# SETTINGS =============================================================================================================

        elif mode == "settings":

            screen.fill(WHITE)

            pg.draw.rect(screen, LIGHT_GRAY, (75, 75, 500, 70))
            text2 = font20.render(
                "All changes occur after restarting the game!",
                True, RED)

            screen.blit(text2, (75, HEIGHT - 75))

            text2 = font40.render("RESOLUTION" + " " * 4 +
                                  str(resolutions[current][0]) + " : "
                                  + str(resolutions[current][1]),
                                  True, REZOL_color)
            screen.blit(text2, (95, 85))

            # Кнопка возврата обратно в меню
            pg.draw.rect(screen, GRAY,
                         (WIDTH - 195, HEIGHT - 145, 120, 70))
            pg.draw.rect(screen, LIGHT_GRAY,
                         (WIDTH - 200, HEIGHT - 150, 120, 70))

            text2 = font40.render("Back", True, BACK_color)

            screen.blit(text2, (WIDTH - 140 - text2.get_width() // 2,
                                HEIGHT - 115 - text2.get_height() // 2))

            if (75 < mouse_pos[0] < 475) and (75 < mouse_pos[1] < 145):
                REZOL_color = WHITE
                at_button = 1

            elif ((WIDTH - 200 < mouse_pos[0] < WIDTH - 80)
                  and (HEIGHT - 150 < mouse_pos[1] < HEIGHT - 80)):
                BACK_color = WHITE
                at_button = 2

            else:
                REZOL_color = BACK_color = BLACK
                at_button = 0

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                if at_button == 1:
                    current = (current + 1) % len(resolutions)
                    config.set('Screen', 'width',
                               str(resolutions[current][0]))
                    config.set('Screen', 'height',
                               str(resolutions[current][1]))
                    with open("config.cfg", "w",
                              encoding='utf-8') as config_file:
                        config.write(config_file)

                elif at_button == 2:
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

            step_is_going = True
            if not already_generated:
                if YorN % 2 == 0:
                    Mappy.generate()
                    #print([(*obj.color, *obj.pos, obj.radius) for obj in Map.obj_list]) это кстати ещё пригодится

                else: #load the map
                    convert_data(load_data())

                already_generated = True

                helpMap.obj_list += Mappy.obj_list
                Teams[0].generate(helpMap)
                helpMap.obj_list += Teams[0].player_list
                Teams[1].generate(helpMap)

            cur_player = Teams[step % 2].player_list[randint(0, player_count - 1)]
            dx -= cur_player.pos[0]
            dy -= cur_player.pos[1]

            while step_is_going:

                prevmp = mouse_pos
                mouse_pos = pg.mouse.get_pos()
                for ev in pg.event.get():

                    if ev.type == pg.QUIT: exit()

                    if ev.type == pg.MOUSEBUTTONDOWN:
                        mouse_mode = 2

                    if (ev.type == pg.MOUSEMOTION) and (mouse_mode == 2):
                        mouse_pos = pg.mouse.get_pos()
                        dx += mouse_pos[0] - prevmp[0]
                        dy += mouse_pos[1] - prevmp[1]

                    if ev.type == pg.MOUSEBUTTONUP:
                        mouse_mode = 1

                    if ev.type == pg.KEYDOWN:
                        if ev.unicode.isprintable():
                            func += ev.unicode

                        elif ev.key == pg.K_BACKSPACE:
                            func = func[:-1]

                        keys = pg.key.get_pressed()

                        if keys[pg.K_RETURN]:
                            #cur_player.attack(dx, dy, func)
                            pass
                            '''try:
                                Plot(func)
                                print(mappy.obj_list)
                                pg.time.delay(1500)

                            except SyntaxError as err:
                                pass
                            except NameError as err:
                                pass
                            except Exception as err:
                                pass

                            func = ""'''

                draw_map(dx, dy, func)
            step += 1

    pg.display.flip()
