from math import factorial

checkedVals = []
sumList = []

def multiZeus(plus3, plus2, plus1, plus0):
    total = plus3 + plus2 + plus1 + plus0
    return (factorial(total)/(factorial(plus3)*factorial(plus2)*factorial(plus1)*factorial(plus0)))*(0.2**(plus3+plus2+plus1))*(0.4**plus0)

def multiTruth(damage, heal):
    total = damage + heal
    return (factorial(total)/(factorial(damage)*factorial(heal)))*(0.3333333**(damage))*(0.6666666**(heal))

# curr is of the form "abcde", where a is the number of plus 3, b is the number of plus 2, etc.
def recZeusProb(target, curr):

    # this specific set of boosts has not yet been checked
    if (curr not in checkedVals):
        checkedVals.append(curr)

        plus3 = curr[0]
        plus2 = curr[1]
        plus1 = curr[2]
        plus0 = curr[3]

        sumList.append(multiZeus(plus3, plus2, plus1, plus0))

        # Check to see if we are done or need to continue recursing
        if (plus3*3 + plus2*2 + plus1 > target):
            if (plus3 > 1):
                recZeusProb(target, [plus3-1, plus2+1, plus1, plus0])
            if (plus2 > 0):
                recZeusProb(target, [plus3, plus2-1, plus1+1, plus0])
            if (plus1 > 0):
                recZeusProb(target, [plus3, plus2, plus1-1, plus0+1])

def recTruthProb(target, curr):

    # this specific set of boosts has not yet been checked
    if (curr not in checkedVals):
        checkedVals.append(curr)

        damage = curr[0]
        nondamage = curr[1]

        sumList.append(multiTruth(damage, nondamage))

        # Check to see if we are done or need to continue recursing
        if (damage > target):
                recTruthProb(target, [damage-1, nondamage+1])

def main(numEvos, target):
    if ((numEvos-1)*3 + 2 < target-5):
        return 0
    else:
        recZeusProb(target-5, [numEvos-1,1,0,0])
        total = 0
        for probab in sumList:
            total += probab
        del checkedVals[:]
        del sumList[:]
    return round(total,4)

def truthVal(numBoost, target):
    if (numBoost < target):
        return 0
    else:
        recTruthProb(target, [numBoost, 0])
        total = 0
        for probab in sumList:
            total += probab
        del checkedVals[:]
        del sumList[:]
    return round(total, 4)

def zeusMain():
    for j in range(15):
        oneRow = ""
        for i in range(21):
            if (i == 10):
                oneRow = str(main(j+1,i))
            if (i > 10):
                oneRow = oneRow + ", " + str(main(j+1,i))
        print oneRow

def truthMain():
    for i in range(30):
        oneRow = ""
        for j in range(21):
            if (j == 0):
                oneRow = str(truthVal(i,j+1))
            else:
                oneRow = oneRow + ", " + str(truthVal(i,j+1))
        print oneRow

truthMain()
