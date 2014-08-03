#!/usr/bin/env python
import os
import sys
import pygame
import random
from pygame.locals import *
from game_util import *
from sigils import futhark, heiroglyphs

def get_random_sigil():
    return random.choice([futhark.Fehu, heiroglyphs.Bird])

def generate_sigils(group):
    new_sigil = get_random_sigil()()
    new_sigil.rect.x = 966
    new_sigil.rect.y = 225
    group.add(new_sigil)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1066, 600))
    pygame.display.set_caption("Wizards!")

    screen.blit(generate_ui(), (0, 0))
    pygame.display.flip()

    sigil_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    sigil_appearance_count = 0

    running = True
    while running:
        if sigil_appearance_count % 180 == 0:
            generate_sigils(sigil_sprites)
        sigil_appearance_count += 1
        sigil_sprites.update()
        screen.blit(generate_ui(), (0, 0))
        sigil_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                running = False
                break
    pygame.quit()
