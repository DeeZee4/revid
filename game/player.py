from game.player_mode import PlayerMode as PM
from settings import Settings as s

class Player():
  def __init__(self, id, name=None, mode=PM.HUMAN):
    self.id = id
    if name != None:
      self.name = name
    else:
      self.name = self.default_player_name()
    self.set_mode(mode)
    self.color = s.colors.get("players")[self.id]
    self.color_hover = s.colors.get("players-hover")[self.id]

  def set_mode(self, player_mode:PM):
    self.mode = player_mode
    self.update_display_name()

  def set_name(self, name):
    if name != None:
      self.name = name
    else:
      self.name = self.default_player_name()
    self.update_display_name()

  def update_display_name(self):
    if self.mode == PM.AI:
      self.display_name = f"AI {self.id+1}"
    else:
      self.display_name = self.name

  def default_player_name(self):
    return f"Player {self.id+1}"

  