from pythonfrp import Globals
from pythonfrp.Factory import *
from pythonfrp.Types import proxyType, anyType
from pythonfrp import Errors

class Reaction:
    def __init__(self, fn, m, v):
        self.fn = fn
        self.m = m
        self.v = v
    def react(self):
        self.fn(self.m, self.v)

class Proxy:
    def __init__(self, name, updater, types = {}, duration = 0):
        self._types = types
        self._alive = True;
        self._type = proxyType
        self._signals = {}
        self._1Reactions = []
        self._gReactions = []
        self._updateSignals = {}
        self._name = name
        self._updater = updater
        Globals.newObjects.append(self)

    def __setattr__(self, name, value):
        if name[0] == '_':
            self.__dict__[name] = value
        else:
            #if value.type == SignalType:
            self._updateSignals[name] = value
            #else:
             #   print("Error: Tried to set attribute to non-signal.")
    def __getattr__(self, name):
        if name[0] == '_':
            return self.__dict__[name]
        else:
            return ObserverF(lambda x: self._get(name))
            #return self._signals[name]
    def _get(self, name):
        if name in self._signals:
            return self._signals[name].now()
        print( str(name) + " does not exist or has not been started in this Proxy: " + repr(self))

    def _initialize(self):
        for k, v in self._updateSignals.items():
            #print(k, v)
            # print("Object: " + self._name + " is initializing field: " + k + " to " + str(v))
            if k in self._types:
                ty = self._types[k]
            else:
                ty = anyType
            v = maybeLift(v)
            Globals.error = "On Line 51 of Proxy, In object " + k + ", attribute " + str(v)
            #print(str(self._signals))
            #print(str(v))
            sig = v.start(expectedType = ty, obj = self)[0] # This is screwing up Integral
            #print("initilize signal = " + repr(sig))
            self._signals[k] = cache(sig)
        #print("----- Initialized " + str(self._name) + " with :" + repr(self._signals))
        self._updateSignals = {}

    def _react(self, when, what):
        if self._alive:
            when = maybeLift(when)
            Globals.error = "On Line 59 of Proxy, In object " + self._name + ", initializing reaction " + when.name
            self._gReactions.append((when.start()[0], what))

    def _react1(self, when, what):
        if self._alive:
            when = maybeLift(when)
            Globals.error = "On Line 59 of Proxy, In object " + self._name + ", initializing one time reaction " + when.name
            self._1Reactions.append((when.start()[0], what))

    def _update(self):
        if self._alive:
#            print("Object: " + str(self) + " signals: " + str(self._signals))
            for k, v in self._signals.items():
#                print("Objects: " + str(self) + " is updating: " + k)
                v.now()
            thunks = []

            #Evaluate one time reactions:
            for c in self._1Reactions:
#                print("Object: " + str(self) + " is updating: " + str(c[0]))
                temp = c[0].now()
                Errors.checkEvent(temp, "One time reaction in " + self._name)
                if temp.occurs():
                    #print("    " + str(temp) + " is being added to thunks")
                    thunks.append(Reaction(c[1], self, temp.value))
                    self._1Reactions = []
                    break

            if (len(thunks) >= 2):
                print("Multiple one time reactions in a heartbeat in object " + self._name)

            #Evaluate recurring reactions
            # print("Number of reactions in " + self._name + " " + str(len(self._gReactions)))
            for d in self._gReactions:
                temp = d[0].now()
                Errors.checkEvent(temp, "recurring reaction in " + self._name)
#                print("Object: " + str(self) + " is updating: " + str(d[0]))
                if temp.occurs():
                    #print("    " + repr(temp) + " is being added to thunks")
                    #print("Thunks" + str(thunks) + " " + str(d))
                    thunks.append(Reaction(d[1], self, temp.value))

            #push to the actuall object
            self._updater(self)
            return thunks

    def __str__(self):
        #print(self._signals)
        #print(self._updateSignals)
        return self._name

    def __repr__(self):
        return str(self._name)

    def _remove(self):
        pass
    def _exit(self):
        Globals.worldObjects = [x for x in Globals.worldObjects if x is not self]
        self._remove()    #  This is in the subclass
        self._alive = False

def clearReactions(m):
    m._1Reactions = []
    m._gReactions = []
