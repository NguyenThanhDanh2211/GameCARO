from sys import exit
import pygame
from pygame.locals import *
from state import State
from GUI.game_render import GameRender
from abpruning import ABPruning
import Settings.game_settings as game_settings
import Settings.ai_settings as ai_settings
import Settings.render_settings as render_settings
import time
import sys

class PlaywAI:
    def __init__(self) -> None:
        
        self.current_match = State()
        self.render = GameRender(self.current_match)
        self.ai = ABPruning(self.current_match)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_player = game_settings.FIRST_TURN_HUMAN
        
    def loop(self):
        rounds = 5  # Số lượt chơi
        current_round = 1  # Đếm lượt chơi
        human_score = 0
        com_score = 0
        wait_time = 3

        while self.running and current_round <= rounds:

             # Hiển thị số lượt chơi và điểm số
            self.render.draw_turn_counter(current_round)
            self.clock.tick(render_settings.FPS)
            pygame.display.update()

            # DRAW
            if (len(self.current_match.moves) == game_settings.MAX_MOVE_COUNT):
                self.render.render_state(self.current_match.board, game_settings.NO_ONE, game_settings.NO_ONE, self.current_match.moves[-1], current_round, human_score, com_score)
                continue
            # AI move first
            if current_round % 2 != 0:
                if(game_settings.FIRST_TURN_COM == game_settings.COM and len(self.current_match.moves) == 0):
                
                    # Announcement
                    print("AI is calculating next move...")
                    print("---------------------------------")

                    AI_calulation_time = -pygame.time.get_ticks()
                    ai_move = self.ai.next_move()
                    AI_calulation_time += pygame.time.get_ticks()
                    
                    # Announcement
                    print("---------------------------------")
                    print("AI calculation time: ", AI_calulation_time/1000 ," seconds (depth = ", ai_settings.MAX_TREE_DEPTH_LEVEL, ").")
                    
                    self.render.handle_com_move(ai_move, self.current_match)
                    self.render.render_state(self.current_match.board, self.current_match.current_turn, State.game_over(self.current_match.board), self.current_match.moves[-1], current_round, human_score, com_score)
            #
            # HUMAN move first
            #         
            
            for event in pygame.event.get():
                #exit
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if(self.render.is_new_game_button_pressed()):
                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        current_round = 1  # Đếm lượt chơi
                        human_score = 0
                        com_score = 0
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round, human_score, com_score)
                        break
                        
                    if(self.render.is_home_button_pressed()):
                        self.running = False
                        break
                    
                    # HUMAN turn
                    if(self.current_match.current_turn == game_settings.HUMAN):

                        self.render.handle_human_move(self.current_match) 
                        self.render.render_state(self.current_match.board, self.current_match.current_turn, State.game_over(self.current_match.board), self.current_match.moves[-1], current_round, human_score, com_score)
                        self.ai.state.board = self.current_match.board

                    if State.game_over(self.current_match.board):
                        
                        # Announcement
                        print("Game Over!")
                        current_round += 1
                        human_score += 1
                        print('The next round will start in 3 seconds')
                        time.sleep(wait_time)
                                               
                        if current_round > rounds:
                            winner_text = ""
                            if human_score > com_score:
                                winner_text = f"Human win!"
                            elif human_score < com_score:
                                winner_text = f"AI win!"
                          
                            self.render.render_winner(winner_text, human_score, com_score)
                           
                            # Chờ người dùng nhấn phím bất kỳ để thoát
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

                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round , human_score, com_score)

                    # AI turn
                    if(self.current_match.current_turn == game_settings.COM):
                        
                        AI_calulation_time = -pygame.time.get_ticks()

                        # Announcement
                        print("AI is calculating next move...")
                        print("---------------------------------")

                        ai_move = self.ai.next_move() #=> đây
                        AI_calulation_time += pygame.time.get_ticks()
                        
                        # Announcement
                        print("---------------------------------")
                        print("AI calculation time: ", AI_calulation_time/1000 ," seconds.")
                        
                        self.render.handle_com_move(ai_move, self.current_match)
                        self.render.render_state(self.current_match.board, self.current_match.current_turn, State.game_over(self.current_match.board), self.current_match.moves[-1], current_round, human_score, com_score)

                        # Announcement
                        print("Waiting for HUMAN's move...")

                    if State.game_over(self.current_match.board):
                        
                        # Announcement
                        print("Game Over!")
                        current_round += 1
                        com_score += 1
                        print('The next round will start in 3 seconds')
                        time.sleep(wait_time)
                        
                        if current_round > rounds:
                            # Display the winner
                            winner_text = ""
                            if human_score > com_score:
                                winner_text = f"Human win!"
                            elif human_score < com_score:
                                winner_text = f"AI win!"

                            self.render.render_winner(winner_text, human_score, com_score)

                            # Chờ người dùng nhấn phím bất kỳ để thoát
                            waiting = True
                            while waiting:
                                pygame.event.pump()  # Cập nhật trạng thái sự kiện
                                for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                                        waiting = False
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()

                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round, human_score, com_score)

            pygame.display.update()
