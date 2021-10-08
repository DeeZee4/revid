import pygame
import os

from settings import Settings as s
from ui.states import *
from ui.components import *
from game.game_state import GameState as GS
import glob

class UI():
  def __init__(self, main):
    self.main = main
    pygame.init()
    self.screen = pygame.display.set_mode(s.dimensions, pygame.RESIZABLE)

  def update(self):
    self.game = self.main.game
    self.screen.fill(s.colors["bg"])

    pygame_info = pygame.display.Info()
    glob.dimensions = (pygame_info.current_w, pygame_info.current_h)

    #choose correct state template
    state = None

    if self.game.game_state == GS.BEFORE:
      state = Before(self)
    elif self.game.game_state == GS.PLAYING:
      state = Playing(self)
    else:
      state = Playing(self)
    
    if state != None:
      state.render()
    else:
      print("ERROR: Unknown gamestate")

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          os._exit(1)