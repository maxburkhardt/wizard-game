from sigil import Sigil
import game_state


class Futhark(Sigil):
    def __init__(self, name):
        self.language = "futhark"
        self.color = (0, 0, 255)
        Sigil.__init__(self, name, self.color)


class Fehu(Futhark):
    def __init__(self):
        self.name = "fehu"
        self.cast_time = 1
        Futhark.__init__(self, self.name)

    def on_cast_server(self):
        self.owner.wizard.modify_health(10)
