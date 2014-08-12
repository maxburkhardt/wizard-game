from sigil import Sigil
import sys


class Combo(Sigil):
    def __init__(self, name):
        if self.child_sigils == None:
            print "Error! Combo instantiated without child sigils!"
            sys.exit(1)
        Sigil.__init__(self, name, (0, 0, 0))

    def cast(self, game_state):
        for sigil in self.child_sigils:
            sigil.cast_game_state = game_state
            sigil.state = "COMBO_CASTING"
        Sigil.cast(self, game_state)

    def on_cast(self):
        for sigil in self.child_sigils:
            sigil.remove()


class BirdFehuCombo(Combo):
    def __init__(self, sigils):
        self.child_sigils = sigils
        self.name = "birdfehu"
        self.cast_time = 3
        Combo.__init__(self, "BirdFehu")

    def on_cast(self):
        print self.name, "was cast!"
        Combo.on_cast(self)


class BirdBirdFehuCombo(Combo):
    def __init__(self, sigils):
        self.child_sigils = sigils
        self.name = "birdbirdfehu"
        self.cast_time = 4
        Combo.__init__(self, "BirdBirdFehu")

    def on_cast(self):
        print self.name, "was cast!"
        Combo.on_cast(self)


VALID_COMBOS = {"birdfehu": BirdFehuCombo, "birdbirdfehu": BirdBirdFehuCombo}


def select_combo(combo_string):
    print "selecting combo:", combo_string
    try:
        return VALID_COMBOS[combo_string.lower()]
    except KeyError:
        return None
