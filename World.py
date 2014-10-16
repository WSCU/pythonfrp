from . import Proxy
from . import Globals
import math
from . Types import *
from . StaticNumerics import *
from . import Numerics

def updateWorld(self):
    c = self._get("color")
    base.setBackgroundColor(c.r, c.g, c.b)


class World(Proxy.Proxy):

    def __init__(self):
        Proxy.Proxy.__init__(self, "world", updateWorld, {"color": colorType, "gravity": p3Type})
        self.color = gray
        self.gravity = Numerics.p3(0,0,-1)

world = World()

# Clear out the world.  This doesn't reset the global time or camera position.
def resetWorld(continueFn):
    Globals.resetFlag=continueFn
    # Should make all DirectGUI stuff invisible
    print("done")
