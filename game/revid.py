from game.board import Board
from settings import Settings as s

class Revid():
  # x and y are the coordinates from the last move
  def flip(board:Board, x:int, y:int):
    # player who did the last move
    p = board.get(x,y)

    columns, rows = s.board

    # Corner kills
    if x == 1 and y == 1:
      if board.get(0,0) != -1:
        board.set(0,0,p)

    if x == columns-2 and y == 1:
      if board.get(columns-1,0) != -1:
        board.set(columns-1,0,p)

    if x == columns-2 and y == rows-2:
      if board.get(columns-1,rows-1) != -1:
        board.set(columns-1,rows-1,p)

    if x == 1 and y == rows-2:
      if board.get(0,rows-1) != -1:
        board.set(0,rows-1,p)

    # Flipping
    # right
    found = False
    for i_x in range(x+1,columns):
      if board.get(i_x, y) == p:
        found = True
    if found:
      for i_x in range(x+1,columns):
        if board.get(i_x, y) == p:
          break
        if board.get(i_x,y) != p and board.get(i_x,y) != -1:
          board.set(i_x,y,p)

    # left
    found = False
    for i_x in range(x)[::-1]:
      if board.get(i_x, y) == p:
        found = True
    if found:
      for i_x in range(x)[::-1]:
        if board.get(i_x, y) == p:
          break
        if board.get(i_x,y) != p and board.get(i_x,y) != -1:
          board.set(i_x,y,p)

    # bottom
    found = False
    for i_y in range(y+1,rows):
      if board.get(x, i_y) == p:
        found = True
    if found:
      for i_y in range(y+1,rows):
        if board.get(x, i_y) == p:
          break
        if board.get(x,i_y) != p and board.get(x,i_y) != -1:
          board.set(x,i_y,p)

    # top
    found = False
    for i_y in range(y)[::-1]:
      if board.get(x, i_y) == p:
        found = True
    if found:
      for i_y in range(y)[::-1]:
        if board.get(x, i_y) == p:
          break
        if board.get(x,i_y) != p and board.get(x,i_y) != -1:
          board.set(x,i_y,p)
    