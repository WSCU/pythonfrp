from . import Proxy
from . import Globals
from . Types import *
from . import Numerics

def updateWorld(self):
    pass
    #c = self._get("color")
    #base.setBackgroundColor(c.r, c.g, c.b) # What is base?
    #Maybe set this in panda specific aswell?


class World(Proxy.Proxy):
    def __init__(self, update):
        Proxy.Proxy.__init__(self, "world", update, {"color": colorType, "gravity": p3Type})
        #self.color = gray # Set this in panda specific area
        self.gravity = Numerics.p3(0,0,-1)


# Clear out the world.  This doesn't reset the global time or camera position.
def resetWorld(continueFn):
    Globals.resetFlag=continueFn
    # Should make all DirectGUI stuff invisible
    print("done")
