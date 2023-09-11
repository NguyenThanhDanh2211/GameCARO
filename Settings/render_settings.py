import Settings.game_setting as game_settings

FPS = 120

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (0, 255, 0)
COLOR_GREEN = (0, 180, 0)
COLOR_BLUE_VIOLET = (138, 43, 226)

X_COLOR = COLOR_RED
O_COLOR = COLOR_BLUE
O_LAST_MOVE_COLOR = COLOR_BLUE_VIOLET
X_LAST_MOVE_COLOR = COLOR_BLUE_VIOLET

def get_last_move_color(player):
    if(player == game_settings.O):
        return O_LAST_MOVE_COLOR
    if(player == game_settings.X):
        return X_LAST_MOVE_COLOR
    
BORDER_SIZE = 30


