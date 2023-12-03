import pygame
import sys
import GUI.game_render as game_render
import Settings.render_settings as render_settings

class Menu:
    def __init__(self) -> None:
        self.running = True
        self.MenuPlaywAI = False
        self.playwFriend = False
        self.aboutme = False
        self.rank = False
        self.quit = False

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)

    def init_btn(self):
        self.MenuPlaywAI = False
        self.playwFriend = False
        self.rank = False
        self.aboutme = False
        self.guide = False
        self.quit = False

    def loop(self):
        while self.running:

            bg = pygame.image.load('Asset/bg.jpg')
            bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
            self.screen.blit(bg, (0, 0))

            # create btn
            PLAYWAI_BTN = game_render.Button(screen=self.screen, pos=(425, 280), text_input='Play with AI', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(210, 40))

            PLAYWFRIEND_BTN = game_render.Button(screen=self.screen, pos=(425, 330), text_input='Play with Friend', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(265, 40))

            RANK_BTN = game_render.Button(screen=self.screen, pos=(425, 380), text_input='Rank', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(120, 40))

            ABOUTME_BTN = game_render.Button(screen=self.screen, pos=(100, 550), text_input='About me', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(140, 40))

            GUIDE_BTN = game_render.Button(screen=self.screen, pos=(260, 550), text_input='Guide', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(140, 40))

            QUIT_BTN = game_render.Button(screen=self.screen, pos=(780, 550), text_input='Quit', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(100, 40))

            #set title game
            font = pygame.font.Font("Asset/CweamyOutline-eZBDm.otf", 120)
            text = font.render("GAME CARO", True, render_settings.COLOR_WHITE)
            text_rect = text.get_rect(center=(425, 150))
            self.screen.blit(text,text_rect)

            # draw btn
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for btn in [PLAYWAI_BTN, PLAYWFRIEND_BTN, ABOUTME_BTN, GUIDE_BTN, RANK_BTN, QUIT_BTN]:
                btn.changeColor(MENU_MOUSE_POS)
                btn.update()

            # check event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAYWAI_BTN.checkForInput(MENU_MOUSE_POS):
                        self.init_btn()
                        self.MenuPlaywAI = True
                        self.running = False
                    if PLAYWFRIEND_BTN.checkForInput(MENU_MOUSE_POS):
                        self.init_btn()
                        self.playwFriend = True
                        self.running = False
                    if RANK_BTN.checkForInput(MENU_MOUSE_POS):
                        self.init_btn()
                        self.rank = True
                        self.running = False
                    if ABOUTME_BTN.checkForInput(MENU_MOUSE_POS):
                        self.init_btn()
                        self.aboutme = True
                        self.running = False
                    if GUIDE_BTN.checkForInput(MENU_MOUSE_POS):
                        self.init_btn()
                        self.guide = True
                        self.running = False
                    if QUIT_BTN.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
    

