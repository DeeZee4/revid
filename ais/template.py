#
# @param board
# from type game.Board
# you can use board.get(x,y) to get the status of the field (-1, 0 or 1)
#
# @param you
# represents the symbol you (this AI) is on the board
# either 0 or 1
#
import random

def turn(board, you):
    #
    # crazy ai goes here
    #

    for _ in range(20):
        x = random.randint(0,7)
        y = random.randint(0,7)
        if board.get(x,y) == -1:
            return (x,y)

    for x in range(8):
        for y in range(8):
            if board.get(x,y) == -1:
                return (x,y)
