# https://www.8ecm.si/ potrebuje našo pomoč pri sestavljanju urnika predavanj
import dataclasses
import functools
from datetime import time

# Struktura podatkov
# Objekt `Predavanje`, `Dan`, `Teden`
from typing import Any, List


class Predavanje:
    def __init__(self, naslov, predavatelj, moderator, zacetek, konec):
        self.naslov = naslov
        self.predavatelj = predavatelj
        self.moderator = moderator
        self.zacetek = zacetek
        self.konec = konec


fm = Predavanje("The dawn of formalized", "A. Bauer", "Russ", time(14), time(15, 30))

# UGH
print(fm, [fm])
try:
    print(fm < fm)
except TypeError as e:
    print("More wörk, wörk, wörk")


class Predavanje(Predavanje):
    # Na nas je, da spišemo lepo predstavitev v nizu
    def __str__(self):
        # F nizi so zakon
        return f"{self.naslov}, {self.predavatelj=}"

    def __repr__(self):
        # Lenoba
        # Samo o f-nizi bi lahko imel celo delavnico
        return f"Predavanje({self}, {f'{self.zacetek}':*^30})"

    def __eq__(self, other):
        return self.zacetek == other.zacetek and self.konec == other.konec

    def __lt__(self, other):
        if self.zacetek < other.zacetek:
            return True
        if self.zacetek == other.zacetek:
            return self.konec < other.konec
        return False


fm = Predavanje("The dawn of formalized", "A. Bauer", "Russ", time(14), time(15, 30))
print(fm, [fm])

print(fm < fm)
print(fm > fm)  # Vaja: Zakaj to deluje?

try:
    print(fm <= fm)
except TypeError as e:
    print("More wörk, wörk, wörk")


# To se da
# Sicer plačamo nekaj več pri primerjanju, ampak se splača če potrebujemo enostavne primerjave relativno hitro


@functools.total_ordering
class Predavanje(Predavanje):
    pass


fm = Predavanje("The dawn of formalized", "A. Bauer", "Russ", time(14), time(15, 30))

try:
    print(fm <= fm)
except TypeError as e:
    print("More wörk, wörk, wörk")

# Napišimo to pravilno, ampak prej si malo poglejmo kaj razredi res so

print(dir(fm))
print(vars(fm))
print(vars(fm)["konec"])
print(fm.__dict__)
fm.__dict__["komentar"] = "Zanimivo"
print(vars(fm))
# Od python 3.nekaj so slovarji urejeni
print(dir(fm))

# Kaj pa je Predavanje?
print(Predavanje)
print(dir(Predavanje))
print(Predavanje.__dict__)
Predavanje.pp = lambda x: print("Predavanje")
fm.pp()
print(dir(Predavanje))
print(Predavanje.__dict__)
print(Predavanje.__gt__)

Predavanje.pa = lambda: print("Predavam")
Predavanje.pa()
try:
    fm.pa()
except TypeError:
    print("Tole ne bo šlo")

# Metode (tiste s self) sprejmejo dodaten parameter "dobesedno"

# Popravimo
print(Predavanje.__str__(fm))
Predavanje.pa = classmethod(lambda x: print("Predavam"))
Predavanje.pa()
fm.pa()


# Vaja: Naredi nov "mock" objekt, ki bo dovolj podoben razredu `Predavanje`, da bo __str__ metoda delovala in jo uspešno pokliči

class Predavanje(Predavanje):
    # Na nas je, da spišemo lepo predstavitev v nizu
    def __str__(self) -> str:
        # F nizi so zakon
        return f"{self.naslov}, {self.predavatelj=}"

    # Kar direktno priredimo (ni najlepše, ampak včasih je ok)
    __repr__ = __str__

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Predavanje) and self.zacetek == other.zacetek and self.konec == other.konec

    def __lt__(self, other: Any) -> bool:
        # VAJA: Zakaj ne type(other) == type(self)
        if not isinstance(other, Predavanje):
            raise TypeError()
        if self.zacetek < other.zacetek:
            return True
        if self.zacetek == other.zacetek:
            return self.konec < other.konec
        return False


# Sedaj pa dataclasses
from dataclasses import dataclass, field


@dataclass
class Dan:
    dan: str
    predavanja: List[Predavanje]


pon = Dan("ponedeljek", [fm, fm, fm])
# Zastonj
print(pon, [pon])


@dataclass(order=True, unsafe_hash=True)
class Dan:
    dan: str
    predavanja: List[Predavanje] = field(default_factory=list, compare=False)
    komentar: str = "Običajen dan"
    dodatno: str = field(init=False, default="")
    uid: int = field(init=False)

    def __post_init__(self):
        if self.komentar == "":
            self.dodatno = "Lenuh"

# Vaje
# Pripravi celoten urnik
# Teden ima 5 dni, Dan ima seznam Predavanja
# Bodi inovativen in uporabi možnosti, ki jih ponujajo dataclasses, da se malo spoznaš
# order, unsafe_hash, default_factory, compare, init, post_init...









@dataclass(frozen=True, order=True)
class DanVTednu:
    ime: str
    dolzina: int = field(init=False)

    def __post_init__(self):
        # Malo moramo goljufati
        object.__setattr__(self, "dolzina", 24)


pon = DanVTednu("pon")
try:
    pon.ime = "torek"
except dataclasses.FrozenInstanceError:
    print("Ne bo šlo")

# Dneve v tednu bi lahko malo prilagodili

from enum import Enum, auto, unique


@unique
class DanVTednu(Enum):
    PONEDELJEK = 1
    TOREK = 2
    SREDA = 3
    CETRTEK = 4
    PETEK = auto()
    # PETEK2 = 5


p = DanVTednu.PETEK
print(p, p.value)


# Vaja: Popravi dneve v tednu, da bodo vsebovali enume


# še malo dobrot

print(dataclasses.fields(pon))
print(dataclasses.asdict(pon))
print(dataclasses.astuple(pon))
print(dataclasses.replace(pon, ime=4))
