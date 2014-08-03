#!/usr/bin/env python
import os
import sys
import pygame
from pygame.locals import *
from sigils import futhark

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1066, 600))
    pygame.display.set_caption("Wizards!")

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((250, 250, 250))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    sigil_sprites = pygame.sprite.Group()
    #allsprites = pygame.sprite.RenderPlain(sigil_sprites)
    clock = pygame.time.Clock()

    running = True
    while running:
        sigil_sprites.update()
        screen.blit(background, (0, 0))
        sigil_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                running = False
                break
            elif event.type == KEYDOWN and event.key == K_SPACE:
                f = futhark.Fehu()
                sigil_sprites.add(f)
    pygame.quit()
