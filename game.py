#!/usr/bin/env python
import os
import sys
import pygame
import random
from pygame.locals import *
from game_util import *
from wizard import Wizard
from sigils import futhark, heiroglyphs, combo
import game_state

def get_random_sigil():
    return random.choice([futhark.Fehu, heiroglyphs.Bird])


def generate_sigils(groups):
    new_sigil = get_random_sigil()()
    new_sigil.rect.x = 966
    new_sigil.rect.y = 325
    for group in groups:
        group.add(new_sigil)


if __name__ == "__main__":
    # initialize sprites for sigils
    all_sprites = pygame.sprite.Group()
    available_sprites = pygame.sprite.Group()
    sigil_overlay_sprites = pygame.sprite.Group()
    sigil_appearance_count = 0

    # set up player info
    player = Wizard()
    opponent = Wizard()
    game_state.player = player
    game_state.opponent = opponent
    game_state.all_sprites = all_sprites
    game_state.sigil_overlay_sprites = sigil_overlay_sprites

    # initialize pygame & display
    pygame.init()
    screen = pygame.display.set_mode((1066, 800))
    pygame.display.set_caption("Wizards!")
    screen.blit(generate_ui(), (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()

    # begin main loop
    running = True
    combo_select = False
    while running:
        if sigil_appearance_count % 180 == 0:
            generate_sigils([all_sprites, available_sprites])
            out_of_bounds = [s for s in available_sprites if s.rect.x <= -150]
            for sigil in out_of_bounds:
                available_sprites.remove(sigil)
        sigil_appearance_count += 1
        all_sprites.update()
        sigil_overlay_sprites.update()
        screen.blit(generate_ui(), (0, 0))
        all_sprites.draw(screen)
        sigil_overlay_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                              event.key == K_ESCAPE):
                running = False
                break
            elif event.type == KEYDOWN and event.key == K_LSHIFT:
                combo_select = True
            elif event.type == KEYUP and event.key == K_LSHIFT:
                combo_select = False
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # handle clicking on available sigil
                if player.can_get_sigil():
                    clicked_sprites = [s for s in available_sprites if
                                       s.rect.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        # we clear combo select if you click something else
                        player.clear_selection()
                        spellbook_position = player.get_available_sigil_position()
                        sprite.rect.x = spellbook_position[0]
                        sprite.rect.y = spellbook_position[1]
                        available_sprites.remove(sprite)
                        player.spellbook.append(sprite)
                        sprite.state = "CLAIMED"
                        sprite.owner = player

                # handle clicking on a sigil in your spellbook
                clicked_in_spellbook = [s for s in player.spellbook if
                                        s.rect.collidepoint(pos)]
                for sprite in clicked_in_spellbook:
                    # if we're not selecting spells for a combo, proceed as normal
                    if not combo_select:
                        # if the player clicks a non-combo sigil, cast it
                        if sprite not in player.combo_select:
                            # we clear combo select if you click something else
                            player.clear_selection()
                            sprite.cast()
                        # otherwise, cast the combo it's in
                        else:
                            # this will make a combo object based off the
                            # sorted list of sigil names
                            combo_type = combo.select_combo("".join(sorted(map(str, player.combo_select))))
                            if combo_type:
                                selected_combo = combo_type(player.combo_select)
                                player.clear_selection()
                                # this makes the combo sprite not appear
                                selected_combo.rect.x = -100
                                selected_combo.rect.y = -150
                                all_sprites.add(selected_combo)
                                selected_combo.cast()
                            else:
                                player.clear_selection()
                    # otherwise, we do special group selection things
                    else:
                        player.combo_select.append(sprite)
                        sprite.select()

    pygame.quit()
