import game_state


class Wizard:
    def __init__(self):
        self.health = 100
        self.spellbook = []
        self.combo_select = []
        self.opponent = None
        self.health_changed = False

    def can_get_sigil(self):
        return len(self.spellbook) <= 7

    def get_available_sigil_position(self):
        y_offset = 125 if game_state.opponent == self else 525
        return (15 + len(self.spellbook) * 133, y_offset)

    def layout_sigils(self):
        i = 0
        for sigil in self.spellbook:
            sigil.rect.x = 15 + (i * 133)
            i += 1

    def clear_selection(self):
        for sigil in self.combo_select:
            sigil.deselect()
        self.combo_select = []

    def modify_health(self, amount):
        self.health_changed = True
        self.health += amount
