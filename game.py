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
    sprite_uuid_map[sigil.uuid] = new_sigil
    for group in groups:
        group.add(new_sigil)


if __name__ == "__main__":
    # initialize sigil infrastructure
    sigil_appearance_count = 0
    sprite_uuid_map = {}

    # set up player info
    player = Wizard()
    opponent = Wizard()
    game_state.player = player
    game_state.opponent = opponent
    game_state.all_sprites = pygame.sprite.Group()
    game_state.available_sprites = pygame.sprite.Group()
    game_state.sigil_overlay_sprites = pygame.sprite.Group()

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
            split_input = map(str.strip, message.split(" "))
            command = split_input[0]
            if command == "NEW":
                generate_sigils([game_state.all_sprites, game_state.available_sprites], sigil_deserialize(split_input[1]))
            elif command == "CLAIMED":
                claimed = sprite_uuid_map[split_input[2]]
                if split_input[1] == client_networking.client_uuid:
                    # this means we got it
                    claimed.execute_claim(player)
                else:
                    # this means we didn't
                    claimed.execute_claim(opponent)
            elif command == "COMPLETE":
                # TODO no combo support yet
                print "Cast of", sprite_uuid_map[split_input[1]].name, "complete"
                sprite_uuid_map[split_input[1]].remove()
            elif command == "HEALTH":
                if split_input[1] == client_networking.client_uuid:
                    player.health = int(split_input[2])
                else:
                    opponent.health = int(split_input[2])
        # every 3 seconds we'll look for sigils off the screen and clean them up
        if sigil_appearance_count % 180 == 0:
            out_of_bounds = [s for s in game_state.available_sprites if s.rect.x <= -150]
            for sigil in out_of_bounds:
                game_state.available_sprites.remove(sigil)
        sigil_appearance_count += 1

        # update all sprites and draw the UI, also keep the framerate synced
        game_state.all_sprites.update()
        game_state.sigil_overlay_sprites.update()
        screen.blit(generate_ui(), (0, 0))
        game_state.all_sprites.draw(screen)
        game_state.sigil_overlay_sprites.draw(screen)
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
                    clicked_sprites = [s for s in game_state.available_sprites if
                                       s.rect.collidepoint(pos)]
                    for sprite in clicked_sprites:
                        # we clear combo select if you click something else
                        player.clear_selection()
                        sprite.claim()

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
                                game_state.all_sprites.add(selected_combo)
                                selected_combo.cast()
                            else:
                                player.clear_selection()
                    # otherwise, we do special group selection things
                    else:
                        player.combo_select.append(sprite)
                        sprite.select()

    pygame.quit()
