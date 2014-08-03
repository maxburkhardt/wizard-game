import pygame 

class Wizard:
  def __init__(self):
    self.health = 100
    self.spellbook = pygame.sprite.Group()

  def can_get_sigil(self):
    return len(self.spellbook) <= 7

  def get_available_sigil_position(self):
    return (15 + len(self.spellbook) * 133, 425)
