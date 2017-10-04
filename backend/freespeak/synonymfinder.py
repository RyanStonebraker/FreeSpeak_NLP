import requests
from freespeak import categorizer

def webscrape(wrd):
    url = "http://words.bighugelabs.com/api/2/1166c33a777038684549d7422cc054fc/" + wrd + "/json"
    results = requests.get(url).json()
    results = [results[key] for key in results]
    results = results[0]['syn']
    print (results)


def find(unk):
    stdsyn = {}
    _TASK = []
    _STRUCTURE = []
    _MODIFIER = []
    _TYPE = []
    _SUPERFLUOUS = []

    categorizer._loadCache()

    synonyms = webscrape(unk)

    print(synonyms)
