import ast
from archsMod import archs
from fractions import Fraction

matrixfile = open("archmatrix.txt", "r")

numArchs = len(archs)
f1 = matrixfile.readlines()
comMatrix = []

def sortSecond(val):
    return val[1]

# combines two rows of tuple with the same length
def combineRows(row1,row2):
    if (len(row1) != len(row2)):
        print "ERROR: Attempted to combine rows of different length"
        return -1
    for j in range(len(row1)):
        row1[j][0] += row2[j][0]
        row1[j][1] += row2[j][1]
    return row1

def printMatrix(imat):
    for i in range(len(imat)):
        print imat[i]

def initCombMat(imat):
    for i in range(len(archs)):
        comMatrix.append(0)

def collapseRows(iMatrix):
    i=0
    for x in f1:
        if (iMatrix[i] == 0):
            iMatrix[i] = ast.literal_eval(x)
        else:
            iMatrix[i] = combineRows(iMatrix[i], ast.literal_eval(x))
        if (i == len(archs)-1):
            i = 0
        else:
            i += 1
    return iMatrix

#TODO: this is similar to what is done in parseArch, generalize+combine
def printInfo(iMatrix):
    winrates = []
    for i in range(numArchs):
        print str(archs[i][0]) + ": " + str(iMatrix[i])
        winrates.append([archs[i][0],0])
    for i in range(numArchs):
        classWins = 0
        classGames = 0
        for j in range(numArchs):
            classWins += iMatrix[i][j][0]
            classGames += iMatrix[i][j][1]
        winrates[i][1] = Fraction(classWins,classGames)
    winrates.sort(key = sortSecond)
    for i in range(len(winrates)):
        print (winrates[i][0] + " = " + str(round(float(winrates[i][1]),4)))

#initCombMat(comMatrix)
#comMatrix = collapseRows(comMatrix)
#printInfo(comMatrix)
