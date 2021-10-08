from settings import Settings as s

class Board():
  def __init__(self):
    self.board = self.new_blank()

  def get(self, x, y):
    if self.is_pos(x, y):
      return self.board[y][x]
    return None

  def set(self, x, y, value):
    if self.is_pos(x, y):
      self.board[y][x] = value
      return True
    return False

  def count(self, value):
    counter = 0
    for column in self.board:
      for field in column:
        if field == value:
          counter += 1
    return counter


  def is_full(self):
    for column in self.board:
      if -1 in column:
        return False
    return True

  def is_pos(self, x, y):
    if 0<=x<=s.board[0]-1 and 0<=x<=s.board[1]-1:
      return True
    return False

  def new_blank(self):
    return [[-1 for _ in range(s.board[0])] for _ in range(s.board[0])]