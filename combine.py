import ast
from archsMod import archs

matrixfile = open("archmatrix.txt", "r")

f1 = matrixfile.readlines()
comMatrix = []

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

def initMat(imat):
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

#def printInfo(iMatrix):

initMat(comMatrix)
comMatrix = collapseRows(comMatrix)
printMatrix(comMatrix)
