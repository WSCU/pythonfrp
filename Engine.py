from . Signal import *
from . Functions import *
from . import Globals

# This is the basic heartbeat update function.  The arguents are the elapsed time since
# the start of the program (in seconds) and a dictionary ef events that occur during the
# current heartbeat.

def heartbeat(ct, events):
    #print "objects " + str(len(Globals.worldObjects))
    Globals.dt = ct - Globals.currentTime
    Globals.currentTime = ct
    Globals.events = events
    Globals.newEvents = {}
    Globals.thunks = []

    #print "time steps: "+repr(ct)
    #for event in events:
        #print "Events: "+repr(event)
    reactions = []
    for worldObject in Globals.worldObjects:
        #print("Updating object: " + repr(worldObject))
        #print(repr(worldObject))
        reactions.extend(worldObject._update())
    for thunk in Globals.thunks:
        thunk()
    for reaction in reactions:
        reaction.react()
    for obj in Globals.newObjects:
        #print("Adding object: " + repr(obj))
        Globals.worldObjects.append(obj)
    Globals.newObjects = []
    for obj in Globals.worldObjects:
        #print("Initializing object: " + repr(obj))
        obj._initialize()
    if Globals.resetFlag is not None:
        for m in Globals.worldObjects:
            exit(m)
        Globals.resetFlag()
        Globals.resetFlag = None

# This initializes the reactive engine - usually called at time 0

def initialize(ct = 0):
    """
    This funciton needs some work.
    will need to check the proxy module to find the right name for this initialize method
    make an initialize method that clears out all the variables and resets the clock
    """
    Globals.thunks = []
    Globals.currentTime = ct
    Globals.newModels = []
    Globals.worldObjects = []
    Globals.events = []

