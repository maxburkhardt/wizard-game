import os
import pygame
from pygame.locals import *
import game_state

BLACK = (0, 0, 0)


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    return image, image.get_rect()

def draw_health(font, which_player, pos, surface):
    health = font.render(str(which_player.health), True, BLACK)
    healthpos = health.get_rect()
    healthpos.x = pos[0]
    healthpos.y = pos[1]
    surface.blit(health, healthpos)



def generate_ui():
    background = pygame.Surface((1066, 800)).convert()
    background.fill((250, 250, 250))
    pygame.draw.line(background, BLACK, (0, 300), (1066, 300), 4)
    pygame.draw.line(background, BLACK, (0, 500), (1066, 500), 4)
    for i in xrange(8):
        pygame.draw.rect(background, BLACK, (15 + i * 133, 125, 100, 150), 1)
        pygame.draw.rect(background, BLACK, (15 + i * 133, 525, 100, 150), 1)

    # draw health UI
    font = pygame.font.Font(None, 36)
    draw_health(font, game_state.opponent, (25, 25), background)
    draw_health(font, game_state.player, (25, 725), background)
    return background

