from sys import exit
import pygame
from pygame.locals import *
from state import State
from GUI.game_render import GameRender
from GUI.game_render import InputBox
from abpruning import ABPruning
import Settings.game_settings as game_settings
import Settings.ai_settings as ai_settings
import Settings.render_settings as render_settings
import time
import pymongo
import numpy as np

# Kết nối đến MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["game_database"]
hard_collection = db["hard_games"]
final_scores_collection_hard = db["final_scores_hard"]

class PlaywAI:
    def __init__(self):
        self.current_match = State()
        self.render = GameRender(self.current_match)
        self.ai = ABPruning(self.current_match)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_player = game_settings.FIRST_TURN_HUMAN
        self.saved_state = None
        self.player_name = None

    def get_player_name(self):
        self.player_name = InputBox.get_player_name()

    def save_game_state(self, current_round, human_score, com_score):
        game_state = {
            "player_name": self.player_name,
            "current_round": current_round,
            "human_score": human_score,
            "com_score": com_score,
            "board_state": [[int(cell) for cell in row] for row in self.current_match.board] # Chuyển đổi thành mảng 2D để lưu vào MongoDB

        }
        # Kiểm tra xem thông tin của người chơi đã tồn tại hay chưa
        existing_state = hard_collection.find_one({"player_name": self.player_name})
        if existing_state:
            # Nếu đã tồn tại, cập nhật thông tin
            hard_collection.update_one({"player_name": self.player_name}, {"$set": game_state})
        else:
            # Nếu chưa tồn tại, tạo mới thông tin
            hard_collection.insert_one(game_state)
        
    def count_round_completed(self, current_round, human_score, com_score):
        if current_round > 5:
            final_scores = final_scores_collection_hard.find_one({"player_name": self.player_name})
            
            if final_scores:
                human_score += int(final_scores["human_score"])
                com_score += int(final_scores["com_score"])
                completed_rounds += int(final_scores["completed_rounds"])
            else:
                completed_rounds = 1
            final_scores_hard = {
                "player_name": self.player_name,
                "human_score": human_score,
                "com_score": com_score,
                "completed_rounds": completed_rounds,
            }
            final_scores_collection_hard.update_one({"player_name": self.player_name}, {"$set": final_scores_hard}, upsert=True)

    def load_game_state(self):
        game_state = hard_collection.find_one({"player_name": self.player_name})
        if game_state is not None:
            self.player_name = game_state["player_name"]
            current_round = game_state["current_round"]
            human_score = game_state["human_score"]
            com_score = game_state["com_score"]
            self.current_match.board = np.array(game_state["board_state"])
            return self.player_name, current_round, human_score, com_score
        return None


    def loop(self):
        self.get_player_name()  # Nhập tên người chơi

        rounds = 5  # Số lượt chơi
        current_round = 1  # Đếm lượt chơi
        human_score = 0
        com_score = 0
        wait_time = 3

        while self.running and current_round <= rounds:
           
            self.clock.tick(render_settings.FPS)
            pygame.display.update()

            # DRAW
            if (len(self.current_match.moves) == game_settings.MAX_MOVE_COUNT):
                self.render.render_state(self.current_match.board, game_settings.NO_ONE, game_settings.NO_ONE, self.current_match.moves[-1], current_round, human_score, com_score)

                self.save_game_state(current_round, human_score, com_score)  # Lưu trạng thái

                continue
            # AI move first
            if current_round % 2 != 0:
                if (game_settings.FIRST_TURN_COM == game_settings.COM and len(self.current_match.moves) == 0):

                    # Announcement
                    print("AI is calculating next move...")
                    print("---------------------------------")

                    AI_calulation_time = -pygame.time.get_ticks()
                    ai_move = self.ai.next_move()
                    AI_calulation_time += pygame.time.get_ticks()

                    # Announcement
                    print("---------------------------------")
                    print("AI calculation time: ", AI_calulation_time / 1000, " seconds (depth = ", ai_settings.MAX_TREE_DEPTH_LEVEL, ").")

                    self.render.handle_com_move(ai_move, self.current_match)
                    self.render.render_state(self.current_match.board, self.current_match.current_turn, State.game_over(self.current_match.board), self.current_match.moves[-1], current_round, human_score, com_score)
            #
            # HUMAN move first
            #

            for event in pygame.event.get():
                # exit
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (self.render.is_new_game_button_pressed()):
                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        current_round = 1  # Đếm lượt chơi
                        human_score = 0
                        com_score = 0
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round, human_score, com_score)
                        break

                    if (self.render.is_home_button_pressed()):
                        self.save_game_state(current_round, human_score, com_score)  # Lưu trạng thái
                        self.running = False
                        break
                    if self.render.is_continue_button_pressed():
                        load_result = self.load_game_state()  # Tải lại trạng thái đã lưu
                        if load_result is not None:
                            player_name, current_round, human_score, com_score = load_result
                            self.player_name = player_name
                            self.render.render_state(self.current_match.board, self.current_match.current_turn, State.game_over(self.current_match.board), self.current_match.moves[-1], current_round, human_score, com_score)
                        continue  # Chuyển qua vòng lặp tiếp theo

                    # HUMAN turn
                    if (self.current_match.current_turn == game_settings.HUMAN):

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

                        self.render.check_winner_final(current_round, human_score, com_score, rounds)
                        self.count_round_completed(current_round, human_score, com_score)
                        
                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round, human_score, com_score)

                    # AI turn
                    if (self.current_match.current_turn == game_settings.COM):

                        AI_calulation_time = -pygame.time.get_ticks()

                        # Announcement
                        print("AI is calculating next move...")
                        print("---------------------------------")

                        # ai_move = self.ai.random_move(self.current_match, 1)  # => ramdom move nè
                        ai_move = self.ai.next_move() # => next move

                        AI_calulation_time += pygame.time.get_ticks()

                        # Announcement
                        print("---------------------------------")
                        print("AI calculation time: ", AI_calulation_time / 1000, " seconds.")

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

                        self.render.check_winner_final(current_round, human_score, com_score, rounds)
                        self.count_round_completed(current_round, human_score, com_score)

                        self.current_match = State()
                        self.ai = ABPruning(self.current_match)
                        self.render.render_state(self.current_match.board, game_settings.FIRST_TURN_HUMAN, False, (-1, -1), current_round, human_score, com_score)

            pygame.display.update()



# PlaywAI().loop()