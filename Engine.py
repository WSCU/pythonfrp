import unittest
import sched, time
#from StateMachine import *
from Externals import initEvents, pollGUI
from Signal import *
from Functions import *
import World
import Globals
from direct.task import Task

def heartBeat(ct, events):
    #print "objects " + str(len(Globals.worldObjects))
    Globals.dt = ct - Globals.currentTime
    Globals.currentTime = ct
    Globals.events = events
    Globals.newEvents = {}
    Globals.thunks = []

    pollGUI()

    #print "time steps: "+repr(ct)
    #for event in events:
        #print "Events: "+repr(event)
    reactions = []
    for worldObject in Globals.worldObjects:
        #print("Updating object: " + repr(worldObject))
        #print repr(worldObject)
        reactions.extend(worldObject._update())
    for f in Globals.thunks:
        f()
    for r in reactions:
        r.react()
    for obj in Globals.newObjects:
        #print("Adding object: " + repr(obj))
        Globals.worldObjects.append(obj)
    Globals.newObjects = []
    for obj in Globals.worldObjects:
        #print("Initializing object: " + repr(obj))
        obj._initialize()
    if Globals.resetFlag is not None:
        for m in Globals.worldObjects:
            if m is not World.world and m is not World.camera:
                exit(m)
        Globals.nextNE2dY = .95         # Positioning for 2-D controls - old controls should be gone
        Globals.nextNW2dY = .95
        Proxy.clearReactions(World.world)
        Proxy.clearReactions(World.camera)
        Globals.resetFlag()
        Globals.resetFlag = None
#will need to check the proxy module to find the right name for this initialize method
#make an initialize method that clears out all the variables and resets the clock
def initialize(ct):
    Globals.thunks = []
    Globals.currentTime = 0 #Not sure if this should be 0 or CT
    Globals.newModels = []
    Globals.worldObjects = {}
    Globals.events = []
    Globals.panda3dCamera = camera #Panda3-D built in camera
    Globals.world = world

def engine(ct):
    #Initialize all signals (signalF.start)
    #set the time to 0
    #get events and clear thunks
    Globals.currentTime = ct
    initEvents()
    taskMgr.add(stepTask, 'PandaClock')
    run()
def stepTask(task):
    heartBeat(task.time, Globals.newEvents) # The task contains the elapsed time
    return Task.cont

