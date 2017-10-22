import re
from freespeak import categorizer
# from freespeak import NLPinterpret
# from freespeak import synonymfinder
from freespeak import taskhandle


# handles internal identification of natural language
def identify(nltext):
    # splits sentences based on a period/space or a period/newline
    parsed = re.split(r"\.+\s+|\n+|\.$", nltext)

    # removes all entries that are blank
    parsed = [entry for entry in parsed if entry != ""]

    # sends each sentence individually to be labelled for context and
    # then puts them in a list
    labeled = [categorizer.label(sentence) for sentence in parsed]
    return labeled
