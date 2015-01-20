currentTime = 0 # The current global time
objectNames = None # Hands out unique name to every panda object
eventSignals = {}
newEvents = {} # Events that are being sensed but not reacted to yet
events = {} # This is a dictionary of all events posted in the previous tick interval
simEvents = [] # Simulated events for use in the test engine.
reactEvents = [] # Reactions that are not part of an object
eventSignals = {} # This is a dictionary of event values received since the last tick
newObjects = [] # The new list of active models assembled at every tick
worldObjects = [] # list of all active objects
thunks = []
tracking = False

collections = {}
collectionReactions = {"when1" : {}, "when": {}, "react": {}, "react1": {}}

observers = {} #dictionary of observers
dt = 1 #global delta time
#world = dict() #dictionary of global signals
sl = {} # What is this?
eventListenerCache = {}

resetFlag = None
# Used to identify signals

nextSignalRef = 0

