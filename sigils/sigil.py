import time
from game_util import *
import sigil_overlay


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
        self.overlay = None

    def remove(self):
        if self in self.cast_game_state["player"].spellbook:
            self.cast_game_state["player"].spellbook.remove(self)
        self.cast_game_state["all_sprites"].remove(self)
        self.cast_game_state["player"].layout_sigils()

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

    def cast(self, game_state):
        if self.state == "CASTING" or self.state == "COMBO_CASTING":
            return
        self.state = "CASTING"
        self.start_cast = time.time()
        self.cast_game_state = game_state

    def select(self, game_state):
        if self.overlay:
            return
        overlay = sigil_overlay.SigilOverlay()
        overlay.rect.x = self.rect.x
        overlay.rect.y = self.rect.y
        self.overlay = overlay
        game_state["sigil_overlay_sprites"].add(overlay)

    def deselect(self, game_state):
        game_state["sigil_overlay_sprites"].remove(self.overlay)
        self.overlay = None

    def __str__(self):
        return self.name
