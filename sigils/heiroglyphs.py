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

    def on_cast_server(self):
        self.owner.wizard.opponent.modify_health(-10)

