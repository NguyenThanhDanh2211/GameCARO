import pygame
import sys

from state import State
import Settings.render_settings as render_settings
import Settings.game_settings as game_settings
from GUI.game_render import Button

class playwFriend:
    def __init__(self, state: State) -> None:
        self.state = State()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)
        self.running = True
        self.current_round = 1
        self.human1_score = 0
        self.human2_score = 0

        # self.screen.fill(render_settings.BOARD_COLOR) => đây

        bg = pygame.image.load('Asset/bg.jpg')
        bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))

        blur_surface = pygame.Surface((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        blur_surface.set_alpha(150)  # Đặt độ trong suốt
        blur_surface.fill((255, 255, 255))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(blur_surface, (0, 0))
        # # pygame.display.update()

        if (len(state.moves) > 0):
            self.render_state(state.board, game_settings.FIRST_TURN_HUMAN, False, state.moves[-1], self.current_round, self.human2_score, self.human1_score)
        else:
            self.render_state(state.board, game_settings.FIRST_TURN_HUMAN, False, (-1,-1), self.current_round, self.human2_score, self.human1_score)
        pygame.display.update()

       
    def render_state(self, board, current_turn, player_win,last_move, current_round, human1_score, human2_score):
    
        """
        It renders board state and displays that board state
        
        :param board: the current state of the board
        :param current_turn: The current turn of the game
        :param player_win: The player who won the game
        :return: The return value of the function is the value of the last expression evaluated.
        """
        
        self.clear()
        
        # human1 WIN
        if(player_win == game_settings.COM): #X
            self.draw_board(board, render_settings.X_WIN_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(player_win), current_round, human1_score, human2_score)
            return
        # HUMAN2 WIN
        if(player_win == game_settings.HUMAN): #O
            self.draw_board(board, render_settings.O_WIN_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(player_win), current_round, human1_score, human2_score)
            return
        if(player_win == game_settings.NO_ONE):
            last_turn = game_settings.get_opponent(current_turn)
            # DRAW
            if(current_turn == game_settings.NO_ONE):
                self.draw_board(board, render_settings.DRAW_INFO_TEXT, render_settings.COLOR_WIN, last_move, render_settings.get_last_move_color(last_turn), current_round, human1_score, human2_score)
                return
            # GAME IS NOT OVER YET. HUMAN1 TURN
            if(current_turn == game_settings.HUMAN):
                self.draw_board(board, render_settings.O_TURN_INFO_TEXT, render_settings.COLOR_BLUE, last_move, render_settings.get_last_move_color(last_turn), current_round, human1_score, human2_score)
                return
            # GAME IS NOT OVER YET. COM TURN
            if(current_turn == game_settings.COM):
                self.draw_board(board, render_settings.X_TURN_INFO_TEXT, render_settings.COLOR_RED, last_move, render_settings.get_last_move_color(last_turn), current_round, human1_score, human2_score)
                return

    def draw_X(self, x, y, color):
        """
        Draw an X on the screen at the given coordinates
        
        :param x: the x coordinate of the cell
        :param y: 0-2
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
        Draw a circle with a radius of O_RADIUS - O_CELL_BORDER at the center of the square at position
        (x,y) on the board.
        
        :param x: the x coordinate of the board
        :param y: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29,
        """
        posX = render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE/2 + y * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2
        posY = render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE/2 + x * render_settings.SQUARE_SIZE + render_settings.O_LINE_THICKNESS/2
        # subtract cell border
        radius = render_settings.O_RADIUS - render_settings.O_CELL_BORDER
        # draw circle
        pygame.draw.circle(self.screen, color, [posX, posY], radius , render_settings.O_LINE_THICKNESS)
    
    def render_winner(self, winner_text, human2_score, human1_score):
        self.clear()

        font = pygame.font.Font('Asset/Rekilash-PKBxZ.otf', 100)
        winner_surface = font.render(winner_text, True, render_settings.COLOR_WIN)
        winner_rect = winner_surface.get_rect(center=(render_settings.WINDOW_WIDTH // 2, render_settings.WINDOW_HEIGHT // 2 -70))

        human2_score_text = font.render(f"{human2_score}", True, render_settings.COLOR_BLUE)
        human1_score_text = font.render(f"{human1_score}", True, render_settings.COLOR_RED)
        haicham = font.render(f":", True, render_settings.COLOR_WHITE)

        human2_score_rect = human2_score_text.get_rect(center=(render_settings.WINDOW_WIDTH // 2 -50, winner_rect.bottom + 50))
        haicham_rect = haicham.get_rect(center=(render_settings.WINDOW_WIDTH // 2, winner_rect.bottom + 50))
        human1_score_rect = human1_score_text.get_rect(center=(render_settings.WINDOW_WIDTH // 2 +50, winner_rect.bottom + 50))

        self.screen.blit(winner_surface, winner_rect)
        self.screen.blit(human2_score_text, human2_score_rect)
        self.screen.blit(haicham, haicham_rect)
        self.screen.blit(human1_score_text, human1_score_rect)

        pygame.display.update()
    
    def check_winner_final(self, current_round, human2_score, human1_score, rounds):
        if current_round > rounds:
            winner_text = ""
            if human2_score > human1_score:
                winner_text = f"Human O win!"
            elif human2_score < human1_score:
                winner_text = f"Human X win!"

            self.render_winner(winner_text, human1_score, human2_score)

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
        It draws text to the screen
        
        :param text: the text to be displayed
        :param textColor: (255, 255, 255)
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
    
    def draw_scores(self, human2_score, human1_score):
        font = pygame.font.Font('Asset/Rekilash-PKBxZ.otf', 50)
        human2_score_text = font.render(f"{human2_score}", True, render_settings.COLOR_BLUE)
        human1_score_text = font.render(f"{human1_score}", True, render_settings.COLOR_RED)
        haicham = font.render(f":", True, render_settings.COLOR_WHITE)

        human2_score_rect = human2_score_text.get_rect(center=(render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5)-15,180+render_settings.BORDER_SIZE + 30/2))
        human1_score_rect = human1_score_text.get_rect(center=(render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5)+50,180+render_settings.BORDER_SIZE + 30/2))
        haicham_rect = haicham.get_rect(center=((render_settings.WINDOW_WIDTH-(render_settings.WINDOW_WIDTH // 5) +17), 180+render_settings.BORDER_SIZE + 30/2))

        self.screen.blit(human2_score_text, human2_score_rect)
        self.screen.blit(haicham, haicham_rect)
        self.screen.blit(human1_score_text, human1_score_rect)
        
    def is_new_game_button_pressed(self):
        """
        If the mouse button is pressed, and the mouse is in the button area, return True. Otherwise,
        return False
        :return: The return value is a boolean.
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
        If the mouse button is pressed, and the mouse is in the button area, return True. Otherwise,
        return False
        :return: The return value is a boolean.
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
        If the mouse button is pressed, and the mouse is in the button area, return True. Otherwise,
        return False
        :return: The return value is a boolean.
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            mouse_x_position, mouse_y_position = mouse_position
            is_in_x_button_area = render_settings.CONTINUE_BUTTON_POS_X_MIN < mouse_x_position < render_settings.CONTINUE_BUTTON_POS_X_MAX
            is_in_y_button_area = render_settings.CONTINUE_BUTTON_POS_Y_MIN < mouse_y_position < render_settings.CONTINUE_BUTTON_POS_Y_MAX
            return is_in_x_button_area and is_in_y_button_area
        return False 


    def draw_board(self, board_state, info_text, info_text_color, last_move, last_move_color, current_round, human2_score, human1_score):
        """
        It draws the board, the info text, the new game button, and the moves on the board.
        
        :param board_state: the current state of the board
        :param infoText: The text to be displayed on the screen
        :param infoTextColor: The color of the text
        """
        # draw board
        # draw vertical line
        for r in range (0, game_settings.BOARD_COL_COUNT + 1):
            
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK, 
            [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN], [render_settings.BOARD_POS_X_MIN + render_settings.SQUARE_SIZE * r, render_settings.BOARD_POS_Y_MIN + render_settings.BOARD_HEIGHT], render_settings.BOARD_LINE_WIDTH)
        # draw horizontal line
        for r in range (0, game_settings.BOARD_ROW_COUNT + 1):
            pygame.draw.line(self.screen, render_settings.COLOR_BLACK,
            [render_settings.BOARD_POS_X_MIN, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], [render_settings.BOARD_POS_X_MIN + render_settings.BOARD_WIDTH, render_settings.BOARD_POS_Y_MIN + render_settings.SQUARE_SIZE * r], render_settings.BOARD_LINE_WIDTH)
        
        
        # draw INFO TEXT
        self.draw_info_text(info_text, info_text_color)

        self.draw_scores(human2_score, human1_score)
        self.draw_turn_counter(current_round)

        continue_btn = Button(screen=self.screen, pos=(630, 490), text_input='Continue', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        continue_btn.update()
        newgame = Button(screen=self.screen, pos=(770, 490), text_input='New game', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        newgame.update()
        home = Button(screen=self.screen, pos=(700, 540), text_input='Home', font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 25), base_color=render_settings.COLOR_BLACK, hovering_color=render_settings.COLOR_BLUE, size=(120, 30))
        home.update()
   
        # render board moves
        # last_move_r, last_move_c = last_move
        if last_move:
            last_move_r, last_move_c = last_move
        else:
            # Provide default values or handle the case where last_move is None
            last_move_r, last_move_c = -1, -1  # Adjust the default values accordingly

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
      
    def is_new_move_valid(self, mouse_position, state: State):
        """
        If the mouse position is in the board area, and the selected square is empty, then the move is
        valid
        
        :param mouse_position: The position of the mouse on the screen
        :param state: State
        :type state: State
        :return: The function is_new_move_valid() returns a boolean value.
        """
        if (self.is_mouse_position_in_board_area(mouse_position)):
            square_x_position, square_y_position =  self.get_board_square_position(mouse_position)
            is_selected_square_empty = state.board[square_x_position][square_y_position] == game_settings.EMPTY
            return is_selected_square_empty
        else:
            return False

    def is_mouse_position_in_board_area(self, mouse_position):
        """
        It checks if the mouse position is within the board area
        
        :param mouse_position: (x, y)
        :return: The return value is a boolean.
        """
        mouse_x_position, mouse_y_position = mouse_position
        is_mouse_x_position_valid = render_settings.BOARD_POS_X_MIN < mouse_x_position < render_settings.BOARD_POS_X_MAX
        is_mouse_y_position_valid = render_settings.BOARD_POS_Y_MIN < mouse_y_position < render_settings.BOARD_POS_Y_MAX
        return is_mouse_x_position_valid and is_mouse_y_position_valid

    def get_board_square_position(self, mouse_position):
        """
        The boardsquare's x, y position is inverse to the mouse positions'.
        
        :param mouse_position: (x, y)
        :return: The board_square_x_position and board_square_y_position are being returned.
        """
        mouse_x_position, mouse_y_position = mouse_position
        #The boardsquare's x, y position is inverse to the mouse positions'. 
        board_square_y_position = int((mouse_x_position - render_settings.BOARD_POS_X_MIN) / render_settings.SQUARE_SIZE)
        board_square_x_position = int((mouse_y_position - render_settings.BOARD_POS_Y_MIN) / render_settings.SQUARE_SIZE)
        return (board_square_x_position, board_square_y_position)
    
    def clear(self):
        """
        It clears the screen and updates the display
        """
        bg = pygame.image.load('Asset/bg.jpg')
        bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))

        blur_surface = pygame.Surface((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        blur_surface.set_alpha(150)  # Đặt độ trong suốt
        blur_surface.fill((255, 255, 255))

        self.screen.blit(bg, (0, 0))
        self.screen.blit(blur_surface, (0, 0))
        pygame.display.update()

    def handle_human2_move(self, state: State):
        """
        It takes human's mouse left click position and checks if it's a valid move. If it is, it updates the state with
        the move
        
        :param state: State
        :type state: State
        :return: the position of the square that the human player clicked on.
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
    
    def handle_human1_move(self, state: State):
        """
        It takes human's mouse left click position and checks if it's a valid move. If it is, it updates the state with
        the move
        
        :param state: State
        :type state: State
        :return: the position of the square that the human player clicked on.
        """
        mouse_button_pressed = pygame.mouse.get_pressed()
        # mouse left click
        if mouse_button_pressed[0]:
            mouse_position = pygame.mouse.get_pos()
            if self.is_new_move_valid(mouse_position, state):
                human_move = self.get_board_square_position(mouse_position)

                # Announcement
                print("HUMAN 1 move: (row:", human_move[0], ", column:", human_move[1], ").")
                
                state.update_move(game_settings.COM, human_move)
                return
        return

import time

class playwFriendMain:
    def __init__(self) -> None:
        self.current_match = State()
        self.render = playwFriend(self.current_match)
        self.running = True

    def loop(self):
        rounds = 5  # Số lượt chơi
        current_round = 1  # Đếm lượt chơi
        player1_score = 0
        player2_score = 0

        while self.running and current_round <= rounds:

            pygame.display.update()

            # DRAW
            if len(self.current_match.moves) == game_settings.MAX_MOVE_COUNT:
                self.render.render_state(
                    self.current_match.board, game_settings.NO_ONE, game_settings.NO_ONE,
                    self.current_match.moves[-1], current_round, player1_score, player2_score
                )

                time.sleep(3)

                current_round += 1
                self.current_match = State()
                self.render.render_state(
                    self.current_match.board, game_settings.FIRST_TURN_HUMAN, False,
                    (-1, -1), current_round, player1_score, player2_score
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.render.is_new_game_button_pressed():
                        self.current_match = State()
                        current_round = 1  # Đếm lượt chơi
                        player1_score = 0
                        player2_score = 0
                        self.render.render_state(
                            self.current_match.board, game_settings.FIRST_TURN_HUMAN, False,
                            (-1, -1), current_round, player1_score, player2_score
                        )
                        break
                    if (self.render.is_home_button_pressed()):
                        self.running = False
                        break

                    # HUMAN turn
                    if self.current_match.current_turn == game_settings.HUMAN:
                        self.render.handle_human2_move(self.current_match)
                        self.render.render_state(
                            self.current_match.board, game_settings.COM,  # Switch turn to COM
                            State.game_over(self.current_match.board), self.current_match.moves[-1],
                            current_round, player1_score, player2_score
                        )

                        # Check for a win
                        if State.game_over(self.current_match.board):
                            print("Game Over!")
                            player1_score += 1
                            current_round += 1
                            print('The next round will start in 3 seconds')
                          
                            time.sleep(3)
                            self.render.check_winner_final(current_round, player2_score, player1_score, rounds)
                            self.current_match = State()
                            self.render.render_state(
                                self.current_match.board, game_settings.FIRST_TURN_HUMAN, False,
                                (-1, -1), current_round, player1_score, player2_score
                            )

                    # COM turn
                    elif self.current_match.current_turn == game_settings.COM:
                        self.render.handle_human1_move(self.current_match)
                        self.render.render_state(
                            self.current_match.board, game_settings.HUMAN,  # Switch turn to HUMAN
                            State.game_over(self.current_match.board), self.current_match.moves[-1],
                            current_round, player1_score, player2_score
                        )

                        # Check for a win
                        if State.game_over(self.current_match.board):
                            print("Game Over!")
                            player2_score += 1
                            current_round += 1
                            print('The next round will start in 3 seconds')
                            
                            time.sleep(3)
                            self.render.check_winner_final(current_round, player2_score, player1_score, rounds)

                            
                            self.current_match = State()
                            self.render.render_state(
                                self.current_match.board, game_settings.FIRST_TURN_HUMAN, False,
                                (-1, -1), current_round, player1_score, player2_score
                            )

            pygame.display.update()