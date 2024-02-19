import random
from math import inf as infinity
from state import State
import Settings.game_settings as game_settings
import Settings.ai_settings as ai_settings
from minimaxnode import MinimaxNode
import numpy as np

class ABPruning:
    def __init__(self, __state: State) -> None:
        self.state = __state

    def next_move(self):
        """
        Hàm này sẽ kiểm tra xem trạng thái hiện tại có phải là bước đi đầu tiên hay không. Nếu có, nó sẽ trả về một bước di chuyển ngẫu nhiên. Nếu không, nó sẽ kiểm tra xem đối thủ có high impact move hay không. Nếu có, AI sẽ thực hiện động thái đó. Nếu không, nó sẽ sử dụng thuật toán cắt tỉa alpha-beta để tìm ra nước đi tốt nhất
        :return: nước đi tiếp theo được thực hiện
        """
        # =======================================
        if(np.array_equal(self.state.board, game_settings.EMPTY_BOARD) or len(self.state.moves) <= 3):
            
            # Announcement
            print("AI used random move.")
            return self.random_move(self.state, 1)

        # =======================================
        # CHECKMATE MOVE
        # nếu đối thủ hoặc AI có checkmate move thì AI sẽ thực hiện nước đi này
        # đi nước đi nếu AI có checkmate move

        # Announcement
        print("Checking for checkmate move...")

        com_checkmate_move = State.checkmate(self.state.board, self.state.current_turn)
        if com_checkmate_move: 

            # Announcement
            print("AI has checkmate move.")
        
            return com_checkmate_move
        
        # ngược lại nếu đối thủ có checkmate move thì thực hiện
        opponent_checkmate_move = State.checkmate(self.state.board, game_settings.get_opponent(self.state.current_turn))
        if opponent_checkmate_move:

            # Announcement
            print("HUMAN has checkmate move.")

            return opponent_checkmate_move

        # Announcement
        print("No one has checkmate move.")

        # Announcement
        print("---------------------------------")
        
        # =======================================
        # HIGH-IMPACT MOVE
        # nếu đối thủ hoặc AI high-impact move, 
        # AI sẽ thực hiện nước đi nào có điểm cao nhất

        # Announcement
        print("Checking for high-impact move...")

        if ai_settings.ENABLE_HIGH_IMPACT_MOVE:
            opponent_high_impact_move, opponent_high_impact_score = State.high_impact_move(self.state.board, game_settings.get_opponent(self.state.current_turn))
            com_high_impact_move, com_high_impact_score = State.high_impact_move(self.state.board, self.state.current_turn)
            if opponent_high_impact_move and opponent_high_impact_score > com_high_impact_score:
                
                # Announcement
                print("AI has discovered that HUMAN has a high-impact move.")
                print("AI has taken this move (a defensive move).")
                
                return opponent_high_impact_move
            
            if com_high_impact_move and com_high_impact_score >= opponent_high_impact_score: # Ưu tiên các nước đi có lợi cho người chơi

                # Announcement
                print("AI has discovered that it has a high-impact move.")
                print("AI has taken this move (an offensive move).")
                
                return com_high_impact_move
            
            # Announcement
            print("AI did not discover any high-impact moves.")
        
        # Announcement
        print("---------------------------------")

        # =======================================
        # COMBO MOVE
        # nếu đối thủ hoặc AI có combo move, AI sẽ thực hiện nó

        # Announcement
        print("Checking for combo moves...")

        opponent_combo_move = State.combo_move(self.state.board, game_settings.get_opponent(self.state.current_turn))
        com_combo_move = State.combo_move(self.state.board, self.state.current_turn)
        
        if com_combo_move:
            
            # Announcement
            print("AI has a combo move. Take it!")
            
            return com_combo_move
        
        if opponent_combo_move: # Ưu tiên nước đi mang lại lợi thế cho người chơi hiện tại.
            
            # Announcement
            print("HUMAN has a combo move. Block it!")
            
            return opponent_combo_move

        # Announcement
        print("There is no combo move.")
        print("---------------------------------")

        # =======================================
        # nếu không => AI sử dụng Alpha-Beta pruning

        # Announcement
        print("AI has decided to use the Alpha-Beta pruning algorithm. Calculating...")
        
        root_node = MinimaxNode(self.state.board, self.state.moves[-1::1], self.state.current_turn, None)
        

        ABPruning.alpha_beta(root_node, ai_settings.MAX_TREE_DEPTH_LEVEL, -infinity, +infinity, True)
        
        # Announcement
        print("Completed calculation with depth = ", ai_settings.MAX_TREE_DEPTH_LEVEL, ".")

        return root_node.planing_next_move

    def random_move(self, state: State, expansion_range):
        """
        Lấy trạng thái và phạm vi mở rộng, đồng thời trả về một bước di chuyển ngẫu nhiên từ các bước di chuyển có thể
        
        :state: trạng thái hiện tại của bàn cờ
        :type state: State
        :expansion_range: phạm vị mở rộng của cây tìm kiếm
        """
        # AI move first
        # if(state.board == game_settings.EMPTY_BOARD):
        if np.array_equal(state.board, game_settings.EMPTY_BOARD):

            return(int(game_settings.BOARD_ROW_COUNT / 2), int(game_settings.BOARD_COL_COUNT / 2))
        # HUMAN move first
        possible_moves = State.generate_possible_moves(state.board, expansion_range)
        return random.choice(possible_moves)

    def alpha_beta(current_node: MinimaxNode, depth, alpha, beta, maximizingPlayer):
        """
        Đây là hàm đệ quy thực hiện thuật toán cắt tỉa alpha beta để tính điểm tốt nhất có thể cho người chơi hiện tại, dựa trên trạng thái bảng hiện tại
        
        current_node: MinimaxNode
        type current_node: MinimaxNode
        depth: độ sâu của cây
        alpha: giá trị tốt nhất mà người chơi MAX có thể đạt được tại nút MAX trên đường đi
        beta: giá trị tốt nhất mà người chơi MIN có thể đạt được tại nút MIN trên đường đi
        maximizingPlayer: True nếu là lượt của AI, False là lượt của người chơi
        return: giá trị của nước đi tốt nhất
        """
        # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        # https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
        
        if(depth == 0 or State.game_over(current_node.board)):
            O_score, X_score = State.evaluate(current_node.board)
            return X_score - O_score
        
        if maximizingPlayer:
            value = -infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = ABPruning.alpha_beta(child_node, depth - 1, alpha, beta, False)
                # value = max(value, temp) # đây
                if temp > value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = + infinity
            child_nodes = current_node.generate_child_nodes()
            for child_node in child_nodes:
                temp = ABPruning.alpha_beta(child_node, depth - 1, alpha, beta, True)
                # value = min(value, temp) # đây
                if temp < value:
                    value = temp
                    current_node.planing_next_move = child_node.last_move
                beta = min(beta, value) 
                if alpha >= beta:
                    break
            return value
