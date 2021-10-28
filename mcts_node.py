from myagent import Agent
import random
from copy import deepcopy
import math
import json

BOARD_SIZE = 5
tot_moves = BOARD_SIZE*BOARD_SIZE - 1


class Node():
    def __init__(self, cur_state, parent = None, color = None,  prev_move = None, moves_taken = None, prev_state = None, create = True):
        self.cur_state = cur_state
        self.prev_state = prev_state
        self.prev_move = prev_move
        self.color = color
        self.moves_taken = moves_taken
        self.parent = parent
        """
        To make functions work, need a parent node to root
        """
        if parent is None:
            if moves_taken is None:
                self.moves_taken = 0
                self.color = 1
                god_parent = Node(cur_state=[[0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0],
                                    [0, 0, 0, 0, 0]],
                                    moves_taken=-1,
                                    create =False)
                self.parent = god_parent
            if prev_state is not None:
                self.color = color
                empty_parent = Node(cur_state=prev_state, create = False)
                self.parent = empty_parent

        if self.moves_taken != -1:
            self.game_functions = Agent(pre_board=self.parent.cur_state, board=self.cur_state)

        else:
            self.game_functions = Agent([[0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0],
                                         [0, 0, 0, 0, 0]], self.cur_state)

        self.is_terminal_state = self.check_terminal()

        """
        MCTS Important values
        """
        self.win_count ={
            1: 0,
            2: 0
        }
        self.num_of_rollouts = 1
        self.children = []

        self.children_unvisited = []
        if self.moves_taken >= 0:
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    if self.game_functions.check_legit_placement(x, y, self.cur_state, self.parent.cur_state, self.color):
                        self.children_unvisited.append((x, y))

            # To start passing
        if self.moves_taken > 20:
            self.children_unvisited.append((-1,-1))

        self.children_edges = deepcopy(self.children_unvisited)

    def visit_particular_child(self,edge):

        for child in self.children:
            if child.prev_move[0] == edge[0] and child.prev_move[1] == edge[1]:
                #print("going from ", self.cur_state)
                #print("to child: ", child.cur_state)
                return child

        #If child hasnt been visited yet
        #print("Creating child")
        next_board = self.game_functions.place_piece(edge[0],edge[1],self.cur_state,self.prev_state,self.color)

        new_node = Node(cur_state=next_board,
                        parent=self,
                        color=3 - self.color,
                        prev_move=edge,
                        moves_taken=self.moves_taken + 1,
                        prev_state=self.cur_state,
                        create=False
                        )
        #print("Move :", edge, ", Going to Child:")
        self.game_functions.show_board(new_node.cur_state)
        self.children.append(new_node)
        return new_node







    def get_parent(self):

        return self.parent

    def check_terminal(self):

        if self.moves_taken >= BOARD_SIZE*BOARD_SIZE - 1:
            return True
        if self.moves_taken > 2:
            if self.moves_taken >= tot_moves:
                return True
            else:
                oppo_played = 0
                for x in range(BOARD_SIZE):
                    for y in range(BOARD_SIZE):
                        if self.cur_state[x][y] != self.prev_state[x][y]:
                            oppo_played += 1
                z = json.load(open('move_count.json'))
                prev_move = self.prev_move
                if prev_move[0] == -1 and oppo_played == 0:
                    return True

        return False

    def record_game(self, winner, verbose = False):
        self.win_count[winner] += 1
        self.num_of_rollouts += 1

    def check_simulation_terminal(self, board, pre):
        pass

    def winning_ratio(self, color):
        return float(self.win_count[color]) / float(self.num_of_rollouts)

    # Random for now
    def rollout_policy(self):
        index = random.randint(0, len(self.children_unvisited) - 1)
        return index


    def visit_random_child(self):

        # Visits a random child from vaild moves
        index = self.rollout_policy()
        child_to_visit = self.children_unvisited.pop(index)
        #print("Visiting child: ", index)
        next_board = self.game_functions.place_piece(child_to_visit[0],child_to_visit[1],self.cur_state,self.prev_state,self.color)

        # Creates new Node and attaches to parent
        new_node = Node(cur_state=next_board,
                        parent=self,
                        color=3 - self.color,
                        prev_move=child_to_visit,
                        moves_taken=self.moves_taken + 1,
                        prev_state=self.cur_state
                        )
        self.children.append(new_node)
        return new_node

    def children_left_to_visit(self):

        if self.children_unvisited is not None:
            return len(self.children_unvisited)
        else:
            return 0

    def simulate_random_game(self, verbose = False):
        sim_board = deepcopy(self.cur_state)
        prev_sim_board = deepcopy(self.parent.cur_state)
        turn = self.color
        moves = self.moves_taken


        rand_move = []
        one_pass = 0
        while moves <= tot_moves - 1:
            for x in range(BOARD_SIZE):
                for y in range(BOARD_SIZE):
                    if self.game_functions.check_legit_placement(x, y, sim_board, prev_sim_board, turn):
                        rand_move.append((x,y))

            if moves > 18:
                rand_move.append((-1, -1))
            action = random.choice(rand_move)
            # 2 Passes Terminal
            if action[0] == -1:
                one_pass += 1
                if one_pass == 2:
                    break
            else:
                one_pass = 0
            prev_sim_board = deepcopy(self.parent.cur_state)
            sim_board = self.game_functions.place_piece(action[0], action[1], sim_board, prev_sim_board, color=turn)

            rand_move = []
            moves += 1
            turn = 3 - turn

        winner = self.game_functions.find_winner(sim_board)
        return winner




    def test_children(self):

        print(self.moves_taken)
        while self.children_left_to_visit():
            self.visit_random_child()
            print("Child added")

        for child in self.children:
            print(child.moves_taken)







if __name__ == "__main__":
    root = Node([[2, 1, 1, 1, 0],
[2, 1, 2, 2, 1],
[2, 1, 1, 2, 2],
[1, 2, 1, 0, 1],
[1, 2, 2, 1, 2]]
)

    print(root.color)


