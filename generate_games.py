import os
import random
import sys
import numpy as np
from write import writeOutput
import shutil
import pickle


#drive.mount('/content/drive/')

from myagent import Agent
from self_player import MCTS_Agent, tree

N = 5

# os.listdir()
shutil.copy('./init/input.txt', './')
game = Agent()
big_tree = tree()
player1 = MCTS_Agent(input_big_tree=big_tree)
player2 = MCTS_Agent(input_big_tree=big_tree)

x_position_data = []
y_action_data = []

win_position_data = []
win_action_data = []

sav_frequency = 25
rnd = 751
while(rnd+1):
    print("=====Round {}=====", rnd)
    winner, x, y = game.train_cycle(player1, player2)

    print(winner)

    if winner == 1:
        fact = 0
    else:
        fact = 1

    move = 0
    for move in range(len(x)):
        if move%2 == fact:
            win_position_data.append(x[move])
            win_action_data.append(y[move])

    x_position_data.append(x)
    y_action_data.append(y)

    print("win position len: ", len(win_position_data))
    print("win action len: ", len(win_action_data))

    if rnd % (sav_frequency*2) == 0:

        # big_tree.save_tree_with_count(rnd)
        node = big_tree.ultimate_root
        path = "./saved_data/trees/mcts_tree_7_" + str(rnd) + ".json"
        f = open(path, 'wb')
        p = pickle.Pickler(f)
        p.dump(node)
        f.close()

    if rnd % sav_frequency == 0:


        #Saving all moves
        nx_new = np.concatenate(x_position_data)
        ny_new = np.concatenate(y_action_data)

        if rnd != 0:
            path1 = "./saved_data/positions/positions_7_" + str(rnd - sav_frequency) + ".npy"
            path2 = "./saved_data/actions/actions_7_" + str(rnd - sav_frequency) + ".npy"

            nx_old = np.load(path1)
            ny_old = np.load(path2)

            nx_new = np.concatenate((nx_old, nx_new))
            ny_new = np.concatenate((ny_old, ny_new))

        path1 = "./saved_data/positions/positions_7_" + str(rnd)
        path2 = "./saved_data/actions/actions_7_" + str(rnd)
        print("saving: ", path1, ",", path2)
        np.save(path1, nx_new)
        np.save(path2, ny_new)

        #saving win data

        win_nx_new = np.concatenate(win_position_data)
        win_ny_new = np.concatenate(win_action_data)

        if rnd != 0:
            path1 = "./saved_data/positions/win_positions_7_" + str(rnd - sav_frequency) + ".npy"
            path2 = "./saved_data/actions/win_actions_7_" + str(rnd - sav_frequency) + ".npy"

            win_nx_old = np.load(path1)
            win_ny_old = np.load(path2)

            win_nx_new = np.concatenate((win_nx_old, win_nx_new))
            win_ny_new = np.concatenate((win_ny_old, win_ny_new))

        path1 = "./saved_data/positions/win_positions_7_" + str(rnd)
        path2 = "./saved_data/actions/win_actions_7_" + str(rnd)
        print("saving: ", path1, ",", path2)
        np.save(path1, win_nx_new)
        np.save(path2, win_ny_new)

        #path1 = "./saved_data/positions/win_positions_7_" + str(rnd) + ".npy"
        #path2 = "./saved_data/actions/win_actions_7_" + str(rnd) + ".npy"

        x_position_data = []
        y_action_data = []
        win_position_data = []
        win_action_data = []
        big_tree.save_tree_in_json()

    rnd+=1



print(len(win_position_data))
print(len(win_action_data))








