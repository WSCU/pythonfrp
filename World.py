from pythonfrp import Proxy
from pythonfrp import Globals
from pythonfrp.Types import *
from pythonfrp import Numerics


def updateWorld(self):
    for f in world._updaters:
        f(self)


class World(Proxy.Proxy):
    def __init__(self, update=updateWorld):
        Proxy.Proxy.__init__(self, "world", update, {})
        # Create a world labeled 'world' with an updater that calls each signal's custom update


world = World() # Instance of World class
world._updaters = []


def addSignal(name, default, type, update):  # Add a signal to a given object, paired with a specified updater.
    world.__setattr__(name, default)
    world._types[name] = type
    world._updaters.append(update)


def resetWorld(continueFn=lambda: None):  # Makes all DirectGUI stuff invisible
    Globals.resetFlag = continueFn
