__author__ = 'maxb'
from sigils import heiroglyphs, futhark, combo

def sigil_serialize(sigil):
    return sigil.name + ":" + sigil.uuid


def sigil_deserialize(sigil):
    name, uuid = sigil.split(":")
    new_sigil = None
    if name == "bird":
        new_sigil = heiroglyphs.Bird()
    elif name == "fehu":
        new_sigil = futhark.Fehu()
    elif name == "birdfehu":
        new_sigil = combo.BirdFehuCombo(1)
    elif name == "birdbirdfehu":
        new_sigil = combo.BirdBirdFehuCombo(1)
    new_sigil.uuid = uuid
    return new_sigil
