from . import Proxy
from . import Globals
from . Types import *
from . import Numerics

def updateWorld(self):
    for f in world._updaters:
        f(self)

class World(Proxy.Proxy):
    def __init__(self, update = updateWorld):
        Proxy.Proxy.__init__(self, "world", update, {})

world = World()
world._updaters = []

def addSignal(name,default,type,update): #Add a signal to a given object, paired with a specified updater
    world.__setattr__(name,default)
    world._types[name]= type
    world._updaters.add(update)

def resetWorld(continueFn = lambda: None):
    Globals.resetFlag=continueFn
    #Makes all DirectGUI stuff invisible

