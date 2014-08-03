from sigil import Sigil

class FutharkSigil(Sigil):
  def __init__(self, sprite):
    self.language = "futhark"
    self.color = "blue"
    Sigil.__init__(self, sprite)

class Fehu(FutharkSigil):
  def __init__(self):
    self.name = "fehu"
    FutharkSigil.__init__(self, "fehu.png")
