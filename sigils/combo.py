from sigil import Sigil
import sys
import game_state
import client_networking


class Combo(Sigil):
    def __init__(self, name):
        if self.child_sigils == None:
            print "Error! Combo instantiated without child sigils!"
            sys.exit(1)
        Sigil.__init__(self, name, (0, 0, 0))

    def cast(self):
        all_uuids = ""
        for sigil in self.child_sigils:
            sigil.state = "COMBO_CASTING"
            all_uuids += " " + sigil.uuid
        client_networking.send_queue.put("CAST " + all_uuids)

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
