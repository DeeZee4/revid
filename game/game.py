from time import time
from game.game_state import GameState as GS
from game.board import Board
from game.player import Player
from game.player_mode import PlayerMode as PM
from game.revid import Revid

class Game():
  def __init__(self):
    self.game_state = GS.BEFORE
    self.board = Board()
    self.player = []
    for i in range(2):
      self.player.append(Player(i))
    self.next = self.player[0]
    self.winner = None
    self.invalid_turn = None

  def turn(self, x:int, y:int):
    if self.game_state == GS.PLAYING:
      if self.board.get(x,y) == -1:
        self.board.set(x, y, self.next.id)
        Revid.flip(self.board, x, y)
        self.next = self.get_opponent(self.next)

        if self.board.is_full():
          self.set_game_state(GS.AFTER)
        else:
          if self.next.mode == PM.AI:
            self.ai_turn()

      else:
        self.invalid_turn = (x,y)
        self.winner = [self.get_opponent(self.next)]
        self.set_game_state(GS.AFTER)

  def ai_turn(self):
    x,y = self.next.ai.get_turn(self.board, self.next)
    self.turn(x,y)

  def set_game_state(self, game_state:GS):
    if game_state == GS.AFTER:
      if self.winner == None:
        ps = self.get_player_scores()
        
        max_score = 0
        winner = []
        for i, score in enumerate(ps):
          if score > max_score:
            winner = []
            winner.append(self.player[i])
            max_score = score
          elif score == max_score:
            winner.append(self.player[i])
        self.winner = winner

      self.game_state = GS.AFTER
        
  def get_player_scores(self):
    player_scores = []
    for p in self.player:
      player_scores.append(self.board.count(p.id))
    return player_scores

  def get_opponent(self, p):
    if p.id == self.player[0].id:
      return self.player[1]
    else:
      return self.player[0]