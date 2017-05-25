"""
A proxy object that prints the name and values of all its signals.
Mostly used for testing.
"""

from pythonfrp.Proxy import Proxy

class Printer(Proxy):
    def __init__(self, name, args):
        Proxy.__init__(self, name, printupdate, {})
        for k, v in args.items():
            setattr(self, k, v)


def printupdate(proxy):
    for k, v in proxy._signals.items():
        print(k + ": " + str(v.now()))


def printer(name = "printing object", **kwargs):
    return Printer(name, kwargs)
