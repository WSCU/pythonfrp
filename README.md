pythonfrp
=========
pythonfrp is an attempt to bring reactive programming into python.

What is Reactive Programming?
-----------------------------

Simply put, reactive programming uses continuous time and data flow instead of explicit time.

The [wikipedia](http://en.wikipedia.org/wiki/Reactive_programming) article has a good explanation.

Usage
---
A simple hello world:

    from pythonfrp.Engine import *
    from pythonfrp.Printer import printer

    printer(x = integral(1, 0))
    start(tSteps = 10)

Documentation and website
----
All documentation and more information can be found at [reactive-engine.org](http://www.reactive-engine.org)
