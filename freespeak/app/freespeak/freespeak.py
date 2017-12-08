import re
import categorizer
# from freespeak import NLPinterpret
# from freespeak import synonymfinder
import taskhandle


# handles internal identification of natural language
def identify(nltext):
    # splits sentences based on a period/space or a period/newline
    parsed = re.split(r"\.+\s+|\n+|\.$", nltext)

    # removes all entries that are blank
    parsed = [entry for entry in parsed if entry != ""]

    # sends each sentence individually to be labelled for context and
    # then puts them in a list
    labeled = []
    total_labeled = ""
    variables = []
    for sentence in parsed:
        fullLabel = categorizer.label(sentence, variables)
        total_labeled += str(fullLabel[0])
        labeled.append(fullLabel[1])
        for v in fullLabel[2]:
            if v not in variables:
                variables.append(v)

    return (total_labeled, labeled)
