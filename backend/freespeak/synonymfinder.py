import requests
from freespeak import categorizer

def webscrape(wrd):
    url = "http://words.bighugelabs.com/api/2/1166c33a777038684549d7422cc054fc/" + wrd + "/json"
    results = requests.get(url)
    if results.status_code == 200:
        results = results.json()
        results = [results[key] for key in results]
        results = results[0]['syn']
    else:
        results = ""
    return results


def find(unk):
    synonyms = webscrape(unk)

    label = "SUPERFLUOUS"
    known_syn = unk
    for syn in synonyms:
        if syn in categorizer._TASK:
            label = "TASK"
            known_syn = syn
            break
        elif syn in categorizer._STRUCTURE:
            label = "STRUCTURE"
            known_syn = syn
            break
        elif syn in categorizer._MODIFIER:
            label = "MODIFIER"
            known_syn = syn
            break
        elif syn in categorizer._TYPE:
            label = "TYPE"
            known_syn = syn
            break
        elif syn in categorizer._SUPERFLUOUS:
            label = "SUPERFLUOUS"
            known_syn = syn
            break

    if known_syn != unk:
        categorizer.stdsyn[unk] = known_syn
    else:
        categorizer._SUPERFLUOUS.append(unk)

    return (known_syn, label)
