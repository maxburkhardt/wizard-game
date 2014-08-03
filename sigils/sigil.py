import pygame
import time
from game_util import *

class Sigil(pygame.sprite.Sprite):
  def __init__(self, name, color):
    pygame.sprite.Sprite.__init__(self)
    #self.image, self.rect = load_image(sprite)
    #self.rect.x = 10
    #self.rect.y = 10
    self.image = pygame.Surface([100, 150])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.state = "AVAILABLE"

  def update(self):
    if self.state == "AVAILABLE":
      self.rect.x -= 1 
    elif self.state == "CASTING":
      delta = time.time() - self.start_cast
      if delta > self.cast_time:
        self.state = "FINISHED"
        self.on_cast()
        self.cast_game_state["player"].spellbook.remove(self)
        self.cast_game_state["all_sprites"].remove(self)
        self.cast_game_state["player"].layout_sigils()

  def cast(self, game_state):
    if self.state == "CASTING":
      return
    self.state = "CASTING"
    self.start_cast = time.time()
    self.cast_game_state = game_state
