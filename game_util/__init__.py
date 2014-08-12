import os
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    return image, image.get_rect()


def generate_ui():
    background = pygame.Surface((1066, 600)).convert()
    background.fill((250, 250, 250))
    pygame.draw.line(background, BLACK, (0, 200), (1066, 200), 4)
    pygame.draw.line(background, BLACK, (0, 400), (1066, 400), 4)
    for i in xrange(8):
        pygame.draw.rect(background, BLACK, (15 + i * 133, 25, 100, 150), 1)
        pygame.draw.rect(background, BLACK, (15 + i * 133, 425, 100, 150), 1)
    return background
