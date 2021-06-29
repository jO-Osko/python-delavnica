# __init__ ni konstruktor, ampak inicializator
from dataclasses import field, dataclass, fields


class AttributeDict(dict):
    __slots__ = ()
    __getattr__ = dict.__getitem__  # Da ga lahko uporabljamo kot a.XYZ namesto a["XYZ"]

    def __setitem__(self, key, value):
        if key not in self:
            raise TypeError("Object is read only")
        else:
            super().__setitem__(key, value)

    def __setattr__(self, key, value):
        self[key] = value


a = AttributeDict({1: 2, "k": 4})

a[1] = 3
a.k = "12"
print(a)

# Ne omogoča pa nastavljanja stvari
try:
    a[2] = 3
except TypeError:
    print("pa res ne")


# __new__ vs __init__
# Metoda __new__ skonstruira objekt, __init__ pa ga inicializira
# Zakaj __init__ ne vrne self?, ker to ni rezultat, init je po zasnovi mutable
# Z __new__ naredimo nov objekt, kateregakoli, ob primernih pogojih se pokliče init

class Neumnosti:
    def __new__(cls, *args, **kwargs):
        if args and args[0] == "scary":
            return "hahhahahahaha"
        return super().__new__(cls)


print(Neumnosti(1))
print(Neumnosti("scary"))


# Uporabimo naš slovar


class SpecialniSlovar(dict):
    def __new__(cls, *args, **kwargs):
        if kwargs.get("frozen"):
            kwargs.pop("frozen")
            return AttributeDict(*args, **kwargs)
        return dict(*args, **kwargs)


s = SpecialniSlovar({"a": "b"}, frozen=False)


# print(s.a)


# Static vs class methods
# Predvsem uporabne v dedovanju in za bolj splošno kodo

# More dataclass goodies
# Kaj sploh je class?
# Kaj sploh je funkcija

# Nekaj o default argumentih

# Padeš na ustnem izpitu
# Poseben quirk pythona
# Kaj se v resnici zgodi
def fun(x, y=[]):
    print(x == y, x is y, y)
    return y


a = fun([])
a.append(10)
a.append(20)
fun(a, )


# Kaj se res zgodi, default se nastavi ob definiciji


def inicializacja():
    print("poklican sem bil")
    return []


print("prej")


def g(x=inicializacja()):
    print("kličem g")
    return x


print("potem")
for j in range(10):
    g()

# Nekaj splošnih nasvetov
a = [
    1,
    2,  # Pusti vejico, je veliko bolj prijazna za git review
]

fun(
    10,
    [],
)

# Še malo o argumentih

print(1, 2, 3, 4, sep="številkeeeeeee")
print(*range(10), sep="sad")


# Kako pridemo do tega
def printer(a: int, b: "upam da številka", /, *, a_res):
    printer.callable += 1
    if a_res:
        print("ni res")
    return a + b

printer.callable = 0

# Swift recimo omogoča različno poimenovanje argumentov

printer(1, 2, a_res=True)
printer(1, 2, a_res=True)
printer(1, 2, a_res=True)
printer(1, 2, a_res=True)

print(printer.callable)

print(printer.__annotations__)


# Wrappers

def wrapper(f):
    print("ovijam")

    def ff(x):
        print("računam")
        return 2 * f(x)

    return ff


@wrapper
def g(x):
    return x


h = wrapper(g)

print(g(10))
print(h(10))


# Zakaj pa to ne bi delovalo za razrede

def class_wrapper(cls):
    old_init = cls.__init__

    def __init__(self, *args, **kwrags):
        print("Inicializiram")
        # pokaži zakaj cls.__init__ ni ok
        rtr = old_init(self, *args, **kwrags)
        print("Koncano")
        return rtr

    cls.__init__ = __init__
    return cls


@class_wrapper
class A:
    def __init__(self, x):
        self.x = x


a = A(10)


def dataclass_wrapper(cls):
    cls = dataclass(cls)
    cls_fields = {
        j.name: j for j in fields(cls)
    }
    validators = {
        j: validator for j, info in cls_fields.items() if (validator := info.metadata.get("validator"))
    }

    def special_set(self, attr, value):
        print("here")
        print(validators, attr, validators.get(attr))
        if validator := validators.get(attr):
            try:
                value = validator(value)
                object.__setattr__(self, attr, value)
            except Exception as e:
                print("Čiščenje")
                raise TypeError("Napaka v validiranju") from e

    cls.__setattr__ = special_set

    return cls


def validate_username(name: str):
    if "math" not in name.lower():
        raise TypeError("No math")
    return f"Math paper: {name}"


@dataclass_wrapper
class UserData:
    name: str
    lecture: str = field(metadata={"validator": validate_username})


u = UserData("a", "math")
# u = UserData("a", "ma2th")

#  @property