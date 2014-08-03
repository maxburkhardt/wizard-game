#!/usr/bin/env python
import os
import sys
import pygame
import random
from pygame.locals import *
from game_util import *
from wizard import Wizard
from sigils import futhark, heiroglyphs

def get_random_sigil():
    return random.choice([futhark.Fehu, heiroglyphs.Bird])

def generate_sigils(groups):
    new_sigil = get_random_sigil()()
    new_sigil.rect.x = 966
    new_sigil.rect.y = 225
    for group in groups:
        group.add(new_sigil)

if __name__ == "__main__":

    # initialize pygame & display
    pygame.init()
    screen = pygame.display.set_mode((1066, 600))
    pygame.display.set_caption("Wizards!") 
    screen.blit(generate_ui(), (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()

    # initialize sprites for sigils
    all_sprites = pygame.sprite.Group()
    available_sprites = pygame.sprite.Group() 
    sigil_appearance_count = 0

    # set up player info
    player = Wizard()
    opponent = Wizard()
    game_state = {"player": player, "opponent": opponent, "all_sprites":
            all_sprites}

    # begin main loop
    running = True
    while running:
        if sigil_appearance_count % 180 == 0:
            generate_sigils([all_sprites, available_sprites])
            out_of_bounds = [s for s in available_sprites if s.rect.x <= -150]
            for sigil in out_of_bounds:
                available_sprites.remove(sigil)
        sigil_appearance_count += 1
        all_sprites.update()
        screen.blit(generate_ui(), (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                    event.key == K_ESCAPE):
                running = False
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # handle clicking on available sigil
                if player.can_get_sigil():
                    clicked_sprites = [s for s in available_sprites if
                            s.rect.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        spellbook_position = player.get_available_sigil_position()
                        sprite.rect.x = spellbook_position[0]
                        sprite.rect.y = spellbook_position[1]
                        available_sprites.remove(sprite)
                        player.spellbook.append(sprite)
                        sprite.state = "CLAIMED"

                # handle clicking on a sigil in your spellbook
                clicked_in_spellbook = [s for s in player.spellbook if
                        s.rect.collidepoint(pos)]
                for sprite in clicked_in_spellbook:
                    sprite.cast(game_state)

    pygame.quit()
