from pythonfrp import Interp
from pythonfrp.StaticNumerics import *
from pythonfrp.Factory import *
from pythonfrp.Types import *
import math

pi       = math.pi
twopi    = 2*pi

P3       = lift("SP3", SP3, types = [numType, numType, numType], outType = p3Type)
p3 = P3
P2       = lift("SP2", SP2, types = [numType, numType], outType = p2Type)
p2 = P2
P3C       = lift('P3C',SP3C,[numType, numType, numType], outType = p3Type)
p3c = P3C

p2       = lift("p2", SP2, types = [numType, numType], outType = p2Type)
P2 = p2


getX     = lift("getX", lambda v:v.x, [hasXYType], numType)
getY     = lift("getY", lambda v:v.y, [hasXYType], numType)
getZ     = lift("getZ", lambda v:v.z, [p3Type], numType)


radians  = lift("radians", math.radians, [numType], numType)
# Delete this from elsewhere, use math.degrees in update functions
degrees  = lift("degrees", math.degrees, [numType], numType)
sin      = lift("sin", math.sin, [numType], numType)
asin     = lift("asin", math.asin, [numType], numType)
cos      = lift("cos", math.cos, [numType], numType)
acos     = lift("acos", math.acos, [numType], numType)
tan      = lift("tan", math.tan, [numType], numType)
atan2    = lift("atan2", math.atan2, [numType, numType], numType)
sqrt     = lift("sqrt", math.sqrt, [numType], numType)
exp      = lift("exp", math.exp, [numType], numType)
pow      = lift("pow", math.pow, [numType,numType], numType)
log      = lift("log", math.log, [numType], numType)

ceiling  = lift("ceiling", sCeiling, [numType], numType)
floor    = lift("floor", sFloor, [numType], numType)
fraction = lift("fraction", sFraction, [numType], numType)
max      = lift("max", max, [numType,numType], numType)
min      = lift("min", min, [numType,numType], numType)
# sections
add      = lift("add", lambda x: lambda y: x+y, [numType], fnType)
sub      = lift("sub", lambda x: lambda y: y-x, [numType], fnType)
times    = lift("times", lambda x: lambda y: x*y, [numType], fnType)
div      = lift("div", lambda x: lambda y: x/y, [numType], fnType)

#dot      = lift(lambda x,y: genDot(x,y), "dot", infer="dot")
const    = lift("const", lambda x: lambda y: x, [anyType], fnType)



string   = lift("string", str, [anyType], stringType)

#norm      = lift(normP3, 'norm', [P3Type], P3Type)

normA = lift("normA", sNormA, [numType], numType)

def dist(x, y):
    return abs(x-y)

format    = lift("format", lambda str, *a: str % a)

# Lifted conditional

def staticIf(test, x, y):
    if test:
        return x
    return y

choose = lift("choose", staticIf)

# Interpolation functions

lerp = lift("lerp", Interp.lerpStatic)
interpolate = lift("interpolate", Interp.interpolateStatic)


def encodeNums(*n):
    s = ""
    r = ""
    for num in n:
        r = r + s + str(num)
        s = ","
    return r

def decodeNums(s, f):
    nums = s.split(",")
    return f(*map(lambda x: float(x.strip()), nums))

p3Type.encoder = lambda p: encodeNums(p.x, p.y, p.z)
p3Type.decoder = lambda s: decodeNums(s, p3)

p2Type.encoder = lambda p: encodeNums(p.x, p.y)
p2Type.decoder = lambda s: decodeNums(s, p2)

