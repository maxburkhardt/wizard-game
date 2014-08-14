__author__ = 'maxb'
from sigils import heiroglyphs, futhark

def sigil_serialize(sigil):
    return sigil.name + ":" + sigil.uuid


def sigil_deserialize(sigil):
    name, uuid = sigil.split(":")
    new_sigil = None
    if name == "bird":
        new_sigil = heiroglyphs.Bird()
        new_sigil.uuid = uuid
    elif name == "fehu":
        new_sigil = futhark.Fehu()
        new_sigil.uuid = uuid
    return new_sigil
