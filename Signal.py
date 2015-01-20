from . import Globals
from . import Errors
from . Types import signalType, eventValueType

class EventValue:
    def __init__(self, value = None):
        self._type = eventValueType
        self.value = value
    def __add__(self, e):
        Errors.checkEvent(e, "event addition")
 #       print "Event merge: " + str(self) + " " + str(e)
        if self.value is None:
            return e
        else:
            return self
    def occurs(self):
        return self.value is not None
    def __str__(self):
        if self.value is None:
            return "<No Event>"
        return "<" + str(self.value) + ">"

noEvent = EventValue()

class Signal:
    def __init__(self):
        self._type = signalType

class Lift0(Signal):
    def __init__(self, v):
        Signal.__init__(self)
        self.v = v
    def now(self):
        return self.v
    def __str__(self):
        return str(self.v)

class Lift(Signal):
    def __init__(self,name, f, args):
        Signal.__init__(self)
        self.f = f
        self.name = name
        self.args=args
        print("Lift const: " + str(self.args))
        print("Lift const, arg0.now: " + repr(self.args[0].now()))
        print("Lift const, arg1.now: " + repr(self.args[1].now()))
    def now(self):
        print("Lift, arg0.now: " + repr(self.args[0].now()))
        print("Lift, arg1.now: " + repr(self.args[1].now()))
        ea = list(map(lambda a: a.now() , self.args)) # Why is this giving me a Lift0
        # for the frist argument instead of its value?
        # Why is the value a Lift0
        print("Lift: " + str(ea))
        #print ("eval" + self.name + " " + str(ea) + " = " + str(self.f(*ea)))
        return self.f(*ea)

# Cached Signal that inherits Signal
# Baisically is just a time stamp
class CachedSignal(Signal):
    def __init__(self, s):
        Signal.__init__(self)
        self.cachedValue = 0
        self.time = -1
        #print "cache " + repr(s)
        self.s = s
#        if not isinstance(s, Lift):  # Could also be an observer
#            die()
    def now(self):
        if self.time is not Globals.currentTime:
            self.cachedValue = self.s.now()
            self.time = Globals.currentTime
        return self.cachedValue

def cache(s):
    if isinstance(s, Lift0) or isinstance(s, StateMachine):
        return s
    return CachedSignal(s)

# A State Machine signal
class StateMachine(Signal):
    def __init__(self, s0, i, f):
        #print "s0 = " + repr(s0) + " i = " + repr(i) + " f = " + repr(f)
        Signal.__init__(self)
        self.f = f
        self.i = i
        self.time = -1
        self.value = self.i.now()
        s0(self)
    def now(self):
        #Caching the value
        #We don't want to recalculate more than once each step
        if self.time is not Globals.currentTime:
            self.f(self)
            self.time = Globals.currentTime
        return self.value

class Observer(Signal):
    def __init__(self, f):
        Signal.__init__(self)
        self.f = f
    def now(self):
        return self.f(self)

