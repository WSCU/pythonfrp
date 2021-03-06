from pythonfrp.Signal import *
from pythonfrp.Functions import *
from pythonfrp.Globals import *
from pythonfrp.Factory import *
from pythonfrp.World import *
import pythonfrp.Proxy as Proxy # Not sure why this needs to be like this?
from pythonfrp.StaticNumerics import *
from pythonfrp.Numerics import *

# Some of these imports are used as a pass through, with the idea being a developer only imports Engine


# This is the basic heartbeat update function.  The arguents are the elapsed time since
# the start of the program (in seconds) and a dictionary ef events that occur during the
# current heartbeat.

def heartbeat(ct, events):
#    print("Beat")
    #print("objects " + str(len(Globals.worldObjects)))
    Globals.dt = ct - Globals.currentTime
    Globals.currentTime = ct
    Globals.events = events
    Globals.newEvents = {}
    Globals.thunks = []

#    print("time steps: "+repr(ct))
#    for event in events:
#        print("Events: "+repr(event))
    reactions = []
    if Globals.resetFlag is not None:
        for m in Globals.worldObjects:
#            if not type(m) is World:
#            print ("Type of m is: " + str(type(m)))
            exit(m)
        # Reset the world object
#        World.world = World(name="world2")
#        world._name = "world2"
        world._alive = True
        world._gReactions = []
        Globals.newObjects.append(world)
        #Call the init FN thats passed into resetWorld
#        Globals.initFn()
#        Globals.initFn = None
        # Call the rest FN thats passed into resetWorld
        Globals.resetFlag()
        Globals.resetFlag = None
        
    for worldObject in Globals.worldObjects:
#        print("Updating object: " + repr(worldObject))
#        print(repr(worldObject))
#        print(repr(reactions))
#        print(worldObject._update)
        reactions.extend(worldObject._update())
    for thunk in Globals.thunks:
        thunk()
    for reaction in reactions:
        reaction.react()
#        print ("Engine each reaction: " + str(reaction))
#    print(len(reactions))
    for obj in Globals.newObjects:
#        print("Adding object: " + repr(obj))
        Globals.worldObjects.append(obj)
    Globals.newObjects = []
    for obj in Globals.worldObjects:
#        print("Initializing object: " + repr(obj))
        obj._initialize()


# This initializes the reactive engine - usually called at time 0

def initialize(ct = 0):
    """
    This function needs some work.
    will need to check the proxy module to find the right name for this initialize method
    make an initialize method that clears out all the variables and resets the clock
    """
    Globals.thunks = []
    Globals.currentTime = ct
    Globals.newModels = []
    Globals.worldObjects = []
    Globals.events = []

# Functions that are exported for ease of use: These exist inside the engine, but aren't so easy to find and may
# need to be used by devs






