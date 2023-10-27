import pygame
import sys
import Settings.render_settings as render_settings
import GUI.game_render as game_render
from playwAI import PlaywAI
from playwAI_EASY import PlaywAI_EASY

class MenuPlaywithAI:
    def __init__(self) -> None:
        self.running = True
        self.easy = False
        self.hard = False

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

            EASY_BTN = game_render.Button(screen=self.screen, pos=(425, 300), text_input='Easy', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(160, 40))

            HARD_BTN = game_render.Button(screen=self.screen, pos=(425, 350), text_input='Hard', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(200, 40))

            font = pygame.font.Font("Asset/Huggo-3zdZG.otf", 50)
            text = font.render("PLAY WITH AI", True, render_settings.COLOR_WHITE)
            text_rect = text.get_rect(center=(425, 150))
            self.screen.blit(text,text_rect)

            # draw button
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for button in [HOME_BTN, EASY_BTN, HARD_BTN]:
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
                    if EASY_BTN.checkForInput(MENU_MOUSE_POS):
                        self.running = False
                        play_easy = PlaywAI_EASY()
                        play_easy.loop()
                    if HARD_BTN.checkForInput(MENU_MOUSE_POS):
                        self.running = False
                        play = PlaywAI()
                        play.loop()
                        
                        
                        
                   
            pygame.display.update()