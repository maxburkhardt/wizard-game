import pygame
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
