import pygame
from game_util import *

class Sigil(pygame.sprite.Sprite):
  def __init__(self, sprite):
    pygame.sprite.Sprite.__init__(self)
    # self.image, self.rect = load_image(sprite, -1)
    # self.rect.x = 10
    # self.rect.y = 10
    self.image = pygame.Surface([30, 30])
    self.image.fill((255,0,0))
    self.rect = self.image.get_rect()
    # screen = pygame.display.get_surface()
    # self.area = screen.get_rect()
    # self.rect.topleft = 10, 10

  def update(self):
    self.rect.x += 1 
