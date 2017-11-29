import requests
import categorizer


# Simple webscraper that utilizes a json formatted api to check synonyms for
# words -- bighugelabs doesn't return a huge list of synonyms for their api
# requests, so in the future I might just front end scrape a bigger thesaurus
def webscrape(wrd):
    api_key = "1166c33a777038684549d7422cc054fc"
    url = "http://words.bighugelabs.com/api/2/" + api_key + "/" + wrd + "/json"
    results = requests.get(url)
    if results.status_code == 200:
        results = results.json()
        results = [results[key] for key in results]
        try:
            results = results[0]['syn']
        except:
            print("<script>console.log(" + wrd + ");</script>")
            return [""]
    else:
        results = ""
    return results


# compares all synonyms of unknown word to words stored in caches, if there was
# a huge list of synonyms and huge caches, this would be terribly inefficient..
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

    if known_syn != unk:
        categorizer.stdsyn[unk] = known_syn
    else:
        categorizer._SUPERFLUOUS.append(unk)

    return (known_syn, label)
