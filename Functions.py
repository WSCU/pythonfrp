#Collection of useful and necessary functions used in the Reactive Engine.
from Signal import *
from Factory import *
from StaticNumerics import zero
from Errors import *
import World
import Proxy

import Globals

def now(s):
    if isinstance(s, ObserverF):
        return s.get()
    return None  # Should be an error

def integralInternal(x):  # This reurns the special value Zero() at the initial sampling.
                          # This should always be added to something so that the Zero is never
                          # returned to user code.  Only the __add__ method inthe Zero class is
                          # supported so only addition will remove the Zrto
    def initIntegral(s):
        s.value = zero
    def thunk(sm):
        i = sm.i.now()
        #print "integral "+ str(sm.state) + " " + str(i) + " " + str(Globals.dt)
        sm.value = sm.value + i * Globals.dt
        #print sm.state
    def integralf(sm):
        Globals.thunks.append(lambda: thunk(sm))
        return sm.value
    return StateMachineF(initIntegral, maybeLift(x), integralf)

def integral(x, v0):
    return integralInternal(x) + v0

def deriv(sig, init = zero):
    def initDeriv(sm):
        sm.value = init
        sm.first = True
    def thunk(sm):
        i = sm.i.now()
        print str(i)
        if not sm.first:
            sm.value = (i - sm.previous) * (1/Globals.dt)
        else:
            sm.first = False
        sm.previous = i
    def derivf(sm):
        Globals.thunks.append(lambda: thunk(sm))
        return sm.value
    return StateMachineF(initDeriv, maybeLift(sig), derivf)

def tag(v,evt):
    return lift("tag", lambda e: EventValue(v) if e.occurs() else noEvent)(evt)

def tagMap(fn, evt):
    return lift("tag", lambda e: EventValue(fn(e.value)) if e.occurs() else noEvent) (evt)

def tagCount(evt):
    def initTag(sm):
        sm.count = 0
    def tagFN(sm):
        i = sm.i.now()
        checkEvent(i, "tag")
        if not i.occurs():
            sm.value = noEvent
        else:
            sm.count += 1
            sm.value = EventValue(sm.count)
    return StateMachineF(initTag, maybeLift(evt), tagFN)

def tagList(l, evt):
    return tagMap(lambda i: l[i%len(l)], tagCount(evt))

def hold(iv, evt): #Holds the last value of an Event
    def initHold(sm):
        sm.value = iv
    def holdFN(sm):
        i = sm.i.now();
        checkEvent(i, "hold")
        if i.occurs():
            sm.value = i.value;
    return StateMachineF(initHold, maybeLift(evt),holdFN)

def accum(iv, evt): #accumulates the value of a signal over time
    def initAccum(sm):
        sm.value = iv
    def accumFN(sm):
        s = sm.i.now();
        checkEvent(s, "accum")
        if s.occurs():
            sm.value = s.value(sm.value)
    return StateMachineF(initAccum, maybeLift(evt), accumFN)

def getCollection(m):
    if type(m) is str:
        try:
            return Globals.collections[m]
        except KeyError:
            # There may not be any model in a collection yet
            # print ("No collection with the name: " + m + " returning empty list")
            return []
    else:
        return [m]

def hitE(m1, m2, trace = False):
    def hitFN(o):
        ml1 = getCollection(m1)
        ml2 = getCollection(m2)
        res = []
        for m in ml1:
            for e in ml2:
                if m is not e and m._touches(e, trace = trace):
                    res.append((m,e))
        if res == []:
            return noEvent
        return EventValue(res)
    return ObserverF(hitFN)

def hit(m1, m2, reaction, trace = False):
    def hitReaction(m,v):
        for p in v:
            reaction(p[0], p[1])
    react(m1, hitE(m1, m2, trace = trace), hitReaction)

def hit1(m1, m2, reaction, trace = False):
    react1(m1, hitE(m1, m2, trace = trace), reaction)

def saveForCollection(type, m, when, what):
    if m not in Globals.collectionReactions[type]:
        Globals.collectionReactions[type][m] = []
    Globals.collectionReactions[type][m].append([when, what])

def react(m, when, what = None):
    if what is None:
        what = when
        when = m
        m = World.world
    if type(m) is str:
        saveForCollection("react", m, when, what)
    coll = getCollection(m)
    for proxy in coll:
        proxy._react(when, what)

def react1(m, when, what = None):
    if what is None:
        what = when
        when = m
        m = World.world
    if type(m) is str:
        saveForCollection("react1", m, when, what)
    coll = getCollection(m)
    for proxy in coll:
        proxy._react1(when, what)

def when(m, when, what = None):
    if what is None:
        what = when
        when = m
        m = World.world
    if type(m) is str:
        saveForCollection("when", m, when, what)
    coll = getCollection(m)
    for proxy in coll:
        proxy._react(happen(when), what)

def when1(m, when, what = None):
    if what is None:
        what = when
        when = m
        m = World.world
    if type(m) is str:
        saveForCollection("when1", m, when, what)
    coll = getCollection(m)
    for proxy in coll:
        proxy._react1(happen(when), what)

def exit(x):
    if isinstance(x, Proxy.Proxy):
        x._exit()

def localtime():
    def ltF(o):
        return Globals.currentTime - o.startTime
    return ObserverF(ltF, type = numType)

localTime = localtime()

def clock(step, start = 0, end = 1000000):
    def initClock(sm):
        sm.i = 0
        sm.eventTime = Globals.currentTime + start
        sm.step = step
        sm.end = Globals.currentTime + end
        sm.value = noEvent
    def clockFN(sm): # tracks and updates engine time
        # state is the previous value of the clock
        if Globals.currentTime >= sm.eventTime and Globals.currentTime < sm.end:
            sm.eventTime = sm.eventTime + sm.step
            sm.value = EventValue(sm.i)
            sm.i = sm.i + 1
        # add the current clock signal to the list of fast updating signals (which doesn't exist yet)
        else:
            sm.value = noEvent
    return StateMachineF(initClock, maybeLift(0), clockFN)

#make a clock signal too. Clock will control the heartbeat: make the heartbeat every second
time = ObserverF(lambda x: Globals.currentTime, type = numType)

def delay(n, absoluteTime = False):
    def initClock(sm):
        sm.eventTime = n + (0 if absoluteTime else Globals.currentTime)
        sm.value = noEvent
        sm.fired = False
    def clockFN(sm): # tracks and updates engine time
        # state is the previous value of the clock
        if not sm.fired and Globals.currentTime >= sm.eventTime:
            sm.value = EventValue(True)
            sm.fired = True
        # add the current clock signal to the list of fast updating signals (which doesn't exist yet)
        else:
            sm.value = noEvent
    return StateMachineF(initClock, maybeLift(0), clockFN)

def timeIs(n):
    return delay(n, absoluteTime = True)

def exitScene(m, v):
    exit(m)

eventTrue = EventValue(True)

# This converts a boolean behavior into an event that fires whenever the
# behavior is true
def happen(b, val = True):
    return lift("happen", lambda x:EventValue(val) if x else noEvent)(b)

# This limits an event stream to the first event
def once(e):
    def initOnce(sm):
        sm.value = noEvent
        sm.fired = False
    def onceFN(sm): # tracks and updates engine time
        # state is the previous value of the clock
        i = sm.i.now()
        if i.occurs() and not sm.fired:
            sm.value = i
            sm.fired = True
        else:
            sm.value = noEvent
    return StateMachineF(initOnce, maybeLift(e), onceFN)

# This event occurs whenever the behavior changes.  Value of the event is the
# new value of the behavior
def changes(b):
    def initChanges(sm):
        sm.value = noEvent
        sm.last = EventValue()  # This is any value tha is guaranteed not to be in the input
    def changesFN(sm): # tracks and updates engine time
        # state is the previous value of the clock
        v = sm.i.now()
        if v != sm.last:
            sm.value = EventValue(v)
            sm.last = v
        else:
            sm.value = noEvent
    return StateMachineF(initChanges, maybeLift(e), changesFN)

# Filter an event stream.  Only event values that satify fn will occur
def filter(fn, e):
    lift("filter", lambda val: EventValue(fn(val.value)) if val.occurs() else noEvent)

def atTime(t,f):
    def r(m,v):
        f()
    react1(timeIs(t), r)
