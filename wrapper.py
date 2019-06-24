from pull import *
from parseArch import *
from combine import *
from patchDates import *

mostRecent = getRecent()

tourFile = open("tempjcg","r")

fullResults = 0

print "Would you like the fill results from a specific patch?"

print "Which JCG would you like the results from?"
for i in range(len(mostRecent[0])):
    print str(i+1) + ": " + str(mostRecent[0][i])
uinput = int(raw_input(""))

jcgPull(mostRecent[0][uinput-1])
main()

#if combining
#initCombMat(comMatrix)
#comMatrix = collapseRows(comMatrix)
#printInfo(comMatrix)
