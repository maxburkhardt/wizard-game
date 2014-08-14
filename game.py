#!/usr/bin/env python
import os
import sys
import pygame
import random
from pygame.locals import *
from game_util import *
from sigil_util import *
from wizard import Wizard
from sigils import futhark, heiroglyphs, combo
import game_state
import client_networking
import time


def generate_sigils(groups, sigil):
    new_sigil = sigil
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

    # initialize networking
    client_networking.establish_connection("127.0.0.1", 1111)
    print "Establishing connection to server and waiting for game to start."
    while True:
        if not client_networking.recv_queue.empty():
            message = client_networking.recv_queue.get()
            if message == "READY":
                break
        time.sleep(1)


    # begin main loop
    running = True
    combo_select = False
    while running:
        # check for messages from the server
        if not client_networking.recv_queue.empty():
            message = client_networking.recv_queue.get()
            command, data = message.split(" ")
            if command == "NEW":
                generate_sigils([all_sprites, available_sprites], sigil_deserialize(data))
        # every 3 seconds we'll look for sigils off the screen and clean them up
        if sigil_appearance_count % 180 == 0:
            out_of_bounds = [s for s in available_sprites if s.rect.x <= -150]
            for sigil in out_of_bounds:
                available_sprites.remove(sigil)
        sigil_appearance_count += 1

        # update all sprites and draw the UI, also keep the framerate synced
        all_sprites.update()
        sigil_overlay_sprites.update()
        screen.blit(generate_ui(), (0, 0))
        all_sprites.draw(screen)
        sigil_overlay_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        # event handling
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
