# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import sys, os
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

currentTime = 0 # The current global time
cam = None # The camera object, exported to the user variable cam
panda3dCamera = camera # The original Panda3d camera
direct = DirectObject()       # The directObj() used to communicate with the mouse / kayboard
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
nextNE2dY = .95 # Positioning for 2-D controls
nextNW2dY = .95

mousePos = None # Last location of the mouse
nextModelId = 0
observers = {} #dictionary of observers
dt = 1 #global delta time
#world = dict() #dictionary of global signals
sl = {}
eventListenerCache = {}

resetFlag = None

# Global GUI signals

lbutton = False # Left button state
rbutton = False # Right button state
rbuttonPull = None # "Pulled" 2-D Point for the right button
lbuttonPull = None # "Pulled" 2-D point for the left button


# Used to identify signals

nextSignalRef = 0

texture = None # Used to communicate with particle effect code from particle panel

collections = {}
collectionReactions = {"when1" : {}, "when": {}, "react": {}, "react1": {}}
#osType = platform.system() # OS That is being used. # NotReturning Correct osType should be Windows Insted of Java.
#print osType
#osType = 'Linux'
#pandaPath = os.getcwd()
#pandaPath = "/c/panda/lib"
pandaPath = "/c/Reactive-Engine/src/lib"
#pandaPath = "/c/panda/lib"
#pandaPath = "/c/users/outcast/documents/GitHub/Reactive-Engine/src/lib" #this is for Grahams personal machine
'''
osType = 'Windows'
if osType is 'Linux':
# print "we're on Linux"
pandaPath = os.getcwd()+"/lib/" # Since we are on a Linux system we will now use a linux file path.
if osType is 'Windows':
# print "we're on Windows" # Since we are on a Windows system we will use the windows file path.
pandaPath = os.getcwd()+"/lib/"
'''
