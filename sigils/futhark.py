from sigil import Sigil

class Futhark(Sigil):
  def __init__(self, name):
    self.language = "futhark"
    self.color = (0, 0, 255)
    Sigil.__init__(self, name, self.color)

class Fehu(Futhark):
  def __init__(self):
    self.name = "fehu"
    Futhark.__init__(self, self.name)
