import numpy as np
from myagent import Agent

BOARD_SIZE = 5

class Vectorizer():

    def __init__(self):
        self.size = BOARD_SIZE
        self.planes = 12

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
        print(game_tensor)
        print("Size = ", len(game_tensor))
        #game_functions = Agent()
        game_functions = Agent(board=board, pre_board=prev_board, color=color)
        base_plane = {
            color: 0,
            3-color: 6
        }


        for x in range(self.size):
            for y in range(self.size):

                liberty = game_functions.group_liberty_count(x,y,game_functions.cur_board)
                if liberty == 4:
                    liberty = 3

                if game_functions.cur_board[x][y] != 0:
                    plane = base_plane[game_functions.cur_board[x][y]] + liberty - 1
                    game_tensor[plane][x][y] = 1

                if game_functions.prev_board[x][y] != 0:
                    prev_move_plane = base_plane[game_functions.prev_board[x][y]] + 3 + liberty - 1
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
    v =Vectorizer()
    print(v.vectorize_input(board=[[1, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]],
                            prev_board= [[1, 0, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]], color=1 ))
