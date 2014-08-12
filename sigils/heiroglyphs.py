from sigil import Sigil
import game_state


class Heiroglyph(Sigil):
    def __init__(self, name):
        self.language = "heiroglyphs"
        self.color = (255, 0, 0)
        Sigil.__init__(self, name, self.color)


class Bird(Heiroglyph):
    def __init__(self):
        self.name = "bird"
        self.cast_time = 2
        Heiroglyph.__init__(self, self.name)

    def on_cast(self):
        if self.owner == game_state.player:
            game_state.opponent.health -= 10
        else:
            game_state.player.health -= 10
        print "bird finished casting!"
