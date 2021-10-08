from ui.ui import UI
from game.game import Game

class Main():
  def __init__(self):
    self.game = None
    self.ui = UI(self)
    
    while True:
      if self.game == None:
        self.game = Game()

      self.ui.update()

if __name__ == "__main__":
  Main()