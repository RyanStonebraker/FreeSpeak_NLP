import re
from freespeak import categorizer
# from freespeak import NLPinterpret
# from freespeak import synonymfinder
# from freespeak import taskhandle

def handle(nltext):
    parsed = re.split(r"\.+\s+|\n+|\.$", nltext)
    parsed = [entry for entry in parsed if entry != ""]

    labeled = [categorizer.label(sentence) for sentence in parsed]
    return labeled
