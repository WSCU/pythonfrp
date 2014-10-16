    # Done

# This is the non-reactive version of the numeric classes.  To get the overloading right,
# we have to go through contortions using radd, rsub, and rmul so that an ordinary
# number doesn't screw up overloading in 1 + signal, 1 - signal, and 1 * signal.
# Not sure why rdiv isn't here.

#import g
import math
import random
import sys
from . import Factory
from . import Errors
from . import Interp
from . import Numerics
from . Types import *
from SHPR import *

# This is a where we park signal functions.

pi       = math.pi
twopi    = 2 * pi
sCeiling = math.ceil
sFloor   = math.floor
cos = math.cos
sin = math.sin
def sFraction(x):
    return x - sFloor(x)

def degrees( v):
    return v*(180/pi)

# This class is the 0 element in an arbitrary numeric
# class.  It is used as the initial result of an integrator.


# Note that the destination is never changed.
class Zero:
    def __str__(self):
        return "0"
    def __add__(self, y):
        return  y

zero = Zero()

def staticLerp(t, x, y):
    return (1-t)*x + t*y

def staticLerpA(t, x, y):
    x1 = x / twopi
    y1 = y / twopi
    x2 = twopi * (x1 - math.floor(x1))
    y2 = twopi * (y1 - math.floor(y1))
    if x2 < y2:
        if y2 - x2 > pi:
            return staticLerp(t, x2 + twopi, y2)
        return staticLerp(t, x2, y2)
    else:
        if x2 - y2 > pi:
            return staticLerp(t, x2-2 * pi, y2)
        return staticLerp(t, x2, y2)

# Normalize an angle to the -pi to pi range
def sNormA(a):
    a1 = a / twopi
    a2 = twopi * (a1 - math.floor(a1))
    return a2 if a2 <= pi else a2 - twopi

# The P2 class (2-d point)
# Note that P2 x Scalar works.  Probably not P2 / scalar though.

class SP2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._type = p2Type
    def __str__(self):
        return "P2(%7.2f, %7.2f)" % (self.x, self.y)
    def __add__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP2):
            return addP2(self, y)
        if isinstance(y, Factory.SFact):
            return y + self
        Errors.errorOnStaticTypes("Add", "SP2", y)
        sys.exit()
    def __radd__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP2):
            return addP2(self, y)
        Errors.errorOnStaticTypes("Add", "SP2", y)
    def __sub__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP2):
            return subP2(self, y)
        if isinstance( y, Factory.SFact):
            return Factory.Lift0F(self, p2Type) - y
        Errors.errorOnStaticTypes("Sub", "SP2", y)
    def __rsub__(self, y):
        if y is zero:
            return zero.sub(self, zero)
        if isinstance(y, SP2):
            return subP2(y, self)
        Errors.errorOnStaticTypes("Sub", "SP2", y)
    def __mul__(self, y):
        if y is zero:
            return zero
        if isinstance(y, type(1)) or isinstance(y,type(1.0)):
            return scaleP2(y, self)
        if getPtype(y).includes(numType):
            return scaleP2(y, self)
        Errors.errorOnStaticTypes("Mul", "SP2", y)
    def __rmul__(self, y):
        if y is zero:
            return zero
        if isinstance(y, type(1)) or isinstance(y,type(1.0)):
            return scaleP2(y, self)
        if getPtype(y).includes(numType):
            return scaleP2(y, self)
        Errors.errorOnStaticTypes("Mul", "SP2", y)
    def __div__(self, y):
        if y is zero:
            print("Universal Explosion")
            return zero
        if isinstance(y, type(1)) or isinstance(y,type(1.0)):
            return scaleP2((1.0/y), self)
        if getPtype(y).includes(numType):
            return scaleP2(1.0/y, self)
        Errors.errorOnStaticTypes("Div", "SP2", y)
    def __abs__(self):
        return absP2(self)
    def __neg__(self):
        return scaleP2(-1, self)
    def interp(self, t, p2):
        return SP2(staticLerp(t, self.x, p2.x),
                   staticLerp(t, self.y, p2.y))
    def interpA(self, t, p2):
        return SP2(staticLerpA(t, self.x, p2.x),
                   staticLerpA(t, self.y, p2.y))

# Used for integration


def readP2(str):
    nums = parseNumbers(str)
    return SP2(nums[0], nums[1])


# non-overloaded methods for P2 arithmentic

def addP2(a, b):
    return SP2(a.x + b.x, a.y + b.y)

def subP2(a, b):
    return SP2(a.x-b.x, a.y-b.y)

def scaleP2(s, a):
    return Numerics.P2(s * a.x, s * a.y)

def absP2(a):
    return math.sqrt(a.x * a.x + a.y * a.y)

def dotP2(a, b):
    return SP2(a.x * b.x, a.y * b.y)


# The P3 class, similar to P2

class SP3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self._type = p3Type

    def __str__(self):
        return "P3(%7.2f, %7.2f, %7.2f)" % (self.x, self.y, self.z)

    def __add__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP3):
            return addP3(self, y)
        if isinstance(y, Factory.SFact):
            return y + self
        Errors.errorOnStaticTypes("Add", "SP3", y)
    def __radd__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP3):
            return addP3(self, y)
        if isinstance(y, Factory.SFact):
            return y + self
        Errors.errorOnStaticTypes("Add", "SP3", y)
    def __sub__(self, y):
        if y is zero:
            return self
        if isinstance(y, SP3):
            return subP3(self, y)
        if isinstance(y, Factory.SFact):
            return Factory.Lift0F(self, p3Type) - y
        Errors.errorOnStaticTypes("Sub", "SP3", y)
    def __rsub__(self, y):
        if y is zero:
            return zero.sub(self, zero)
        if isinstance(y, SP3):
            return subP3(y, self)
        Errors.errorOnStaticTypes("Sub", "SP3", y)
    def __mul__(self, y):
        if y is zero:
            return zero
        if isinstance(y, type(1)) or isinstance(y,type(1.0)):
            return scaleP3(y, self)
        #print getPtype(y)
        if getPtype(y).includes(numType):
            return scaleP3(y, self)
        Errors.errorOnStaticTypes("Mul", "SP3", y)
    def __rmul__(self, y):
        if y is zero:
            return zero.rmul(self, y)
        if isinstance(y, type(1)) or isinstance(y, type(1.5)):
            return scaleP3(y, self)
        #print getPtype(y)
        if getPtype(y).includes(numType):
            return scaleP3(y, self)
        Errors.errorOnStaticTypes("Mul", "SP3", y)
    def __div__(self, y):
        if y is zero:
            print("Universal Explosion")
            return zero
        if isinstance(y, type(1)) or isinstance(y,type(1.0)):
            return scaleP3((1.0/y), self)
        if getPtype(y).includes(numType):
            return scaleP3((1.0/y), self)
        Errors.errorOnStaticTypes("Div", "SP2", y)
    def __abs__(self):
        return absP3(self)
    def __neg__(self):
        return scaleP3(-1, self)
    def interp(self, t, p2):
        return SP3(staticLerp(t, self.x, p2.x),
                   staticLerp(t, self.y, p2.y),
                   staticLerp(t, self.z, p2.z))

def readP3(str):
    nums = parseNumbers(str)
    return SP3(nums[0], nums[1], nums[2])


def crossProduct(a, b):
    return SP3(a.y * b.z - a.z * b.y,
               a.z * b.x - a.x * b.z,
               a.x * b.y - a.y * b.x)

def normP3(p):
    a = absP3(p)
    if a < 0.0000001:  # Avoid divide by 0
        return SP3(0, 0, 0)
    else:
        return scaleP3(1 / a, p)
def addP3(a, p):
    return SP3(a.x + p.x, a.y + p.y, a.z + p.z)
def subP3(a, p):
    return SP3(a.x - p.x, a.y - p.y, a.z - p.z)
def scaleP3(s, a):
    return Numerics.P3(a.x * s, a.y * s, a.z * s);
def absP3(a):
    return math.sqrt(a.x * a.x + a.y * a.y + a.z * a.z);
def dotP3(a, b):
    return SP3(a.x * b.x, a.y * b.y, a.z * b.z)

# Construct a polar 2-D point
def SP2Polar(r, theta):
    r = r + 0
    theta = theta + 0
    return SP2(r * math.cos(theta), r * math.sin(theta))

def SP3C(r, theta, z):
    p = SP2Polar(r, theta)
    return SP3(p.x, p.y, z)

# Conversions from tuple type.


def sFirst(p):
    p.first

def sSecond(p):
    p.second

def sHPRtoP3(p):
    return SP3(math.sin(p.h) * math.cos(p.p),
               -math.cos(p.h) * math.cos(p.p),
               -math.sin(p.p))

def sP3toHPR(p):
    return SHPR(math.atan2(p.y, p.x) + pi / 2,
                math.atan2(p.z, abs(SP2(p.x, p.y))),
                0)




# Random number stuff - static only!

def randomChoice(choices):
    return random.choice(choices)

def random01():
    return random.random()

def random11():
    return 2 * random.random()-1

def randomRange(low, high=None):
    if high is None:
        return low * random01()
    return low + random01() * (high-low)

def randomInt(low, high=None):
    if high is None:
        return random.randint(0, low)
    return random.randint(low, high)

def shuffle(choices):
    c = list(choices)
    random.shuffle(c)
    return c

def sStep(x):
    if (x < 0):
        return 0
    else:
        return 1


def sSmoothStep(x):
    if (x < 0):
        return 0
    if (x > 1):
        return 1
    return x * x * (-2 * x + 3)

random.seed()
################################################################

