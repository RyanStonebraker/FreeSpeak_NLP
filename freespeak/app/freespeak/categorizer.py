import os
import re
import sys
import synonymfinder
import taskhandle
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


# stores all wordcache files into memory so they can be referenced
# the idea behind this was to optimize tasks server side so that the more
# data was enterred, the quicker parts of speech could be identified.
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


# simple regex function that splits based on spaces, but preserves things in
# quotations
def deconstruct(snt):
    snt = snt.lower()
    pattern = re.compile(r'''((?:[^ "]|"[^"]*")+)''')
    return [wrd for wrd in pattern.split(snt) if wrd != "" and wrd != " "]


# casts a word as an int or float, and if it fails, then its not a number.
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
# -checks to see whether string is quoted
def checkString(poss_str):
    if re.match(r'^\"(.)+\"$', poss_str):
        return True
    return False


# Returns whether string is a boolean true or false and then includes
# what the string would evaluate to as a boolean
def checkBool(poss_str):
    return((poss_str == "true" or poss_str == "false"), poss_str == "true")


# does some minor string scrubbing and then checks to see if word is already
# cached, if not it gets sent off to the synonym finder to see if it should be
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
    elif checkBool(wrd)[0]:
        wrd = checkBool(wrd)[1]
        lbl = "BOOLEAN"
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


# Writes out all changes to the cache as a set so there are no repeated values
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


# compiles a regex expression converting 1st, 2nd, 3rd, 4th, 5th,... to numbers
# technically this would strip 11nd or 50rd as well, but english is messy..
checkNumEnd = re.compile(r"(\s[0-9]+)((?:rd|th|st|nd))\s", re.IGNORECASE)


# replaces conjunction words with spaces and symbols to words and returns a
# copy of the original sentence passed paired with each word's labels
def label(sentence):
    _loadCache()

    sentence = sentence.replace("  ", " ")
    sentence = sentence.replace(" and ", " ")
    sentence = sentence.replace(" & ", " ")
    sentence = sentence.replace(",", " ")
    sentence = sentence.replace("+", " plus ")
    sentence = sentence.replace("-", " minus ")
    sentence = sentence.replace("*", " multiplied ")
    sentence = sentence.replace("/", " divided ")
    sentence = sentence.replace("  ", " ")
    sentence = re.sub(checkNumEnd, r'\1 ', sentence)

    sentence = deconstruct(sentence)

    sentence = [matchword(word) for word in sentence]

    _unloadCache()

    # print (sentence) # debug output
    return (sentence, taskhandle.getcontext(sentence))
