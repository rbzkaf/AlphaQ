from copy import deepcopy
from write import writeNextInput
import numpy as np

BOARD_SIZE = 5


class Agent:

    def __init__(self, pre_board=None, board=None, color=None):

        if pre_board is not None:
            self.prev_board = pre_board
            self.cur_board = board
            self.color = color

        else:
            with open('input.txt') as f:
                lines = f.readlines()

            self.color = int(lines[0])
            self.prev_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:BOARD_SIZE + 1]]
            self.cur_board = [[int(x) for x in line.rstrip('\n')] for line in lines[BOARD_SIZE + 1: 2 * BOARD_SIZE + 1]]

    def get_input(self):
        pass

    def terminal_state(self, moves_taken):
        pass

    def piece_liberty_spots(self, i, j, board):
        """

        :param i:
        :param j:
        :return:
        """

        liberty_spots = []
        neighbors = self.find_neighbors(i, j, board)
        for point in neighbors:
            if board[point[0]][point[1]] == 0:
                liberty_spots.append(point)
        return liberty_spots

    def piece_liberty_count(self, i, j, board):

        return len(self.piece_liberty_spots(i, j, board))

    def find_neighbors(self, i, j, board):
        neighbors = []

        if i > 0:
            neighbors.append((i - 1, j))
        if i < BOARD_SIZE - 1:
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < BOARD_SIZE - 1:
            neighbors.append((i, j + 1))

        return neighbors

    def find_neighbors_ally(self, i, j, board):
        ally_neighbors = []
        color = board[i][j]
        if i > 0:
            if board[i - 1][j] == color:
                ally_neighbors.append((i - 1, j))
        if i < BOARD_SIZE - 1:
            if board[i + 1][j] == color:
                ally_neighbors.append((i + 1, j))
        if j > 0:
            if board[i][j - 1] == color:
                ally_neighbors.append((i, j - 1))
        if j < BOARD_SIZE - 1:
            if board[i][j + 1] == color:
                ally_neighbors.append((i, j + 1))

        return ally_neighbors

    def find_neighbors_enemy(self, i, j, board):
        enemy_neighbors = []
        color = board[i][j]
        if i > 0:
            if board[i - 1][j] == 3 - color:
                enemy_neighbors.append((i - 1, j))
        if i < BOARD_SIZE - 1:
            if board[i + 1][j] == 3 - color:
                enemy_neighbors.append((i + 1, j))
        if j > 0:
            if board[i][j - 1] == 3 - color:
                enemy_neighbors.append((i, j - 1))
        if j < BOARD_SIZE - 1:
            if board[i][j + 1] == 3 - color:
                enemy_neighbors.append((i, j + 1))

        return enemy_neighbors

    def find_group(self, i, j, board):

        root = [(i, j)]
        group_members = []

        while root:
            x = root.pop()
            group_members.append(x)
            allies = self.find_neighbors_ally(x[0], x[1], board)
            for y in allies:
                if y not in root and y not in group_members:
                    root.append(y)
        return group_members

    def group_liberty_spots(self, i, j, board):

        if board[i][j] == 0:
            return []
        group = self.find_group(i, j, board)
        free_spots = []
        for piece in group:
            spots = self.piece_liberty_spots(piece[0], piece[1], board)
            for spot in spots:
                if spot not in free_spots:
                    free_spots.append(spot)
        return free_spots

    def group_liberty_count(self, i, j, board):

        return len(self.group_liberty_spots(i, j, board))

    def get_dying_pieces(self, board, color):
        dying = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.group_liberty_count(x, y, board) == 0 and board[x][y] == 3 - color:
                    dying.append((x, y))

        return dying

    def get_board_after_died(self, board, color):
        for piece in self.get_dying_pieces(board, color):
            board[piece[0]][piece[1]] = 0

        return board

    def check_legit_placement(self, i, j, board, prev_board, color, reason=False):

        if i < 0 or i >= BOARD_SIZE:
            if reason:
                print("Out of bounds")
            return False

        if j < 0 or j >= BOARD_SIZE:
            if reason:
                print("Out of bounds")
            return False

        if board[i][j] != 0:
            if reason:
                print("Piece already in position")
            return False

        next_board = deepcopy(board)
        next_board[i][j] = color

        if self.group_liberty_count(i, j, next_board):
            return True

        next_board = self.get_board_after_died(next_board, color)

        if not self.group_liberty_count(i, j, next_board):
            if reason:
                print("No liberty here")
            return False

        # repeat placement
        elif color == prev_board[i][j]:
            if reason:
                print("KO Rule. Repeat Placement")
            return False

        return True

    def get_ko_board(self, board, prev_board, color, reason=False):

        ko_board = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                ko_board[i][j] = 0

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):

                next_board = deepcopy(board)
                next_board[i][j] = color

                next_board = self.get_board_after_died(next_board, color)

                if next_board[i][j] == prev_board[i][j]:
                    ko_board[i][j] =1

        return ko_board


    def place_piece(self, i, j, board, prev_board, color):

        if i == -1 and j == -1:
            return board
        if not self.check_legit_placement(i, j, board, prev_board, color):
            print("Illegal move")
            return False
        next_board = deepcopy(board)
        next_board[i][j] = color
        next_board = self.get_board_after_died(next_board, color)
        return next_board

    def score(self, board, color):
        score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == color:
                    score += 1
        return score

    def find_winner(self, board):
        black_score = self.score(board, 1)
        white_score = self.score(board, 2)

        if black_score > white_score + 2.5: return 1
        if black_score < white_score + 2.5: return 2

    def show_board(self, board):
        for l in board:
            print(l)

    def game_end_flag(self, ):
        pass

    # Somewhat uses logic from host.py

    def train_cycle(self,player1,player2):

        board = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        prev_board = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

        played_move = 0
        pass_flag = 0
        piece_type = 2

        vectorizer = Vectorizer()

        x_pos = []
        y_act = []
        while 1:
            self.viz_board(board)
            piece_type = 3 - piece_type

            if played_move >= 24 or pass_flag >= 2:
                print("played moves:",played_move)
                print("pass flag", pass_flag)
                result = self.find_winner(board)
                print('Game ended.')
                print('The winner is {}'.format('X' if result == 1 else 'O'))
                return result, x_pos, y_act

            player = "X" if piece_type == 1 else "O"
            print(player + " makes move...")

            writeNextInput(1, prev_board, board)
            if piece_type == 1:
                writeNextInput(1, prev_board, board)
                action = player1.get_input()
            else:
                writeNextInput(2, prev_board, board)
                action = player2.get_input()

            print(action)

            if action[0] == -1:
                pass_flag +=1
            else:
                pass_flag = 0

            next_board = self.place_piece(action[0],action[1],board,prev_board,piece_type)
            if next_board == False:
                print("Because of illegal move, opponent wins")
                return 3-piece_type

            x_pos.append(vectorizer.vectorize_input(board=board,prev_board=prev_board,color=piece_type))
            y_act.append(vectorizer.vectorize_action(action=action))

            prev_board = deepcopy(board)
            board = deepcopy(next_board)
            played_move += 1

    def viz_board(self, board):

        print('-' * len(board) * 2)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)


class Vectorizer():

    def __init__(self):
        self.size = BOARD_SIZE
        self.planes = 8

    def normalize_board(self,board,prev_board,color):

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):

                if color == 1:
                    if board[x][y] == 2:
                        board[x][y] = -1
                    if prev_board[x][y] == 2:
                        prev_board[x][y] = -1

                if color == 2:
                    if board[x][y] == 1:
                        board[x][y] = -1
                    if prev_board[x][y] == 1:
                        prev_board[x][y] = -1
                    if board[x][y] == 2:
                        board[x][y] = 1
                    if prev_board[x][y] == 2:
                        prev_board[x][y] = 1

        return board,prev_board



    def vectorize_input(self,board,prev_board,color):

        game_tensor = np.zeros(self.return_shape())
        #game_functions = Agent()
        game_functions = Agent(board=board, pre_board=prev_board, color=color)
        base_plane = {
            color: 0,
            3-color: 4
        }


        for x in range(self.size):
            for y in range(self.size):

                liberty = game_functions.piece_liberty_count(x,y,game_functions.cur_board)
                if liberty == 4:
                    liberty = 3


                if game_functions.cur_board[x][y] != 0:
                    plane = base_plane[game_functions.cur_board[x][y]] + liberty - 1
                    game_tensor[plane][x][y] = 1

                if game_functions.prev_board[x][y] != 0:
                    prev_move_plane = base_plane[game_functions.prev_board[x][y]] + 3
                    game_tensor[prev_move_plane][x][y] = 1

        return game_tensor

    def vectorize_action(self,action):

        out = [[0 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE + 1)]

        out[action[0]][action[1]] = 1

        return out

    def return_point_index(self,i,j,plane=0):

        index = self.size*self.size*plane + self.size*i + j
        return index

    def return_shape(self):

        return self.planes, self.size, self.size

if __name__ == "__main__":
    player = Agent()
    for l in player.cur_board:
        print(l)

    print(player.get_ko_board(player.cur_board,player.prev_board,player.color))



