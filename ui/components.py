import pygame
import time

from settings import Settings as s
import glob
from game.game_state import GameState as GS

class Button():
  def __init__(self, screen, dimensions, cbg=s.colors["fg"], cfg=s.colors["bg"], chover=None, msg=None, action=None):
    self.screen = screen
    self.x, self.y, self.w, self.h = dimensions
    self.fill_color = cbg
    self.text_color = cfg
    self.hover_color = chover
    self.msg = msg
    self.action = action

  def render(self):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = self.fill_color

    if self.x-self.w/2 < mouse[0] < self.x+self.w/2 \
    and self.y-self.h/2 < mouse[1] < self.y+self.h/2:
      if self.hover_color != None:
        color = self.hover_color
      if click[0] == True and self.action != None:
        if time.time() - glob.last_click > s.click_interval:
          glob.last_click = time.time()
          self.action()

    pygame.draw.rect(self.screen, color, (self.x-self.w/2,self.y-self.h/2,self.w,self.h), border_radius=5)

    if self.msg != None:
      text = Label(self.screen, (self.x, self.y), self.msg, fg=self.text_color, font_size=16)
      text.render()


class Label():
  def __init__(self, screen, pos, msg=None, fg=s.colors["fg"], font_size=16):
    self.screen = screen
    self.x, self.y = pos
    self.color = fg
    self.msg = msg
    self.font_size = font_size

  def render(self):
    font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
    text_surface = font.render(self.msg, True, self.color)
    text_rect = text_surface.get_rect()
    text_rect.center = (self.x,self.y)
    self.screen.blit(text_surface, text_rect)

### Game Specific ##########
class Field():
  def __init__(self, ui, pos, x, y, r, active=True):
    self.ui = ui
    self.pos = pos
    self.x = x
    self.y = y
    self.r = r
    self.active = active

  def render(self):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    hover = False

    if self.active:
      if self.pos[0]-self.r < mouse[0] < self.pos[0]+self.r \
      and self.pos[1]-self.r < mouse[1] < self.pos[1]+self.r:
        hover = True
        if click[0] == True:
          if time.time() - glob.last_click > s.click_interval:
            glob.last_click = time.time()
            self.ui.game.turn(self.x, self.y)

    color = s.colors.get("bg")

    board = self.ui.game.board

    if board.get(self.x, self.y) == -1 and hover:
      color = self.ui.game.next.color_hover
    
    for p in self.ui.game.player:
      if board.get(self.x, self.y) == p.id:
        color = p.color
        break
    
    
    pygame.draw.circle(self.ui.screen, color, self.pos, self.r)

    


class Grid():
  def __init__(self, ui, dimensions):
    self.ui = ui
    self.x, self.y, self.w, self.h = dimensions


  def render(self):
    pygame.draw.rect(self.ui.screen, s.colors.get("bg"), (self.x,self.y,self.w,self.h))


    count_columns, count_rows = s.board
    q = s.field_divider_proportion

    # Calculate column width in percent
    count_c_divider = count_columns + 1
    
    # Used a linear system of equations to find these equations
    columns_percent = 100/(count_columns+q*count_c_divider)
    columns_percent /= 100
    c_divider_percent = q*columns_percent
    c_w = columns_percent*self.w
    c_d_w = c_divider_percent*self.w
    if c_d_w < 1:
      c_d_w = 1



    # Calcualte row height in percent
    count_r_divider = count_rows + 1

    rows_percent = 100/(count_rows+q*count_r_divider)
    rows_percent /= 100
    r_divider_percent = q*rows_percent
    r_h = rows_percent*self.h
    r_d_h = r_divider_percent*self.h
    if r_d_h < 1: 
      r_d_h = 1

    # draw grid
    for i_x in range(count_c_divider):
      x = (c_w+c_d_w)*i_x+self.x
      pygame.draw.rect(self.ui.screen, s.colors.get("fg"), (x, self.y, c_d_w, self.h))


    for i_y in range(count_r_divider):
      y = (r_h+r_d_h)*i_y+self.y
      pygame.draw.rect(self.ui.screen, s.colors.get("fg"), (self.x, y, self.w, r_d_h))

    # draw fields
    if c_w < r_h:
      r = (c_w/2)*0.9
    else:
      r = (r_h/2)*0.9

    for x in range(count_columns):
      for y in range(count_rows):
        pos_x = self.x + (c_w+c_d_w)*x + c_w/2 + c_d_w
        pos_y = self.y + (r_h+r_d_h)*y + r_h/2 + r_d_h

        active = True
        if self.ui.game.board.get(x,y) != -1:
          active = False

        field = Field(self.ui, (pos_x, pos_y), x, y, r, active=active)
        field.render()


class PlayingArea():
  def __init__(self, ui, dimensions):
    self.ui = ui
    self.x, self.y, self.w, self.h = dimensions

  def render(self):
    pygame.draw.rect(self.ui.screen, self.ui.game.next.color, (self.x,self.y,self.w,self.h))

    # Grid
    q = s.space_around_grid

    grid_x = self.x + self.w*q
    grid_y = self.y + self.h*q
    grid_w = self.w - 2 * self.w * q
    grid_h = self.h - 2 * self.h * q
    grid = Grid(self.ui, (grid_x,grid_y,grid_w,grid_h))
    grid.render()



class RightArea():
  def __init__(self, ui, dimensions):
    self.ui = ui
    self.x, self.y, self.w, self.h = dimensions

  def render(self):
    screen_width, screen_height = glob.dimensions


    # score labels
    lbl_scores = []
    for i,p in enumerate(self.ui.game.player):
      text = f"{p.display_name}: {self.ui.game.board.count(p.id)}"
      lbl = Label(self.ui.screen, (self.w/2+self.x, self.y+(i+1)*self.h*0.1), msg=text, fg=p.color, font_size=26)
      lbl.render()
      lbl_scores.append(lbl)
    
    # status label
    status = []
    if self.ui.game.game_state == GS.PLAYING:
      status = [f"Waiting for {self.ui.game.next.display_name}"]
    elif self.ui.game.game_state == GS.AFTER:
      if len(self.ui.game.winner) > 1:
        status = [f"It's a tie!"]
      else:
        if self.ui.game.invalid_turn == None:
          status = [f"{self.ui.game.winner[0].display_name} won!"]
        else:
          status = [f"{self.ui.game.winner[0].display_name} won,", f" because {self.ui.game.get_opponent(self.ui.game.winner[0]).display_name}", f" tried an invalid ", f"move: {str(self.ui.game.invalid_turn)}"]

    for i,text in enumerate(status):
      lbl_status = Label(self.ui.screen, (self.w/2+self.x, self.y+self.h*0.4+i*self.h*0.03), msg=text, fg=s.colors.get("fg"))
      lbl_status.render()


    # Restart
    def restart_game():
      self.ui.main.game = None

    btn_restart = Button(self.ui.screen, (self.x+self.w/2, self.y+self.h*0.9, self.w*0.9, self.h*0.1), cbg=(255,255,0), cfg=(0,0,0), chover=(255,0,0), msg="Restart", action=restart_game)
    btn_restart.render()
