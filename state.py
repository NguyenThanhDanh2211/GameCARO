from copy import deepcopy
from math import inf as infinity
import numpy as np


import Settings.ai_settings as ai_settings
import Settings.game_settings as game_settings
import Settings.render_settings as render_settings

class State:
    def __init__(self):
        self.moves = []
        self.board = deepcopy(game_settings.EMPTY_BOARD)
        self.current_turn = game_settings.FIRST_TURN_HUMAN

    def update_move(self, last_turn, move_position):
        """
        Cập nhật trạng thái bàn cờ với nước đi trước, nước đi hiện tại của người chơi hay máy tính

        last_turn: nước đi trước của người chơi
        move_position: vị trí của nước đi vừa thực hiện
        """
        r, c = move_position
        self.moves.append(move_position)
        self.board[r][c] = last_turn

        if(last_turn == game_settings.COM):
            self.current_turn = game_settings.HUMAN
        else: self.current_turn = game_settings.COM
    
        
    def game_over(board):
        """
        Kiểm tra xem có giống mẫu không

        board: trạng thái hiện tại của bàn cờ
        return: người chiến thắng trò chơi
        """
        value_lines = State.split_board_to_array(board)
        score_X = 0
        score_O = 0
        for value_line in value_lines:
            pattern_length = 5
            if(len(value_line) >= pattern_length):
                for i in range(0, len(value_line) - pattern_length +1):
                    temp_line = [
                        value_line[i],
                        value_line[i+1],
                        value_line[i+2],
                        value_line[i+3],
                        value_line[i+4]
                    ]
                    # HUMAN win
                    if(temp_line == ai_settings.O_ENDGAME_PATTERN):
                        score_O = score_O + 1
                        return game_settings.O
                    
                    # COM win
                    if(temp_line == ai_settings.X_ENDGAME_PATTERN):
                        score_X = score_X + 1
                        return game_settings.X
                    
        return game_settings.EMPTY
    
    def split_board_to_array(board_state):
        """
        Chuyển mảng 2 chiều thành mảng 1 chiều

        board_state: mảng 2 chiều của bàn cờ hiện tại
        return: danh sách các mảng 1 chiều
        """
        res_arrays = []
        # /
        diagonal_count = range(-(game_settings.BOARD_ROW_COUNT-1), game_settings.BOARD_COL_COUNT, 1)
        for d in diagonal_count:
            res_arrays.append( [ row[r+d] for r,row in enumerate(board_state) if 0 <= r+d < len(row)] )
        
        # \
        for d in diagonal_count:
            res_arrays.append( [ row[~(r+d)] for r,row in enumerate(board_state) if 0 <= r+d < len(row)] )

        # rows
        for row in board_state:
            res_arrays.append(deepcopy(row))

        # columns
        for c in range(0, game_settings.BOARD_COL_COUNT):
            temp_column = []
            for r in range(0, game_settings.BOARD_ROW_COUNT):
                temp_column.append(board_state[r][c])
            res_arrays.append(temp_column)
        
        return res_arrays
        
    def is_valid_move(move_position, board):
        """
        Kiếm tra xem nước đi có hợp lệ hay không

        move_position: vị trí của nước đi
        board: bàn cờ người chơi đang chơi
        """
        move_r, move_c = move_position
        is_r_valid = (0 <= move_r < game_settings.BOARD_ROW_COUNT)
        is_c_valid = (0 <= move_c < game_settings.BOARD_COL_COUNT)
        return is_c_valid and is_r_valid

    def generate_possible_moves(board, expansion_range):
        """
        Trả về danh sách các nước đi có thể dựa trên trạng thái mở rộng của bàn cờ và phạm vi mở rộng của các quân cờ lân cận

        board: trạng thái hiện tại của bàn cờ
        """
        possible_moves = []
        if np.array_equal(board, game_settings.EMPTY_BOARD):
            for r in range(0, game_settings.BOARD_ROW_COUNT):
                for c in range(0, game_settings.BOARD_COL_COUNT):
                    possible_moves.append((r, c))
        else:
            for r in range(0, game_settings.BOARD_ROW_COUNT):
                for c in range(0, game_settings.BOARD_COL_COUNT):
                    temp_move = board[r][c]
                    if temp_move == game_settings.EMPTY and State.has_neighbor((r, c), board, expansion_range):
                        possible_moves.append((r, c))
        return possible_moves
    
    def has_neighbor(move_position, board, expansion_range):
        """
        Kiểm tra xem một vị trí trong bàn cờ có lân cận với một vị trí của nước đi trước trong một phạm vi nhất định không
        
        move_position: vị trí muốn kiếm tra
        board: trạng thái hiện tại của bàn cờ
        expansion_range: số hàng và cột muốn mở rộng từ vị trí muốn kiếm tra
        """
        move_r, move_c = move_position
        r_radius = expansion_range
        c_radius = expansion_range

        for r in range(-r_radius, r_radius + 1):
            for c in range(-c_radius, c_radius + 1):
                neighbor_c = move_c + c
                neighbor_r = move_r + r
                neighbor_position = (neighbor_r, neighbor_c)
                neighbor = 0

                if(State.is_valid_move(neighbor_position, board)):
                    neighbor = board[neighbor_r][neighbor_c]
                
                if(neighbor != game_settings.EMPTY):
                    return True
        return False
    
    def high_impact_move(board, current_turn):
        """
        Lấy trạng thái bàn cờ và người chơi chơi hiện tại, rồi trả lại nước đi có tác động lớn nhất lên bàn cờ và điểm của nước đi đó
        
        board: trạng thái hiện tại của bàn cờ
        current_turn: nước đi hiện tại của người chơi
        return: Một cặp gồm nước đi có điểm cao nhất và điểm cao nhất. 
        Return (None, 0) nếu điểm của nước đi điểm có tác động cao nhất không đạt được HIGH_IMPACT_MOVE_THRESHOLD.
        """
        temp_board = deepcopy(board)
        board_O_score, board_X_score = State.evaluate(board)
        highest_score = 0
        highest_score_move = None
        for r in range(0, game_settings.BOARD_ROW_COUNT):
            for c in range(0, game_settings.BOARD_COL_COUNT):
                if(temp_board[r][c] == game_settings.EMPTY):
                    temp_board[r][c] = current_turn
                    temp_board_O_score, temp_board_X_score = State.evaluate(temp_board)
                    score = 0
                    if(current_turn == game_settings.O):
                        score = temp_board_O_score - board_O_score
                    elif(current_turn == game_settings.X):
                        score = temp_board_X_score - board_X_score
                    
                    if(score > highest_score):
                        highest_score = score
                        highest_score_move = (r, c)
                    
                    temp_board[r][c] = game_settings.EMPTY
        
        if (highest_score >= ai_settings.HIGH_IMPACT_MOVE_THRESHOLD):
            return (highest_score_move, highest_score)
        else:
            return (None, 0)


    def get_direction_pattern_tuples(board, move, streak, current_turn):
        """
        Lấy trạng thái bàn cờ, một nước đi, streak và nước đi hiện tại. Trả về danh sách các quân cờ theo hướng di chuyển
        
        board: trạng thái hiện tại của bàn cờ 
        move: nước đi đang được đánh giá
        streak: số quân cờ liên tiếp để dành chiến thắng
        current_turn: người chơi hiện tại
        return: danh sách các patterns.
        """
        if not State.is_valid_move(move, board):
            return []
        # streak = number of unblocked pieces
        move_r, move_c = move
        # r ~ x
        # c ~ y
        direction_patterns = []
        # horizontal
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('H', pattern))

        # vertical
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('V', pattern))

        # diagonals
        # lower-left to upper-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r + i, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('D1', pattern))
        # upper-left to lower-right
        pattern = []
        for i in range(-streak, streak + 1):
            if(i == 0):
                temp_move = move
                pattern.append(current_turn)
            else:
                temp_move = (move_r - i, move_c + i)
                if(State.is_valid_move(temp_move, board)):
                    temp_move_r, temp_move_c = temp_move
                    pattern.append(board[temp_move_r][temp_move_c])
        if(len(pattern) > streak + 2):
            direction_patterns.append(('D2', pattern))

        return direction_patterns
    
    def evaluate(board):
        """
        Lấy bàn cờ và trả về một cặp điểm cho mỗi người chơi

        board: bàn cờ để đánh giá
        return: điểm của bàn cờ (O_score, X_score).
        """
        O_score = 0
        X_score = 0

        lines = State.split_board_to_array(board)

        for line in lines:
            line_O_score, line_X_score = State.evaluate_line(line)
            O_score += line_O_score
            X_score += line_X_score

        return (O_score, X_score)
    
    # return(O_score, X_score)
    def evaluate_line(line):
        """
        Lấy dòng trên bàn cờ và trả về điểm của X O trên dòng
        
        :line: danh sách các hàng, cột, đường chéo
        :return: điểm X O trên dòng
        """
        O_score = 0
        X_score = 0

        # check 6 patterns 
        pattern_length = 6
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4],
                    line[i+5]
                ]
                # O score
                for p, pattern in enumerate(ai_settings.O_6_PATTERNS):
                    if(temp_line == pattern):
                        O_score += ai_settings.O_5_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_6_PATTERNS):
                    if(temp_line == pattern):
                        X_score += ai_settings.X_5_PATTERNS_SCORES[p]

        # check 5 patterns
        pattern_length = 5
        if(len(line) >= pattern_length):
            for i in range(0, len(line) - pattern_length + 1):
                temp_line = [
                    line[i],
                    line[i+1],
                    line[i+2],
                    line[i+3],
                    line[i+4]
                ]
                # O score
                for p, pattern in enumerate(ai_settings.O_5_PATTERNS):
                    if(temp_line == pattern):
                        O_score += ai_settings.O_5_PATTERNS_SCORES[p]

                # X score
                for p, pattern in enumerate(ai_settings.X_5_PATTERNS):
                    if(temp_line == pattern):
                        X_score += ai_settings.X_5_PATTERNS_SCORES[p]
        return(O_score, X_score)

    def checkmate(board, current_turn):
        """
        Kiểm tra xem có phải là 5 quân cùng loại liên tiếp hay không
        
        board: trạng thái bàn cờ hiện tại
        current_turn: nước đi vừa thực hiện
        return: hàng và cột của nước đi thắng
        """
        # checkmate = a continuous-five
        # continuous-five
        # streak = 5 - 1 # 4 co the bi block
        
        possible_moves = State.generate_possible_moves(board, 1)
        check_mate_moves = []

        for move in possible_moves:
            temp_board = deepcopy(board)
            temp_board[move[0]][move[1]] = current_turn
            if State.game_over(temp_board):
                check_mate_moves.append(move)
                
        if(len(check_mate_moves) > 0):
            score = -infinity
            best_move = None
            for move in check_mate_moves:
                temp_board = deepcopy(board)
                temp_board[move[0]][move[1]] = current_turn
                O_score, X_score = State.evaluate(board)
                temp_score = 0
                if(current_turn == game_settings.O):
                    temp_score = O_score - X_score
                else:
                    temp_score = X_score - O_score
                if(temp_score > score):
                    score = temp_score
                    best_move = move
            return best_move

        else:
            return None
        
    def combo_move(board, current_turn):
        """
        combo_move được thiết kế để kiểm tra xem có một nước đi nào đó có thể tạo ra một tình huống combo đặc biệt trên bảng cờ hay không.
        """
        # khởi tạo các biến 
        blocked_four_patterns = [] # Danh sách các pattern chứa 4 nước đi của người chơi hiện tại, một ô trống và không bị chặn ở một đầu (blocked-four)
        blocked_four_pattern_length = 5 # độ dài blocked-four
        matched_blocked_four_pattern_move_direction_list = [] #Danh sách các tuples chứa hướng và nước đi, tương ứng với những nước đi có thể tạo ra một blocked-four.
        move_direction_dictionary = dict() # Một từ điển chứa thông tin về hướng và pattern của các nước đi đã kiểm tra.

        # Thêm Phần Tử vào blocked_four_patterns
        if(current_turn == game_settings.X):
            for pattern in ai_settings.X_5_PATTERNS:
                if(pattern.count(game_settings.X) == 4):
                    blocked_four_patterns.append(pattern)
        elif(current_turn == game_settings.O):
            for pattern in ai_settings.O_5_PATTERNS:
                if(pattern.count(game_settings.O) == 4):
                    blocked_four_patterns.append(pattern)

        # kiểm tra từng hướng đi của nước đi
        possible_moves = State.generate_possible_moves(board, 2)
        for p_m_move in possible_moves:
            move_direction_set = set() #  lưu trữ các hướng đã kiểm tra.
            matched_direction_count = 0 # Đếm số hướng đã kiểm tra khớp với blocked-four.

            direction_pattern_tuples = State.get_direction_pattern_tuples(board, p_m_move, 4, current_turn) # streak = 4 vì pattern đang xét có độ dài bằng 5
            if(len(direction_pattern_tuples) > 0) :
                for tuple in direction_pattern_tuples:
                    direction, pattern = tuple
                    for i in range(0, len(pattern) - blocked_four_pattern_length + 1):
                        checking_pattern = [
                            pattern[i],
                            pattern[i+1],
                            pattern[i+2],
                            pattern[i+3],
                            pattern[i+4],
                        ]
                        has_pattern_in_this_direction = False
                        for blocked_four_pattern in blocked_four_patterns:
                            if(checking_pattern == blocked_four_pattern):
                                has_pattern_in_this_direction = True
                                move_direction_dictionary[p_m_move] = (direction, checking_pattern)
                                
                        if has_pattern_in_this_direction:
                            matched_blocked_four_pattern_move_direction_list.append((direction, p_m_move))
                            if (direction, p_m_move) not in move_direction_set:
                                move_direction_set.add((direction, p_m_move))
                                matched_direction_count += 1
                                if matched_direction_count > 1: # cần tạo ít nhất 2 locked fours -> a combo 
                                    return p_m_move  