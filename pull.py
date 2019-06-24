## -*- coding: utf-8 -*-

import requests
import sys
import json
import codecs

# Returns two lists; the first list are the tournaments starting with 256 entrants (sorted from newest to
# oldest), the second list are the corresponding matches from the top 16 of the corresponding
# tournaments
def getRecent():
    # Pull the most recent rotation JCGs so that the user can determine the tour number without
    # going to the JCG website
    r = requests.get('https://sv.j-cg.com/compe/rotation')
    with codecs.open("tempjcg.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
    htmlfile = open("tempjcg.txt", 'r')
    nextline = htmlfile.readline()

    top16Tours = []
    groupTours = []

    while (nextline.find("</html>") == -1):
        if (nextline.find("competition commit") != -1):
            tourNum = nextline[52:56]
            htmlfile.readline()
            htmlfile.readline()
            nextline = htmlfile.readline()
            if (nextline.find("トーナメント") != -1):
                top16Tours.append(tourNum)
            else:
                groupTours.append(tourNum)
        nextline = htmlfile.readline()

    return [groupTours, top16Tours]


# Writes the entrylist from the jcg with the input tournament number to "entrylist.txt"
# Writes the html of the tournament page with the input tournament number to "data.txt"
def jcgPull(tourNum):
    # We take in the tournament id that we want to analyze as input, later on this should be part of the UI
    r = requests.get("https://sv.j-cg.com/compe/view/entrylist/" + tourNum + "/json")
    f = open("entrylist.txt", "w")
    f.write(r.text)
    f.close()

    # There isnt a json file corresponding to this, codecs is used to deal with non-ascii characters
    r = requests.get("https://sv.j-cg.com/compe/view/tour/" + tourNum)
    with codecs.open("data.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
