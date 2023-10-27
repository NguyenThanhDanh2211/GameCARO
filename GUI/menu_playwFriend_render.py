import pygame
import sys
import Settings.render_settings as render_settings
import GUI.game_render as game_render
from GUI.aboutme_render import Aboutme


class playwFriend:
    def __init__(self) -> None:
        self.running = True
        self._continue = False
        self.newBoard = False

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)

    def loop(self):
        while self.running:
            bg = pygame.image.load('Asset/bg.jpg')
            bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
            self.screen.blit(bg, (0, 0))

            HOME_BTN = game_render.Button(screen=self.screen, pos=(425, 550), text_input='Home', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(100, 40))

            CONTINUE_BTN = game_render.Button(screen=self.screen, pos=(425, 300), text_input='Continue', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(160, 40))

            NEWGAME_BTN = game_render.Button(screen=self.screen, pos=(425, 350), text_input='New Game', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(200, 40))

            font = pygame.font.Font("Asset/Huggo-3zdZG.otf", 50)
            text = font.render("PLAY WITH FRIEND", True, render_settings.COLOR_WHITE)
            text_rect = text.get_rect(center=(425, 150))
            self.screen.blit(text,text_rect)

            # draw button
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for button in [HOME_BTN, CONTINUE_BTN, NEWGAME_BTN]:
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
                    if CONTINUE_BTN.checkForInput(MENU_MOUSE_POS):
                        aboutme = Aboutme()
                        aboutme.loop()
                        self.running = False
            pygame.display.update()
