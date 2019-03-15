## -*- coding: utf-8 -*-

from fractions import Fraction
import json
import sys

############## GLOBAL BECAUSE FUCK #####

datafile = open("data.txt", 'r')
matrixfile = open("matrix.txt", "a+")

############## CONSTANTS ###############

numClasses = 8

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

# Takes as input a list of participants
# Returns a table with the participants name and the classes they played, each entry in of the form:
# [playername, class1, class2, additional data]
def createTable(participants):
    table = []
    for player in participants:
        playerentry = [player['nm']]
        for deck in player['dk']:
            playerentry.append(deck['cl'])
        playerentry.append(0)
        playerentry.append(0)
        table.append(playerentry)
    return table

# Takes in a list of participants
# Returns the number of participants that brought a deck with the class associated with classnum
# Forest = 1
# Sword = 2
# Rune = 3
# Dragon = 4
# Shadow = 5
# Blood = 6
# Haven = 7
# Portal = 8
def class_selection(participants, classnum):
    output = 0
    for player in participants:
        for deck in player['dk']:
            if deck['cl'] == classnum:
                output += 1
    return output

# Takes in a list of participants
# Returns a list of the number of participants in the 8 classes
def get_class_selection(participants):
    output = []
    for i in range(numClasses):
        num_of_i = class_selection(participants, i+1)
        output.append(num_of_i)
    return output

# Takes in a list of participants
# Prints what the distribution of classes were in the tournament
# TODO: could be better with a loop and enum
def print_class_selection(participants):
    print "Number of Entrants for each class:"
    class_distrib = get_class_selection(participants)
    print "Forest: " + str(class_distrib[0])
    print "Sword: " + str(class_distrib[1])
    print "Rune: " + str(class_distrib[2])
    print "Dragon: " + str(class_distrib[3])
    print "Shadow: " + str(class_distrib[4])
    print "Blood: " + str(class_distrib[5])
    print "Haven: " + str(class_distrib[6])
    print "Portal: " + str(class_distrib[7])

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
    player1=player1.decode('utf-8')
    player2=player2.decode('utf-8')

    if (isWinnerTwo < 0):
        return [player1, player2, 1]
    else:
        return [player1, player2, 2]

#creates a table of all the matches in data.txt (this doesnt currently include top 16).
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

    # Output
    print_class_selection(participants)

    # Put this elsewhere probably
    classSetWins = [0,0,0,0,0,0,0,0]
    classSetLosses = [0,0,0,0,0,0,0,0]
    top16 = [0,0,0,0,0,0,0,0]

    # Make the table of players, entries are of the form: [Name, Class1, Class2, additional data1,
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
                classSetWins[player[1]-1] += 1
                classSetWins[player[2]-1] += 1
            if ((match[loser] == player[0]) and (player[3] != 4) and (player[4] != 1)):
                player[4] += 1
                classSetLosses[player[1]-1] += 1
                classSetLosses[player[2]-1] += 1

    #Move to separate function
    matchupMatrix = []
    for i in range(8):
        nextrow = []
        for j in range(8):
            nextrow.append([0,0])
        matchupMatrix.append(nextrow)

    #NOTE: this fucks up with several players with the same name
    #TODO: finish this function: see what class each players are playing, add to table
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
                winClass1 = player[1]-1
                winClass2 = player[2]-1
            if (match[loser] == player[0]):
                lossClass1 = player[1]-1
                lossClass2 = player[2]-1

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
            top16[player[1]-1] += 1
            top16[player[2]-1] += 1
            print player[0]

    winrateTable = [["Forest",0],["Sword",0],["Rune",0],["Dragon",0],["Shadow",0],["Blood",0],["Haven",0],["Portal",0]]

    for i in range(8):
        if (classSetWins[i]+classSetLosses[i] == 0):
            winrateTable[i][1] = 0
        else:
            winrateTable[i][1] = Fraction(classSetWins[i],classSetWins[i]+classSetLosses[i])

    winrateTable.sort(key = sortSecond)

    print "\nWinrates:"
    for i in range(8):
        print (winrateTable[i][0] + " = " + str(round(float(winrateTable[i][1]),4)))

    print "\nSets won by each class: "
    print classSetWins
    print "\nSets lost by each class: "
    print classSetLosses
    print "\nNumber of each class hitting top 16: "
    print top16
    print "\nMatchup Matrix:"
    for i in range(8):
        #matrixfile.write(str(matchupMatrix[i]) + "\n")
        print matchupMatrix[i]

main()
