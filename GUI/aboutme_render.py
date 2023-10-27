import pygame
import sys

import GUI.game_render as game_render
import Settings.render_settings as render_settings
from GUI.menu_render import Menu

class Aboutme:
    def __init__(self) -> None:
        self.running = True
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)

    # def __del__(self):
    #     pass

    

    def loop(self):
        while self.running:
            
            bg = pygame.image.load('Asset/bg.jpg')
            bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
            self.screen.blit(bg, (0, 0))

            HOME_BTN = game_render.Button(screen=self.screen, pos=(425, 550), text_input='Home', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(100, 40))

            # set title game
            font_title = pygame.font.Font("Asset/RoleverBold-GOVBD.ttf", 50)
            font = pygame.font.Font("Asset/Rubik-Medium.ttf", 20)
            
            # Introduce
            line_title = font_title.render("Introduce", True, "#ffffff")
            intro1 = font.render("Developer:",True, "#ffffff")
            intro1_1 = font.render("Nguyễn Thành Danh B2012067",True, "#ffffff")
            # Version
            intro2 = font.render("Version:",True, "#ffffff")
            intro2_2 = font.render("1.0 (demo)",True, "#ffffff")
            # Release
            intro3 = font.render("Release:",True, "#ffffff")
            intro3_3 = font.render("27/8/2023",True, "#ffffff")
            # Engine
            intro4 = font.render("Engine:",True, "#ffffff")
            intro4_4 = font.render("Python, pygame",True, "#ffffff")

            self.screen.blit(line_title,(380, 320 - 30))
            #developer
            self.screen.blit(intro1,(380, 380 - 30))
            self.screen.blit(intro1_1,(500, 380 - 30))
            #version
            self.screen.blit(intro2,(380, 400 - 30))
            self.screen.blit(intro2_2,(500, 400 - 30))
            #release
            self.screen.blit(intro3,(380, 420 - 30))
            self.screen.blit(intro3_3,(500, 420 - 30))
            #Engine
            self.screen.blit(intro4,(380, 440 - 30))
            self.screen.blit(intro4_4,(500, 440 - 30))

            # draw button
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for button in [HOME_BTN]:
                button.changeColor(MENU_MOUSE_POS)
                button.update()

            # check event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HOME_BTN.checkForInput(MENU_MOUSE_POS):
                        self.running = False
            
            img = pygame.image.load_extended('Asset/giphy.gif')
            img = pygame.transform.scale(img, (320, 320))
            self.screen.blit(img, (50, 130))
            pygame.display.update()
