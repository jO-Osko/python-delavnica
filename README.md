# Računalniška delavnica python++

## Dataclass
- Motivacija
  - Preprost razred
  - `__str__`, `__repr__`, `<`.  
- Namedtuple
- Osnovna uporaba
- Napredne metode (`default_factory`, `hash`, ...)
- Dedovanje

## Originalno vabilo

Kljub popularnosti in močno razširjenosti, se programski jezik python zaradi vsestranske uporabnosti razvija vedno hitreje, tudi s pomočjo [velikih](https://cloud.google.com/blog/products/open-source/supporting-the-python-ecosystem) [tehnoloških](https://www.techatbloomberg.com/blog/supporting-the-python-community-by-shifting-left/) [igralcev.](https://techcrunch.com/2020/11/12/python-creator-guido-van-rossum-joins-microsoft/)

Na delavnici si bomo pogledali nekatere najnovejše pridobitve v jeziku python, ki nam lahko močno olajšajo programiranje, ampak jih zaradi časovne stiske ni mogoče lepo predstaviti tekom rednega študija.

Pogledali si bomo knjižnico `dataclasses`, ki nam z le nekaj dekoratorji močno poenostavi definicijo preprostih razredov. Poleg osnovne uporabe, si bomo pogledali tudi nekaj bolj naprednih konceptov za zahtevnejše kreacije objektov.

Natančneje si bomo pogledal, kaj se dogaja med kreacijami objektov in ugotovili, zakaj metoda `__init__` v resnici ni konstruktor in kako si python v sploh predstavlja objekte. Pogledali bomo kako delujeta metodi `getattr` in `setattr` ter naredili svoj slovar z nekaj dodatki.

Zadnji del delavnice bomo posvetili novim sintaktičnim dodatkom, ki lahko močno olajšajo delo, anotacije tipov, ti "function overloading", uporabo generatorjev, gnezdeno sprožanje izjem in seveda najbolj svežo pridobitev, ki nam omogoča ujemanje na vzorcih po navdihu funkcijskih jezikov (Ta je na voljo šele v verziji 3.10).

Potrebno predznanje in namestitve
- Osnovno poznavanje programiranja
- Nameščena čim novejša različica jezika python (Vsaj 3.9, če se le da 3.10)
- Nameščena knjižnica mypy
- Urejevalnik po izbiri (Pozor: Pycharm še ne podpira novih sintaktičnih dobrot verzije 3.10)