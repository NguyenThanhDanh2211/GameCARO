import pygame
import sys
import GUI.game_render as game_render
import Settings.render_settings as render_settings

class Guide:
    def __init__(self) -> None:
        self.running = True
        self.__screen_size = (850, 600)
        self.__screen = pygame.display.set_mode(self.__screen_size[:2])
        # pygame.display.get_caption("Caro")

    def __del__(self):
        pass

    def loop(self):
        while self.running:
            # set bg
            bg = pygame.image.load('Asset/bg.jpg')
            bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
            self.__screen.blit(bg, (0, 0))

            # create btn
            MENU_BTN = game_render.Button(screen=self.__screen, pos=(425, 600-50),text_input="Menu", font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 35), base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(120, 40))

            # set title game
            font = pygame.font.Font("Asset/Rubik-Medium.ttf", 17)
            font_title = pygame.font.Font("Asset/Rubik-Medium.ttf", 24)
            font_title_htp = pygame.font.Font("Asset/Huggo-3zdZG.otf", 45)

            # How to Play Caro
            line_title_1 = font_title_htp.render("How to Play Caro?", True, "#ffffff")
            line_title_1_2 = font_title.render("Objective:", True, "#ffffff")
            line1 = font.render("The objective of the game is to form a continuous row of five of your own ", True, "#ffffff")
            line1_1 = font.render("pieces either horizontally, vertically, or diagonally on the game board.", True, "#ffffff")
            line_title_2 = font_title.render("Game set up:", True, "#ffffff")
            line2_1 = font.render("1. The game is typically played on a 15x15 grid.", True, "#ffffff")
            line2_2 = font.render("2. Players take turns placing their pieces on the intersections of the grid.", True, "#ffffff")
            line2_3 = font.render("3. One player uses 'X' as their pieces, and the other uses 'O'.", True, "#ffffff")
            line_title_3 = font_title.render("Gameplay:", True, "#ffffff")
            line3_1 = font.render("1. Players take turns placing one of their pieces on an empty intersection on the board.", True, "#ffffff")
            line3_2 = font.render("2. Once placed, pieces cannot be moved or removed from the board.", True, "#ffffff")
            line3_3 = font.render("3. The first player to get five of their pieces in a row (horizontally, vertically, or diagonally) ", True, "#ffffff")
            line3_3_1 = font.render("wins the game.", True, "#ffffff")
            line3_4 = font.render("4. If the board fills up before either player achieves five in a row, the game is a draw.", True, "#ffffff")
            line_title_4 = font_title.render("Winning:", True, "#ffffff")
            line4_1 = font.render("The game is won when one player forms a row of five of their pieces. The row ", True, "#ffffff")
            line4_2 = font.render("can be in any direction: horizontal, vertical, or diagonal.", True, "#ffffff")

            self.__screen.blit(line_title_1,(30, 60 ))
            self.__screen.blit(line_title_1_2,(30, 140 - 30))
            self.__screen.blit(line1,(155, 147 - 30))
            self.__screen.blit(line1_1,(30, 167 - 30))
            self.__screen.blit(line_title_2,(30, 197 - 30))
            self.__screen.blit(line2_1,(30, 227 - 30))
            self.__screen.blit(line2_2,(30, 247 - 30))
            self.__screen.blit(line2_3,(30, 267 - 30))
            self.__screen.blit(line_title_3,(30, 297 - 30))
            self.__screen.blit(line3_1,(30, 327 - 30))
            self.__screen.blit(line3_2,(30, 347 - 30))
            self.__screen.blit(line3_3,(30, 367 - 30))
            self.__screen.blit(line3_3_1,(30, 387 - 30))
            self.__screen.blit(line3_4,(30, 407 - 30))
            self.__screen.blit(line_title_4,(30, 437 - 30))
            self.__screen.blit(line4_1,(140, 445 - 30))
            self.__screen.blit(line4_2,(30, 465 - 30))
            

            # draw button
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            for button in [MENU_BTN]:
                button.changeColor(MENU_MOUSE_POS)
                button.update()
            # check vent
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_BTN.checkForInput(MENU_MOUSE_POS):
                        self.running = False
            pygame.display.update()
