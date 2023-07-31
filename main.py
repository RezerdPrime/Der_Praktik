from Technical_Stuff import *

while running:
    mouse_pos = pg.mouse.get_pos()
    butts = []
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        # MENU =========================================================
        
        if mode == "menu":
            # print("menu")
            screen.fill(WHITE)
            if ((WIDTH - 174) // 2 < mouse_pos[0] <
               (WIDTH - 174) // 2 + 171):
                if ((HEIGHT - 270) // 2 < mouse_pos[1] <
                   (HEIGHT - 270) // 2 + 70):
                    PLAY_color = (255, 255, 255)
                    EDITOR_color = (0, 0, 0)
                    SETTINGS_color = (0, 0, 0)
                    pos_flag = 0
                elif ((HEIGHT - 70) // 2 < mouse_pos[1] <
                      (HEIGHT - 70) // 2 + 70):
                    PLAY_color = (0, 0, 0)
                    EDITOR_color = (255, 255, 255)
                    SETTINGS_color = (0, 0, 0)
                    pos_flag = 1
                elif ((HEIGHT + 130) // 2 < mouse_pos[1] <
                      (HEIGHT + 130) // 2 + 70):
                    PLAY_color = (0, 0, 0)
                    EDITOR_color = (0, 0, 0)
                    SETTINGS_color = (255, 255, 255)
                    pos_flag = 2
            else:
                PLAY_color = (0, 0, 0)
                EDITOR_color = (0, 0, 0)
                SETTINGS_color = (0, 0, 0)
                pos_flag = -1
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if pos_flag == 0:
                    mode = "game"
                elif pos_flag == 1:
                    mode = "editor"
                elif pos_flag == 2:
                    mode = "settings"
                
                transitional_animation()
            
            if mode == "menu":
                menu_interface(PLAY_color, EDITOR_color, SETTINGS_color)
        
        # SETTINGS =====================================================
        
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
            # screen.blit(screen, (0, 0))
            
            # Кнопка возврата обратно в меню
            pg.draw.rect(screen, GRAY,
                         (WIDTH - 195, HEIGHT - 145, 120, 70))
            pg.draw.rect(screen, LIGHT_GRAY,
                         (WIDTH - 200, HEIGHT - 150, 120, 70))
            text2 = font40.render(
                "Back", True, BACK_color)
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
            
        # EDITOR =======================================================
        
        elif mode == "editor":
            # print("editor")
            screen.fill(WHITE)
            
            pg.draw.rect(screen, LIGHT_GRAY, (
                (WIDTH - 174) // 2, (HEIGHT - 270) // 2, 174, 70))
            screen.blit(screen, (0, 0))
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = "menu"
                transitional_animation()
        
        # GAME =========================================================
        
        elif mode == "game":
            font60 = pg.font.Font("fnt.otf", 60)
            text3 = font60.render("You are otchislen",
                                  True, (190, 30, 0))
            for _ in range(1000):
                text3.set_alpha(1)
                screen.blit(text3, ((WIDTH - text3.get_width()) // 2,
                                    (HEIGHT - text3.get_height()) // 2))
                pg.display.flip()
                
            pg.time.wait(500)
            if event.type == pg.MOUSEBUTTONDOWN:
                mode = 'menu'
                
    pg.display.flip()

pg.quit()
