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
    x = integral(1, 0)
    run(steps = 5)
    print(x)
This will output

    > 4

Documentation and website
----
All documentation and more information can be found at [reactive-engine.org](reactive-engine.org)
