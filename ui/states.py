import glob
from ui.components import *
from game.game_state import GameState as GS

class Before():
  def __init__(self, ui):
    self.ui = ui

  def start_game(self):
    self.ui.game.game_state = GS.PLAYING
    if self.ui.game.next.mode == PM.AI:
      self.ui.game.ai_turn()

  def render(self):
    screen_width, screen_height = glob.dimensions

    for i,p in enumerate(self.ui.game.player):
      lbl = Label(self.ui.screen, (screen_width*0.333333*(i+1), screen_height*0.35), msg=p.display_name, font_size=36)
      lbl.render()
      pms = PlayerModeSwitch(self.ui, (screen_width*0.333333*(i+1), screen_height*0.5, screen_width*0.2, screen_height*0.15), p)
      pms.render()

    btn_start = Button(self.ui.screen, (screen_width/2,screen_height*0.7,screen_width*0.5,screen_height*0.1), msg="Play!", action=self.start_game, chover=(0,150,0))
    btn_start.render()


class Playing():
  def __init__(self, ui):
    self.ui = ui
  
  def render(self):
    screen_width, screen_height = glob.dimensions

    pa = PlayingArea(self.ui, (0,0,screen_width*0.7,screen_height))
    pa.render()

    ra = RightArea(self.ui, (screen_width*0.7, 0, screen_width*0.3, screen_height))
    ra.render()

