## -*- coding: utf-8 -*-

from fractions import Fraction
import json
import sys
from archsMod import archs

############## GLOBAL BECAUSE FUCK #####

datafile = open("data.txt", 'r')
matrixfile = open("archmatrix.txt", "a+")

############## CONSTANTS ###############

numClasses = 8
isTop16 = 0
numArchs = len(archs)

########################################

def sortSecond(val):
    return val[1]

# Takes as input the full list of players
# Returns a list of players who actually participated in the tournament
def top256(dct):
    outputplayers = []
    for player in dct:
        if player["te"]:
            outputplayers.append(player)
    return outputplayers

def getarch(hashval):
    # Make sure that all the indicators are in the decklist we are looking at
    for i in range(numArchs):
        correct = 1
        for ind in archs[i][1]:
            if (hashval.find(ind) == -1):
                correct = 0
        if (correct == 1):
            return i
    #TODO: this indicates an error, fix it so that there are generic decks for each class
    print "ERROR"
    return 1000

# Takes as input a list of participants
# Returns a table with the participants name and the archetypes they played, each entry in of the form:
# [playername, arch1, arch2, additional data]
def createTable(participants):
    table = []
    for player in participants:
        playerentry = [player['nm']]
        for deck in player['dk']:
            playerentry.append(getarch(deck['hs']))
        playerentry.append(0)
        playerentry.append(0)
        table.append(playerentry)
    return table

def archetype_selection(participants, arch):
    output = 0
    for player in participants:
        for deck in player['dk']:
            if (getarch(deck['hs']) == arch):
                output += 1
    return output

def get_archetype_selection(participants):
    output = []
    for i in range(len(archs)):
        num_of_i = archetype_selection(participants, i)
        output.append(num_of_i)
    return output

def print_arch_selection(participants):
    print "Number of Entrants for each archetype:"
    arch_distrib = get_archetype_selection(participants)
    for i in range(len(archs)):
        print archs[i][0] + ": " + str(arch_distrib[i])

# this should only ever be called by createMatchTable(), it requires datafile to be at a specific
# point to extract the result of the "next" match
# Match entries are of the form [Player1, Player2, Winner (either 1 or 2)]
def getMatchEntry():
    #skipping html lines to get to actual info
    for i in range(8):
        datafile.readline()

    #next line has number of games won for the first player
    score1 = datafile.readline()[23]

    #the next line has the first player, hidden in html
    helper = datafile.readline()
    index1 = helper.find(">")
    index2 = helper.rfind("<")
    player1 = helper[index1+1:index2]

    #skipping more html lines to get to info
    datafile.readline()
    helper = datafile.readline()
    isWinnerTwo = helper.find("winner")

    #Same as for score1 and player1
    score2 = datafile.readline()[23]
    helper = datafile.readline()
    index1 = helper.find(">")
    index2 = helper.rfind("<")
    player2 = helper[index1+1:index2]

    #making non-english characters work with playerTable
    player1 = player1.decode('utf-8')
    player2 = player2.decode('utf-8')

    if (isWinnerTwo < 0):
        return [player1, player2, 1]
    else:
        return [player1, player2, 2]

#creates a table of all the matches in data.txt by going through the html (this doesnt currently include top 16).
def createMatchTable():
    matchTable = []
    nextline = datafile.readline()

    #simple hack, the end of the file will close the html
    while (nextline.find("</html>") == -1):
        #whenever we see a match, this may have to be changed, it is a little sensitive
        if (nextline.find("onClick=") > -1):
            matchTable.append(getMatchEntry())
        nextline = datafile.readline()

    return matchTable


def main():
    # Get the json that was pulled
    jsonfile = open(sys.argv[1], 'r')
    data = json.loads(jsonfile.readline())
    jsonfile.close()

    # Get the participants that actually played
    partic = data['participants']
    participants = top256(partic)

    # If we are in the top 16, output all the decklists
    if (len(participants) == 16):
        for player in participants:
            for deck in player['dk']:
                print archs[getarch(deck['hs'])][0]
                print "https://shadowverse-portal.com/deck/" + deck['hs']
                isTop16 = 1

    # Output
    print_arch_selection(participants)

    # Put this elsewhere probably
    archSetWins = []
    archSetLosses = []
    top16 = []
    for i in range(numArchs):
        archSetWins.append(0)
        archSetLosses.append(0)
        top16.append(0)

    # Make the table of players, entries are of the form: [Name, Arch1, Arch2, additional data1,
    # additional data2]
    playerTable = createTable(participants)

    # Make the table of matches, entires are of the form: [Player1, Player2, Player1 wins, Player2 wins]
    matchTable = createMatchTable()

    # Move this to a separate function. This could be done in O(mlogn) by sorting the player table.
    for match in matchTable:
        winner = match[2]-1
        loser = match[2] % 2
        for player in playerTable:
            if ((match[winner] == player[0]) and (player[3] != 4) and (player[4] != 1)):
                player[3] += 1
                archSetWins[player[1]] += 1
                archSetWins[player[2]] += 1
            if ((match[loser] == player[0]) and (player[3] != 4) and (player[4] != 1)):
                player[4] += 1
                archSetLosses[player[1]] += 1
                archSetLosses[player[2]] += 1

    #Move to separate function
    matchupMatrix = []
    for i in range(numArchs):
        nextrow = []
        for j in range(numArchs):
            nextrow.append([0,0])
        matchupMatrix.append(nextrow)

    #NOTE: this fucks up with several players with the same name
    for match in matchTable:
        winner = -1
        loser = -1
        if (match[2] == 2):
            winner = 1
            loser = 0
        else:
            winner = 0
            loser = 1

        winClass1 = -1
        winClass2 = -1
        lossClass1 = -1
        lossClass2 = -1

        for player in playerTable:
            if (match[winner] == player[0]):
                winClass1 = player[1]
                winClass2 = player[2]
            if (match[loser] == player[0]):
                lossClass1 = player[1]
                lossClass2 = player[2]

        if ((winClass1 == -1) or (winClass2 == -1) or (lossClass1 == -1) or (lossClass2 == -1)):
            #something weird happened, the player decks werent found in the JSON
            continue

        if (not (((winClass1 == lossClass1) and (winClass2 == lossClass2))
                or ((winClass1 == lossClass2) and (winClass2 == lossClass1)))):
            matchupMatrix[winClass1][lossClass1][0] += 1
            matchupMatrix[winClass2][lossClass1][0] += 1
            matchupMatrix[winClass1][lossClass1][1] += 1
            matchupMatrix[winClass2][lossClass1][1] += 1

            matchupMatrix[winClass1][lossClass2][0] += 1
            matchupMatrix[winClass2][lossClass2][0] += 1
            matchupMatrix[winClass1][lossClass2][1] += 1
            matchupMatrix[winClass2][lossClass2][1] += 1

            matchupMatrix[lossClass1][winClass1][1] += 1
            matchupMatrix[lossClass1][winClass2][1] += 1
            matchupMatrix[lossClass2][winClass1][1] += 1
            matchupMatrix[lossClass2][winClass2][1] += 1

    for player in playerTable:
        if (player[3] == 4):
            top16[player[1]] += 1
            top16[player[2]] += 1

    winrateTable = []

    for i in range(numArchs):
        winrateTable.append([archs[i][0],0])

    for i in range(numArchs):
        if (archSetWins[i]+archSetLosses[i] == 0):
            winrateTable[i][1] = 0
        else:
            winrateTable[i][1] = Fraction(archSetWins[i],archSetWins[i]+archSetLosses[i])

    winrateTable.sort(key = sortSecond)

    print "\nWinrates:"
    for i in range(numArchs):
        print (winrateTable[i][0] + " = " + str(round(float(winrateTable[i][1]),4)))

    print "\nSets won by each archetype: "
    print archSetWins
    print "\nSets lost by each archetype: "
    print archSetLosses
    print "\nNumber of each archetype hitting top 16: "
    print top16
    print "\nMatchup Matrix:"
    for i in range(numArchs):
        matrixfile.write(str(matchupMatrix[i]) + "\n")
        print archs[i][0] + ": " + str(matchupMatrix[i])


main()
