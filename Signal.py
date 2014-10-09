import Globals
import Errors
from Types import signalType, eventValueType

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

class Lift(Signal):
    def __init__(self,name, f, args):
    	Signal.__init__(self)
        self.f = f
        self.name = name
        self.args=args
    def now(self):
    	ea = map (lambda a: a.now() , self.args)
        # print "eval " + self.name + " " + str(ea) + " = " + str(self.f(*ea))
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
        s0(self)
    def now(self):
        if self.time is not Globals.currentTime:
            self.f(self)
            self.time = Globals.currentTime
        return self.value
    def __rmul__(self, y): # JP is confused
        y = maybeLift(y)
        print "rmul in state machine... whats happening to me???"
        return LiftF("mul", lambda x,y: y*x, [self.state, y])

class Observer(Signal):
    def __init__(self, f):
        Signal.__init__(self)
        self.f = f
    def now(self):
        return self.f(self)

