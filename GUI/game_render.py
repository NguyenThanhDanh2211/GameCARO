import pygame
import sys


from state import State
import Settings.render_settings as render_settings
import Settings.game_settings as game_settings

class GameRender:
    def __init__(self, state: State) -> None:
        self.state = State()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)
        self.running = True
        self.current_round = 1
        self.human_score = 0
        self.com_score = 0

        bg = pygame.image.load('Asset/bg.jpg')
        bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))

        blur_surface = pygame.Surface((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        blur_surface.set_alpha(150)  # Đặt độ trong suốt
        blur_surface.fill((255, 255, 255))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(blur_surface, (0, 0))
        # # pygame.display.update()

        if (len(state.moves) > 0):
            self.render_state(state.board, game_settings.FIRST_TURN_HUMAN, False, state.moves[-1], self.current_round, self.human_score, self.com_score)
        else:
            self.render_state(state.board, game_settings.FIRST_TURN_HUMAN, False, (-1,-1), self.current_round, self.human_score, self.com_score)
        pygame.display.update()

    def render_state(self, board, current_turn, player_win,last_move, current_round, human_score, com_score):
    
        """
        Hiển thị trạng thái của bàn cờ
        board: trạng thái hiện tại của bàn cờ
        current_turn: nước đi hiện tại
        player_win: người chiến thắng trò chơi
        last_move: nước đi trước
        current_round: vòng chơi hiện tại
        human_score: điểm của người chơi
        com_score: điểm của máy
        """
        
        self.clear()
        
        # COM WIN
        if(player_win == game_settings.COM):
            self.draw_board(board, render_settings.COM_WIN_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(player_win), current_round, human_score, com_score)
            return
        # HUMAN WIN
        if(player_win == game_settings.HUMAN):
            self.draw_board(board, render_settings.HUMAN_WIN_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(player_win), current_round, human_score, com_score)
            return
        if(player_win == game_settings.NO_ONE):
            last_turn = game_settings.get_opponent(current_turn)
            # DRAW
            if(current_turn == game_settings.NO_ONE):
                self.draw_board(board, render_settings.DRAW_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(last_turn), current_round, human_score, com_score)
                return
            # GAME IS NOT OVER YET. HUMAN TURN
            if(current_turn == game_settings.HUMAN):
                self.draw_board(board, render_settings.HUMAN_TURN_INFO_TEXT, render_settings.COLOR_BLUE, last_move, render_settings.get_last_move_color(last_turn), current_round, human_score, com_score)
                return
            # GAME IS NOT OVER YET. COM TURN
            if(current_turn == game_settings.COM):
                self.draw_board(board, render_settings.COM_TURN_INFO_TEXT, render_settings.COLOR_RED, last_move, render_settings.get_last_move_color(last_turn), current_round, human_score, com_score)
                return

    def draw_X(self, x, y, color):
        """
        Vẽ X theo tọa độ
        
        x: tọa độ x của ô
        y: 0-2
        """
        #    x
        # y ╔═════════════════════════════════▶
        #   ║ (X1, Y1) ╔═══╗ (X2, Y1)
        #   ║          ║   ║
        #   ▼ (X1, Y2) ╚═══╝ (X2, Y2)
        #
        # line 1: (X1, Y1) -> (X2, Y2)
        # line 2: (X1, Y2) -> (X2, Y1)
        pos_X1 = render_settings.BOARD_POS_X_MIN + y * render_settings.SQUARE_SIZE
        pos_X2 = render_settings.BOARD_POS_X_MIN + (y+1) * render_settings.SQUARE_SIZE
        pos_Y1 = render_settings.BOARD_POS_Y_MIN + x * render_settings.SQUARE_SIZE
        pos_Y2 = render_settings.BOARD_POS_Y_MIN + (x+1) * render_settings.SQUARE_SIZE
        # subtract cell border
        pos_X1 = pos_X1 + render_settings.X_CELL_BORDER
        pos_X2 = pos_X2 - render_settings.X_CELL_BORDER
        pos_Y1 = pos_Y1 + render_settings.X_CELL_BORDER
        pos_Y2 = pos_Y2 - render_settings.X_CELL_BORDER

        # draw line 1
        pygame.draw.line(self.screen, color, (pos_X1, pos_Y1), (pos_X2, pos_Y2), render_settings.X_LINE_THICKNESS)
        # draw line 2
        pygame.draw.line(self.screen, color, (pos_X1, pos_Y2), (pos_X2, pos_Y1), render_settings.X_LINE_THICKNESS)
        
    def draw_O(self, x, y, color):
        """
        Vẽ một hình tròn có bán kính O_RADIUS - O_CELL_BORDER ở tâm hình vuông tại vị trí (x,y) trên bảng.
        
        x: tọa độ X
        y: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        """
        posX = render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE/2 + y * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2
        posY = render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE/2 + x * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2

        radius = render_settings.O_RADIUS - render_settings.O_CELL_BORDER

        pygame.draw.circle(self.screen, color, [posX, posY], radius , render_settings.O_LINE_THICKNESS)
    
    def render_winner(self, winner_text, human_score, com_score):
        self.clear()

        font = pygame.font.Font('Asset/Rekilash-PKBxZ.otf', 100)
        winner_surface = font.render(winner_text, True, render_settings.COLOR_WIN)
        winner_rect = winner_surface.get_rect(center=(render_settings.WINDOW_WIDTH // 2, render_settings.WINDOW_HEIGHT // 2 -70))

        human_score_text = font.render(f"{human_score}", True, render_settings.COLOR_BLUE)
        com_score_text = font.render(f"{com_score}", True, render_settings.COLOR_RED)
        haicham = font.render(f":", True, render_settings.COLOR_WHITE)

        human_score_rect = human_score_text.get_rect(center=(render_settings.WINDOW_WIDTH // 2 -50, winner_rect.bottom + 50))
        haicham_rect = haicham.get_rect(center=(render_settings.WINDOW_WIDTH // 2, winner_rect.bottom + 50))
        com_score_rect = com_score_text.get_rect(center=(render_settings.WINDOW_WIDTH // 2 +50, winner_rect.bottom + 50))

        self.screen.blit(winner_surface, winner_rect)
        self.screen.blit(human_score_text, human_score_rect)
        self.screen.blit(haicham, haicham_rect)
        self.screen.blit(com_score_text, com_score_rect)

        pygame.display.update()
    
    def check_winner_final(self, current_round, human_score, com_score, rounds):
        if current_round > rounds:
            winner_text = ""
            if human_score > com_score:
                winner_text = f"Human win!"
            elif human_score < com_score:
                winner_text = f"AI win!"

            self.render_winner(winner_text, human_score, com_score)

            waiting = True
            while waiting:
                pygame.event.pump()  # Cập nhật trạng thái sự kiện
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                        self.running = False
                        waiting = False

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    def draw_info_text(self, text, textColor):
        """
        Hiển thị lượt chơi, cũng như người chiến thắng
        
        :text: text muốn hiển thị
        :textColor: (255, 255, 255)
        """
        text_pos = ((render_settings.WINDOW_WIDTH-render_settings.WINDOW_WIDTH/5+25), 130+render_settings.BORDER_SIZE + 30/2)

        font_text = pygame.font.Font('Asset/Huggo-3zdZG.otf', 30)
        text_surf = font_text.render(text, False, textColor)
        text_rect = text_surf.get_rect(center = text_pos)
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()

    def draw_turn_counter(self, current_round):
        text = f"Round {current_round}"
        font=pygame.font.Font('Asset/Rekilash-PKBxZ.otf', 85)
        text_surf = font.render(text, True, render_settings.COLOR_ROUND)
        text_rect = text_surf.get_rect(center=(render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5)+25, 80))
        self.screen.blit(text_surf, text_rect)
        # pygame.display.update()
    
    def draw_scores(self, human_score, com_score):
        font = pygame.font.Font('Asset/Rekilash-PKBxZ.otf', 50)
        human_score_text = font.render(f"{human_score}", True, render_settings.COLOR_BLUE)
        com_score_text = font.render(f"{com_score}", True, render_settings.COLOR_RED)
        haicham = font.render(f":", True, render_settings.COLOR_WHITE)

        human_score_rect = human_score_text.get_rect(center=(render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5)-15,180+render_settings.BORDER_SIZE + 30/2))
        com_score_rect = com_score_text.get_rect(center=(render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5)+50,180+render_settings.BORDER_SIZE + 30/2))
        haicham_rect = haicham.get_rect(center=((render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5) +17), 180+render_settings.BORDER_SIZE + 30/2))

        self.screen.blit(human_score_text, human_score_rect)
        self.screen.blit(haicham, haicham_rect)
        self.screen.blit(com_score_text, com_score_rect)
        
    def is_new_game_button_pressed(self):
        """
        Button New game, nếu được nhấn thì return True, ngược lại return False
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_x_position, mouse_y_position = mouse_position
            is_in_x_button_area = render_settings.NEWGAME_BUTTON_POS_X_MIN < mouse_x_position < render_settings.NEWGAME_BUTTON_POS_X_MAX
            is_in_y_button_area = render_settings.NEWGAME_BUTTON_POS_Y_MIN < mouse_y_position < render_settings.NEWGAME_BUTTON_POS_Y_MAX
            return is_in_x_button_area and is_in_y_button_area
        return False  

    def is_home_button_pressed(self):
        """
        Button Home, nếu được nhấn thì return True, ngược lại return False
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_x_position, mouse_y_position = mouse_position
            is_in_x_button_area = render_settings.HOME_BUTTON_POS_X_MIN < mouse_x_position < render_settings.HOME_BUTTON_POS_X_MAX
            is_in_y_button_area = render_settings.HOME_BUTTON_POS_Y_MIN < mouse_y_position < render_settings.HOME_BUTTON_POS_Y_MAX
            return is_in_x_button_area and is_in_y_button_area
        return False 
    
    def is_continue_button_pressed(self):
        """
        Button Continue, nếu được nhấn thì return True, ngược lại return False
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_x_position, mouse_y_position = mouse_position
            is_in_x_button_area = render_settings.CONTINUE_BUTTON_POS_X_MIN < mouse_x_position < render_settings.CONTINUE_BUTTON_POS_X_MAX
            is_in_y_button_area = render_settings.CONTINUE_BUTTON_POS_Y_MIN < mouse_y_position < render_settings.CONTINUE_BUTTON_POS_Y_MAX
            return is_in_x_button_area and is_in_y_button_area
        return False 


    def draw_board(self, board_state, info_text, info_text_color, last_move, last_move_color, current_round, human_score, com_score):
        """
        Vẽ bàn cờ, text, các button, nước đi trên bàn cờ, vòng chơi và điểm số
        It draws the board, the info text, the new game button, and the moves on the board.
        """
        # vẽ bàn cờ
        # vẽ đường thẳng
        for r in range (0, game_settings.BOARD_COL_COUNT + 1):
            
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK, 
            [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN], [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN + render_settings.BOARD_HEIGHT], render_settings.BOARD_LINE_WIDTH)
        # vẽ hàng ngang
        for r in range (0, game_settings.BOARD_ROW_COUNT + 1):
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK,
            [render_settings.BOARD_POS_X_MIN, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], [render_settings.BOARD_POS_X_MIN + render_settings.BOARD_WIDTH, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], render_settings.BOARD_LINE_WIDTH)
        
        
        # draw INFO TEXT
        self.draw_info_text(info_text, info_text_color)

        self.draw_scores(human_score, com_score)
        self.draw_turn_counter(current_round)

        continue_btn = Button(screen=self.screen, pos=(630, 490), text_input='Continue', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        continue_btn.update()
        newgame = Button(screen=self.screen, pos=(770, 490), text_input='New game', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        newgame.update()
        home = Button(screen=self.screen, pos=(700, 540), text_input='Home', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        home.update()
   
        # hiển thị nước đi trên bàn cờ
        last_move_r, last_move_c = last_move
        for r in range (0, game_settings.BOARD_ROW_COUNT):
            for c in range (0, game_settings.BOARD_COL_COUNT):
                # set color
                color = None
                if (r == last_move_r and c == last_move_c):
                    color = last_move_color
                else:
                    if board_state[r][c] == game_settings.O: 
                        color = render_settings.O_COLOR
                    elif board_state[r][c] == game_settings.X: 
                        color = render_settings.X_COLOR
                # Empty cell
                if board_state[r][c] == game_settings.EMPTY: 
                    continue
                # Human move
                if board_state[r][c] == game_settings.O: 
                    self.draw_O(r, c, color)
                # COM move
                if board_state[r][c] == game_settings.X: 
                    self.draw_X(r, c, color)
        pygame.display.update()

        # Announcement
        print("Drawing board is completed.")
        print("==================================================================")

    def handle_com_move(self, com_move, state: State):
        """
        Lấy nước đi của AI và hiển thị lên bàn cờ
        :com_move: nước đi do AI thực hiện
        :state: trạng thái hiện tại của bàn cờ
        :type state: State
        :return: nước đi do AI thực hiện
        """

        # Announcement
        print("AI move: (row:", com_move[0], ", column:", com_move[1], ").")

        state.update_move(game_settings.COM, com_move)
        return

    #HUMAN moves    
        
    def is_new_move_valid(self, mouse_position, state: State):
        """
        Nhấn vào vị trí bất kì trong bàn cờ, tại 1 ô trống thì đó là nước đi hợp lệ
        :mouse_position: vị trí nhấn chuột trên màn hình
        :state: State
        :type state: State
        :return: hàm trả về giá trị True, False
        """
        if (self.is_mouse_position_in_board_area(mouse_position)):
            square_x_position, square_y_position =  self.get_board_square_position(mouse_position)
            is_selected_square_empty = state.board[square_x_position][square_y_position] == game_settings.EMPTY
            return is_selected_square_empty
        else:
            return False

    def is_mouse_position_in_board_area(self, mouse_position):
        """
        Kiếm tra vị trí nhấn chuột có nằm trong bàn cờ hay không
        :mouse_position: vị trí (x, y)
        :return: Trả về True, False
        """
        mouse_x_position, mouse_y_position = mouse_position
        is_mouse_x_position_valid = render_settings.BOARD_POS_X_MIN < mouse_x_position < render_settings.BOARD_POS_X_MAX
        is_mouse_y_position_valid = render_settings.BOARD_POS_Y_MIN < mouse_y_position < render_settings.BOARD_POS_Y_MAX
        return is_mouse_x_position_valid and is_mouse_y_position_valid

    def get_board_square_position(self, mouse_position):
        """
        Chuyển đổi tọa độ của chuột trên màn hình thành tọa độ của ô trên bàn cờ
        
        :mouse_position: (x, y)
        :return: The board_square_x_position and board_square_y_position are being returned.
        """
        mouse_x_position, mouse_y_position = mouse_position

        board_square_y_position = int((mouse_x_position - render_settings.BOARD_POS_X_MIN) / render_settings.SQUARE_SIZE)
        board_square_x_position = int((mouse_y_position - render_settings.BOARD_POS_Y_MIN) / render_settings.SQUARE_SIZE)
        return (board_square_x_position, board_square_y_position)
    
    def clear(self):
        """
        Xóa màn hình
        """
        bg = pygame.image.load('Asset/bg.jpg')
        bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))

        blur_surface = pygame.Surface((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        blur_surface.set_alpha(150)  # Đặt độ trong suốt
        blur_surface.fill((255, 255, 255))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(blur_surface, (0, 0))
        pygame.display.update()

    def handle_human_move(self, state: State):
        """
        Lấy vị trí nhấp chuột của người chơi và kiểm tra xem đó có phải là một nước đi hợp lệ hay không. Nếu đúng, nó sẽ cập nhật trạng thái lên bàn cờ
        
        state: State
        type state: State
        return: vị trí mà người chơi nhấn vào
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        # mouse left click
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            if self.is_new_move_valid(mouse_position, state):
                human_move = self.get_board_square_position(mouse_position)

                # Announcement
                print("HUMAN move: (row:", human_move[0], ", column:", human_move[1], ").")
                
                state.update_move(game_settings.HUMAN, human_move)
                return
        return
                    


class Button:
    def __init__(self, screen, pos, text_input, font, base_color, hovering_color, size):
        self.screen = screen
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.x_size = size[0]
        self.y_size = size[1]
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = pygame.draw.rect(self.screen, (225, 225, 225), ((self.x_pos-(self.x_size//2), self.y_pos-(self.y_size//2 -1)), (self.x_size, self.y_size)),1,20)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


from pygame.locals import *

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.font = pygame.font.Font(None, 40)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color_inactive)
        self.active = False

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)

        self.bg = pygame.image.load('Asset/bg.jpg')
        self.bg = pygame.transform.scale(self.bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        
    def handle_event(self, event):
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    return self.text
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                self.txt_surface = self.font.render(self.text, True, self.color_active)

        color = self.color_active if self.active else self.color_inactive
        self.screen.blit(self.bg, (0, 0))
        pygame.draw.rect(self.screen, color, self.rect, 2)
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(self.screen, color, self.rect, 2)
        pygame.display.update()  # Update the display

    def activate(self):
        self.active = True
        self.txt_surface = self.font.render(self.text, True, self.color_active)

    def deactivate(self):
        self.active = False
        self.txt_surface = self.font.render(self.text, True, self.color_inactive)

    def draw_label(self):
        font = pygame.font.Font('Asset/Huggo-3zdZG.otf', 40)
        label = font.render("Enter your name", True, (255, 255, 255))
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.top - 40))
        self.screen.blit(label, label_rect)

    def get_player_name():
        clock = pygame.time.Clock()
        input_box = InputBox(render_settings.WINDOW_WIDTH//2-125, render_settings.WINDOW_HEIGHT//2, 250, 40)

        input_boxes = [input_box]
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                    sys.exit()
                for box in input_boxes:
                    if event.type == MOUSEBUTTONDOWN:
                        if box.rect.collidepoint(event.pos):
                            box.activate()
                        else:
                            box.deactivate()
                    if event.type == KEYDOWN:
                        if box.active:
                            if event.key == K_RETURN:
                                return box.text
                            box.handle_event(event)

            for box in input_boxes:
                box.handle_event(pygame.event.Event(0)) # Update text surface

            input_box.draw_label()
            pygame.display.flip()
            pygame.display.update()
            clock.tick(30)