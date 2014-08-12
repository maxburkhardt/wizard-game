__author__ = 'maxb'
import pygame


class SigilOverlay(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 150])
        self.image.fill((255, 255, 255))
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
