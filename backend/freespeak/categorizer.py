import os

# GLOBAL MARKERS
stdsyn = []
_TASK = []
_STRUCTURE = []
_MODIFIER = []
_TYPE = []



# CURRENT WORD MARKERS
task_ = []
structure_ = []
modifier_ = []
type_ = []
superfluous_ = []

if os.path.isfile("wordcache/_synlist_.txt"):
    with open("wordcache/_synlist_.txt", "r") as synlist:
        for line in synlist:
            stdsyn[line[:line.find(":")]] = line[line.find(":"):]

if os.path.isfile("wordcache/_TASK_.txt"):
    with open("wordcache/_TASK_.txt", "r") as _glbltask:
        for line in _glbltask:
            _TASK[line[:line.find(":")]] = line[line.find(":"):]

if os.path.isfile("wordcache/_STRUCTURE_.txt"):
    with open("wordcache/_STRUCTURE_.txt", "r") as _glblstrct:
        for line in _glblstrct:
            _STRUCTURE[line[:line.find(":")]] = line[line.find(":"):]

if os.path.isfile("wordcache/_MODIFIER_.txt"):
    with open("wordcache/_MODIFIER_.txt", "r") as _glblmod:
        for line in _glblmod:
            _MODIFIER[line[:line.find(":")]] = line[line.find(":"):]

if os.path.isfile("wordcache/_TYPE_.txt"):
    with open("wordcache/_TYPE_.txt", "r") as _glbltype:
        for line in _glbltype:
            _TYPE[line[:line.find(":")]] = line[line.find(":"):]


def label (sentence):
    return sentence
