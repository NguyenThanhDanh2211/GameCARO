import pygame
import pymongo
import Settings.render_settings as render_settings
import GUI.game_render as game_render
import sys

# Kết nối đến MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["game_database"]
final_scores_collection_easy = db["final_scores_easy"]
final_scores_collection_hard = db["final_scores_hard"]

class Rank:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
        pygame.display.set_caption(render_settings.WINDOW_TITLE)
        self.running = True

    def get_all_players_info_easy(self):
        players_info_easy = final_scores_collection_easy.find({}, {"player_name": 1, "human_score": 1, "completed_rounds": 1, "_id": 0}).sort([("completed_rounds", pymongo.DESCENDING), ("human_score", pymongo.DESCENDING)]).limit(6)
        return list(players_info_easy)

    def get_all_players_info_hard(self):
        players_info_hard = final_scores_collection_hard.find({}, {"player_name": 1, "human_score": 1, "completed_rounds": 1, "_id": 0}).sort([("completed_rounds", pymongo.DESCENDING), ("human_score", pymongo.DESCENDING)]).limit(6)
        return list(players_info_hard)

    def render_rank(self):
        while self.running:
            bg = pygame.image.load('Asset/bg.jpg')
            bg = pygame.transform.scale(bg, (render_settings.WINDOW_WIDTH, render_settings.WINDOW_HEIGHT))
            self.screen.blit(bg, (0, 0))

            font_title = pygame.font.Font("Asset/Huggo-3zdZG.otf", 50)
            text = font_title.render("RANK", True, render_settings.COLOR_WHITE)
            text_rect = text.get_rect(center=(425, 75))
            self.screen.blit(text, text_rect)
            text_easy = font_title.render("EASY", True, render_settings.COLOR_WHITE)
            text_easy_rect = text_easy.get_rect(center=(render_settings.WINDOW_WIDTH // 4, 150))
            self.screen.blit(text_easy, text_easy_rect)

            text_hard = font_title.render("HARD", True, render_settings.COLOR_WHITE)
            text_hard_rect = text_hard.get_rect(center=(render_settings.WINDOW_WIDTH // 4 * 3, 150))
            self.screen.blit(text_hard, text_hard_rect)

            all_players_info_easy = self.get_all_players_info_easy()
            all_players_info_hard = self.get_all_players_info_hard()

            font = pygame.font.Font('Asset/Qlassy-axE4x.ttf', 40)

            for idx, player_info_easy in enumerate(all_players_info_easy):
                player_name_easy = player_info_easy["player_name"]
                human_score_easy = player_info_easy["human_score"]
                completed_rounds_easy = player_info_easy["completed_rounds"]

                player_info_text = f"{player_name_easy}: {human_score_easy}/{completed_rounds_easy*5}"
                player_name_surface = font.render(player_info_text, True, render_settings.COLOR_WHITE)
                player_name_rect = player_name_surface.get_rect(center=(render_settings.WINDOW_WIDTH // 4, 200 + idx * 50))

                self.screen.blit(player_name_surface, player_name_rect)

            # Draw a dividing line
            pygame.draw.line(self.screen, render_settings.COLOR_WHITE, (render_settings.WINDOW_WIDTH // 2, 125), (render_settings.WINDOW_WIDTH // 2, render_settings.WINDOW_HEIGHT - 125), 3)

            for idx, player_info_hard in enumerate(all_players_info_hard):
                player_name_hard = player_info_hard["player_name"]
                human_score_hard = player_info_hard["human_score"]
                completed_rounds_hard = player_info_hard["completed_rounds"]

                player_name_surface = font.render(f"{player_name_hard}: {human_score_hard}/{completed_rounds_hard*5}", True, render_settings.COLOR_WHITE)
                player_name_rect = player_name_surface.get_rect(center=(render_settings.WINDOW_WIDTH // 4 * 3, 200 + idx * 50))

                self.screen.blit(player_name_surface, player_name_rect)

            pygame.display.update()

            HOME_BTN = game_render.Button(screen=self.screen, pos=(425, 550), text_input='Home',font=pygame.font.Font('Asset/Qlassy-axE4x.ttf', 30),base_color=render_settings.COLOR_WHITE, hovering_color=render_settings.COLOR_BLUE, size=(100, 40))

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

            pygame.display.update()
