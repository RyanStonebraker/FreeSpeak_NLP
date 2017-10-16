import os
import re
import sys
from freespeak import synonymfinder
from freespeak import taskhandle
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
                stdsyn[line[:line.find(":")]] = line[line.find(":") + 1:]

    if os.path.isfile(CACHE_DIR + "_TASK_.txt"):
        with open(CACHE_DIR + "_TASK_.txt", "r") as _glbltask:
            for line in _glbltask:
                line = line.replace("\n", "")
                _TASK.append(line)

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


def deconstruct(snt):
    snt = snt.lower()
    pattern = re.compile(r'''((?:[^ "]|"[^"]*")+)''')

    return [wrd for wrd in pattern.split(snt) if wrd != "" and wrd != " "]


def checkNum(str_num):
    if str_num.isnumeric():
        return True
    else:
        try:
            float(str_num)
            return True
        except:
            return False
    return False


# Can't return re.match because it returns object, but python if statements
# can check "truthness" of a statement (not a bool)
def checkString(poss_str):
    if re.match(r'^\"(.)+\"$', poss_str):
        return True
    return False


def matchword(wrd):
    lbl = ""
    wrd = wrd.strip(",'[]\{\}\\/|")

    if wrd in stdsyn:
        wrd = stdsyn[wrd]

    if checkNum(wrd):
        lbl = "NUMBER"
    elif checkString(wrd):
        wrd = wrd[1:-1]
        lbl = "STRING"
    elif wrd in _TASK:
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
        wrdlbl = synonymfinder.find(wrd)
        lbl = wrdlbl[1]
        wrd = wrdlbl[0]
    return (wrd, lbl)


def _unloadCache():
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    CACHE_DIR = BASE_DIR + "/wordcache/"

    with open(CACHE_DIR + "_synlist_.txt", "w") as _outSYN:
        for key in set(stdsyn):
            _outSYN.write(key + ":" + stdsyn[key] + "\n")
    with open(CACHE_DIR + "_MODIFIER_.txt", "w") as _outMOD:
        for line in set(_MODIFIER):
            _outMOD.write(line + "\n")
    with open(CACHE_DIR + "_STRUCTURE_.txt", "w") as _outSTRUCT:
        for line in set(_STRUCTURE):
            _outSTRUCT.write(line + "\n")
    with open(CACHE_DIR + "_SUPERFLUOUS_.txt", "w") as _outSPR:
        for line in set(_SUPERFLUOUS):
            _outSPR.write(line + "\n")
    with open(CACHE_DIR + "_TASK_.txt", "w") as _outTASK:
        for line in set(_TASK):
            _outTASK.write(line + "\n")
    with open(CACHE_DIR + "_TYPE_.txt", "w") as _outTYPE:
        for line in set(_TYPE):
            _outTYPE.write(line + "\n")


def label(sentence):
    _loadCache()

    sentence = sentence.replace("  ", " ")
    sentence = sentence.replace(" and ", " ")
    sentence = sentence.replace(" & ", " ")
    sentence = sentence.replace(",", " ")
    sentence = sentence.replace("  ", " ")

    sentence = deconstruct(sentence)

    sentence = [matchword(word) for word in sentence]

    _unloadCache()

    return taskhandle.getcontext(sentence)
