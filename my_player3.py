from myagent import Agent
import random
import json
from copy import deepcopy
import math
import time
from mcts_node import Node
import pickle

BOARD_SIZE = 5


class tree():

    def __init__(self, node=None):

        if node is not None:
            print("Init new tree")
            self.ultimate_root = node
            self.save_tree_in_json()

        else:
            print("Loading Tree")
            self.load_tree_from_json()

    def save_tree_in_json(self):
        node = self.ultimate_root
        f = open('mcts_tree.json', 'wb')
        p = pickle.Pickler(f)
        p.dump(node)

        """for child in node.children:
            print("saving: ", child.cur_state)
            print("whose parent is: ", child.get_parent().cur_state)
            p.dump(child)"""

    def load_tree_from_json(self):
        f = open('mcts_tree.json', 'rb')
        p = pickle.Unpickler(f)
        node = p.load()

        self.ultimate_root = node


class MCTS_Agent(Agent):

    def __init__(self, pre_board=None, board=None):


        self.type = 'MCTS'
        with open('input.txt') as f:
            lines = f.readlines()

        self.color = int(lines[0])
        self.prev_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:BOARD_SIZE + 1]]
        self.cur_board = [[int(x) for x in line.rstrip('\n')] for line in lines[BOARD_SIZE + 1: 2 * BOARD_SIZE + 1]]

        f.close()

        new_game_flag = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.cur_board[x][y] != 0:
                    new_game_flag += 1

        # For new Game
        if new_game_flag == 0:
            print("New Game")
            self.root_node = big_tree.ultimate_root
            self.moves = 0
            self.track_moves(move_num=0)

        elif new_game_flag == 1:
            self.root_node = big_tree.ultimate_root
            self.moves = 1
            opp_move = self.get_opp_move()
            self.track_moves(move_num=1, opp_move=opp_move)
            self.root_node = self.root_node.visit_particular_child(opp_move)

        else:
            z = json.load(open('move_count.json'))
            moves = z['move_count']
            self.moves = moves
            self.track_moves(moves, self.get_opp_move())
            f = open('track_move.json', 'r')
            move_list = json.load(f)
            node = big_tree.ultimate_root
            for x in move_list:
                node = node.visit_particular_child(x)

            self.root_node = node

            f.close()

        print("The root is ")
        for l in self.root_node.cur_state:
            print(l)
        print("\n\nPossibilities are: ", self.root_node.children_unvisited)

        # Can Vary for results
        self.temperature = 2
        self.time = 30 * self.moves + 30

    def get_opp_move(self):

        opp_color = 3 - self.color
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.cur_board[x][y] == opp_color and self.prev_board[x][y] == 0:
                    return (x, y)

        return (-1, -1)

    def track_moves(self, move_num, opp_move=None):

        f = open('track_move.json', 'r')

        if move_num == 0 or move_num == -1:
            print("Clearing move list1")
            move_list = []

        elif move_num == 1:
            move_list = []
            print("Clearing move list2")
            print("Before Append: ", move_list)
            move_list.append(opp_move)
            print("After Append: ", move_list)

        else:
            print("appending to list")
            move_list = json.load(f)
            print("Before Append: ", move_list)
            move_list.append(opp_move)
            print("After Append: ", move_list)

        f.close()

        print("Dumping move list:", move_list)
        f = open('track_move.json', 'w')
        json.dump(move_list, f)
        f.close()

    def get_input(self):

        begin = time.time()
        cur_tree_root_node = self.root_node
        tot_time = 0
        num_of_sims = 0

        #while time.time() - begin < 3.3:
        for i in range(self.time):
            print(time.time())
            cur_node = cur_tree_root_node
            """Select best child if it is not a leaf node
               That is, the node has best UCS"""

            child_left = cur_node.children_left_to_visit()
            if child_left == 0:
                if cur_node.is_terminal_state == False:
                    cur_node = self.select_uct_child(cur_node)

            if cur_node.children_left_to_visit():
                cur_node = cur_node.visit_random_child()

            winner = cur_node.simulate_random_game()
            num_of_sims += 1

            'Back propagate results'
            while cur_node is not None:
                cur_node.record_game(winner)
                cur_node = cur_node.parent

        best_output_move = None
        best_ratio = -1.0
        for child in cur_tree_root_node.children:
            child_ratio = child.winning_ratio(self.color)
            if child_ratio > best_ratio:
                best_ratio = child_ratio
                best_output_move = child.prev_move

        print("Move no.", self.moves)
        print("Selecting move ", best_output_move, "With ratio: ", best_ratio)
        print("Number of simulations run: ", num_of_sims)
        return best_output_move

    def uct_score(self, parent_rollouts, child_rollouts, win_pct, temperature):
        exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
        return win_pct + temperature * exploration

    def select_uct_child(self, node):

        S_p = sum(child.num_of_rollouts for child in node.children) + 1  # Total Rollouts
        log_S_p = math.log(S_p)

        max = -1
        max_child = None
        """
        UCB = win percentage + tempeature * exploration
        """
        for child in node.children:
            child_ratio = child.winning_ratio(self.color)
            uct_score = child_ratio + self.temperature * math.sqrt(log_S_p / child.num_of_rollouts)

            if uct_score > max:
                max = uct_score
                max_child = child

        return max_child

    # Using Output of write.py so it is vocareum acceptable
    def gen_output(self):

        output = self.get_input()
        res = ""
        if output[0] == -1:
            res = "PASS"
        else:
            res += str(output[0]) + ',' + str(output[1])

        with open("output.txt", 'w') as f:
            f.write(res)

        x = {'move_count': self.moves + 2, }

        """"""
        file = open('track_move.json', 'r')
        move_list = json.load(file)
        # print("Before Append: ", move_list)
        move_list.append(output)
        # print("After Append: ", move_list)

        file.close()

        file = open('track_move.json', 'w')

        json.dump(move_list, file)
        file.close()
        """"""

        move_file = open('move_count.json', 'w')
        json.dump(x, move_file)

        f.close()
        move_file.close()
        print(output)


if __name__ == "__main__":

    start = time.time()

    cont = open('cont.json', 'r')
    x = json.load(cont)
    print(x)
    cont.close()
    if x==0:
        big_tree = tree()
        print("load 1")
        cont = open('cont.json', 'w')
        json.dump(1, cont)
        cont.close()
    player = MCTS_Agent()
    # big_tree = tree(player.root_node)
    # player.get_input()
    player.gen_output()
    # print(player.get_opp_move())
    #big_tree.save_tree_in_json()
    print("Time for move = ", time.time() - start)




