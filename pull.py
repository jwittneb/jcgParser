import requests
import sys
import json
import codecs

def myPull(tourNum):
    #we take in the tournament id that we want to analyze as input, later on this should be part of the UI
    r = requests.get('https://sv.j-cg.com/compe/view/entrylist/' + tourNum + '/json')
    f = open("entrylist.txt", "w")
    f.write(r.text)
    f.close()

    #there isnt a json file corresponding to this, codecs used to deal with non-ascii
    r = requests.get('https://sv.j-cg.com/compe/view/tour/' + sys.argv[1])
    with codecs.open("data.txt", "w", encoding='utf-8') as out:
        out.write(r.text)

myPull(sys.argv[1])
