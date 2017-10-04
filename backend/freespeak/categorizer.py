import os
import sys
from freespeak import synonymfinder
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# GLOBAL MARKERS
stdsyn = {}
_TASK = []
_STRUCTURE = []
_MODIFIER = []
_TYPE = []
_SUPERFLUOUS = []



# CURRENT WORD MARKERS
task_ = []
structure_ = []
modifier_ = []
type_ = []
superfluous_ = []

def _loadCache():

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    CACHE_DIR = BASE_DIR + "/wordcache/"

    if os.path.isfile(CACHE_DIR + "_synlist_.txt"):
        with open(CACHE_DIR + "_synlist_.txt", "r") as synlist:
            for line in synlist:
                line = line.replace("\n", "")
                stdsyn[line[:line.find(":")]] = line[line.find(":"):]

    if os.path.isfile(CACHE_DIR + "_TASK_.txt"):
        with open(CACHE_DIR + "_TASK_.txt", "r") as _glbltask:
            for line in _glbltask:
                line = line.replace("\n", "")
                _TASK.append(line)
                line = line.replace("\n", "")

    if os.path.isfile(CACHE_DIR + "_STRUCTURE_.txt"):
        with open(CACHE_DIR + "_STRUCTURE_.txt", "r") as _glblstrct:
            for line in _glblstrct:
                line = line.replace("\n", "")
                _STRUCTURE.append(line)

    if os.path.isfile(CACHE_DIR + "_MODIFIER_.txt"):
        with open(CACHE_DIR + "_MODIFIER_.txt", "r") as _glblmod:
            for line in _glblmod:
                line = line.replace("\n", "")
                _MODIFIER.append(line)

    if os.path.isfile(CACHE_DIR + "_TYPE_.txt"):
        with open(CACHE_DIR + "_TYPE_.txt", "r") as _glbltype:
            for line in _glbltype:
                line = line.replace("\n", "")
                _TYPE.append(line)

    if os.path.isfile(CACHE_DIR + "_SUPERFLUOUS_.txt"):
        with open(CACHE_DIR + "_SUPERFLUOUS_.txt", "r") as _glblsprfl:
            for line in _glblsprfl:
                line = line.replace("\n", "")
                _SUPERFLUOUS.append(line)

def deconstruct (snt):
    snt = snt.lower()
    return snt.split(" ")

def matchword(wrd):
    lbl = ""
    if wrd in stdsyn:
        wrd = stdsyn[wrd]

    if wrd in _TASK:
        lbl = "TASK"
    elif wrd in _STRUCTURE:
        lbl = "STRUCTURE"
    elif wrd in _TYPE:
        lbl = "TYPE"
    elif wrd in _MODIFIER:
        lbl = "MODIFIER"
    elif wrd in _SUPERFLUOUS:
        lbl = "SUPERFLUOUS"
    else:
        lbl = synonymfinder.find(wrd)
    # print(sys.path)
    return (wrd, lbl)

def label (sentence):
    _loadCache()

    sentence = deconstruct(sentence)

    sentence = [matchword(word) for word in sentence]
    # print("Test")
    return sentence

# print(label("This is a test."))
