import time
from game_util import *
import sigil_overlay
import game_state
import uuid
import client_networking


class Sigil(pygame.sprite.Sprite):
    def __init__(self, name, color):
        pygame.sprite.Sprite.__init__(self)
        # self.image, self.rect = load_image(sprite)
        #self.rect.x = 10
        #self.rect.y = 10
        self.image = pygame.Surface([100, 150])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.state = "AVAILABLE"
        self.owner = None
        self.overlay = None
        self.uuid = str(uuid.uuid4())

    def remove(self):
        if self in game_state.player.spellbook:
            game_state.player.spellbook.remove(self)
        game_state.all_sprites.remove(self)
        game_state.player.layout_sigils()

    def update(self):
        if self.state == "AVAILABLE":
            self.rect.x -= 1
        elif self.state == "CASTING":
            delta = time.time() - self.start_cast
            if delta > self.cast_time:
                self.state = "FINISHED"
                self.on_cast()
                self.remove()
        elif self.state == "COMBO_CASTING":
            # TODO animation here?
            pass

    def claim(self):
        print "Sending claim message"
        client_networking.send_queue.put("CLAIM " + self.uuid)
        self.state = "CLAIMING"

    def execute_claim(self, player):
        spellbook_position = player.get_available_sigil_position()
        self.rect.x = spellbook_position[0]
        self.rect.y = spellbook_position[1]
        game_state.available_sprites.remove(self)
        player.spellbook.append(self)
        self.state = "CLAIMED"
        self.owner = player

    def cast(self):
        if self.state == "CASTING" or self.state == "COMBO_CASTING":
            return
        self.state = "CASTING"
        self.start_cast = time.time()

    def select(self):
        if self.overlay:
            return
        overlay = sigil_overlay.SigilOverlay()
        overlay.rect.x = self.rect.x
        overlay.rect.y = self.rect.y
        self.overlay = overlay
        game_state.sigil_overlay_sprites.add(overlay)

    def deselect(self):
        game_state.sigil_overlay_sprites.remove(self.overlay)
        self.overlay = None

    def __str__(self):
        return self.name
