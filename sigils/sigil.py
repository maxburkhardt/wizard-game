import pygame
from game_util import *

class Sigil(pygame.sprite.Sprite):
  def __init__(self, name, color):
    pygame.sprite.Sprite.__init__(self)
    #self.image, self.rect = load_image(sprite)
    #self.rect.x = 10
    #self.rect.y = 10
    self.image = pygame.Surface([30, 30])
    self.image.fill(color)
    self.rect = self.image.get_rect()

  def update(self):
    self.rect.x += 1 
