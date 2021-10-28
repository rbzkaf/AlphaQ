import os
import random
import sys
import numpy as np
from write import writeOutput
import shutil
import pickle


#drive.mount('/content/drive/')

from myagent import Agent
from my_player4 import LittleGo
from player_against_alphabeta import MCTS_Agent, tree

N = 5

# os.listdir()
shutil.copy('./init/input.txt', './')
game = Agent()
big_tree = tree()
player1 = MCTS_Agent(input_big_tree=big_tree)
player2 = LittleGo()

win1_w = 0
win2_w = 0
win1_b = 0
win2_b = 0


sav_frequency = 3
rnd = 18
for i in range(200):
    print("=====Round {}=====", rnd)
    print("Player1 as Black")
    winner,x,y = game.train_cycle(player1, player2)
    if winner == 1:
        win1_b+=1
    else:
        win2_w+=1

    print("Player2 as Black")
    winner, x, y = game.train_cycle(player2, player1)
    if winner == 1:
        win2_b += 1
    else:
        win1_w += 1

    print("Player 1")
    print("Wins as Black: ",win1_b,  "Wins as white: ",win1_w)
    print("Player 2")
    print("Wins as Black: ",win2_b,  "Wins as white: ",win2_w)




    if rnd % sav_frequency == 0:

        # big_tree.save_tree_with_count(rnd)
        node = big_tree.ultimate_root
        path = "./saved_data/trees/mcts_tree_3_" + str(rnd) + ".json"
        f = open(path, 'wb')
        p = pickle.Pickler(f)
        p.dump(node)
        f.close()

        """nx_new = np.concatenate(x_position_data)
        ny_new = np.concatenate(y_action_data)

        if rnd != 0:
            path1 = "./saved_data/positions/positions_3_" + str(rnd - sav_frequency) + ".npy"
            path2 = "./saved_data/actions/actions_3_" + str(rnd - sav_frequency) + ".npy"

            nx_old = np.load(path1)
            ny_old = np.load(path2)

            nx_new = np.concatenate((nx_old, nx_new))
            ny_new = np.concatenate((ny_old, ny_new))

        path1 = "./saved_data/positions/positions_3_" + str(rnd)
        path2 = "./saved_data/actions/actions_3_" + str(rnd)
        print("saving: ", path1, ",", path2)
        np.save(path1, nx_new)
        np.save(path2, ny_new)

        path1 = "./saved_data/positions/positions_3_" + str(rnd) + ".npy"
        path2 = "./saved_data/actions/actions_3_" + str(rnd) + ".npy"

        x_position_data = []
        y_action_data = []
        big_tree.save_tree_in_json()"""

    rnd+=1











