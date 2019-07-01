## -*- coding: utf-8 -*-

import requests
import sys
import json
import codecs
import datetime
from patchDates import *

# Returns the patch that was active at the time of the input date
def getPatch(date):
    mostRecent = dates[0][1]
    for day in dates:
        if (day[0] < date):
            mostRecent = day[1]
    return mostRecent

# Does most of the actual work of getRecent, and should only be called by that function.
def getRecentFromLink(link):
    r = requests.get(link)
    with codecs.open("tempjcg.txt", "w", encoding='utf-8') as out:
        out.write(r.text)
    htmlfile = open("tempjcg.txt", 'r')
    nextline = htmlfile.readline()

    top16Tours = []
    groupTours = []

    while (nextline.find("</html>") == -1):
        if (nextline.find("competition commit") != -1):
            tourNum = nextline[52:56]
            dateline = htmlfile.readline()
            year = dateline[21:23]
            month = dateline[24:26]
            day = dateline[27:29]
            tourdate = datetime.datetime(int("20" + year), int(month), int(day))
            patch = getPatch(tourdate)
            htmlfile.readline()
            nextline = htmlfile.readline()
            if (nextline.find("トーナメント") != -1):
                top16Tours.append([tourNum, patch])
            else:
                groupTours.append([tourNum, patch])
        nextline = htmlfile.readline()

    return [groupTours, top16Tours]


# Writes the entrylist from the jcg with the input tournament number to "entrylist.txt"
# Returns two lists; the first list are the tournaments starting with 256 entrants (sorted from newest to
# oldest), the second list are the corresponding matches from the top 16 of the corresponding
# tournaments
# Output is a pair of lists, group round and top 16 rounds, respectively. Each list has entries of
# the form ["tour number", "name of patch"]
def getRecent():
    # Pull the most recent rotation JCGs so that the user can determine the tour number without
    # going to the JCG website
    # Page2 are the older tournament results
    # This could probably be made into a single page pull
    page2 = getRecentFromLink('https://sv.j-cg.com/compe/rotation?perpage=20&start=20')
    page1 = getRecentFromLink('https://sv.j-cg.com/compe/rotation')

    ret = page1

    for tour in page2[0]:
        ret[0].append(tour)

    for tour in page2[1]:
        ret[1].append(tour)

    return ret


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

#jcgPull(sys.argv[1])
