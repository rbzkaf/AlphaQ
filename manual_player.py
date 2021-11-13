import random
import sys
from read import readInput
from write import writeOutput
import time
from host import GO

class Manual_Player():
    def __init__(self):
        self.type = 'random'

    def get_input(self):
        print("Entire action")
        x = input("x:")
        y = input("y:")
        action = (int(x),int(y))
        return action



if __name__ == "__main__":
    N = 5
    begin = time.time()
    player = Manual_Player()
    print("Entire action")
    x = input("x:")
    y = input("y:")
    action = (x,y)
    writeOutput(action)
    print("Time taken by rando = ", time.time() - begin)