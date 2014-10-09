import sys
import Signal

def checkEvent(evt, context):
    if not isinstance(evt, Signal.EventValue):
        print("Error: " + str(evt) + " is not an event value in " + context)
        sys.exit()
    return

def badKeyName(n):
    print(str(n) + " is not a valid key name")
    sys.exit()

def errorOnStaticTypes(func, correct, y):
    print(func + " of " + correct + " bad argument: " + str(y))
    sys.exit()

def checkNumArgs(expected, got, obj, attr):
    #print str(expected) + " " + str(got)
    if expected is 0 or expected is got:
        return
    else:
        if hasattr(obj, '_name'):
            name = obj._name
        else:
            name = str(obj)
        print("in " + str(name) + ", attribute " + str(attr) + ", expected: " + str(expected) + " args, but recieved: " + str(got) + " args")
        sys.exit()

def typeError(expected, got, name, attr):
    print("in " + str(name) + ", attribute " + str(attr) + ", expected: " + str(expected) + ", but recieved: " + str(got))
    sys.exit()