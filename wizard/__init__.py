import pygame 

class Wizard:
  def __init__(self):
    self.health = 100
    self.spellbook = []

  def can_get_sigil(self):
    return len(self.spellbook) <= 7

  def get_available_sigil_position(self):
    return (15 + len(self.spellbook) * 133, 425)

  def layout_sigils(self):
    i = 0
    for sigil in self.spellbook:
      sigil.rect.x = 15 + (i * 133)
      i += 1
