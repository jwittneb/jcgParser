from pull import *
from parseArch import *
from combine import *
from patchDates import *

mostRecent = getRecent()

tourFile = open("tempjcg.txt","r")

fullResults = 0

print "Would you like the full results from a specific patch? (y/n)"
uinput = raw_input("")

if (uinput == "n"):

    print "Which JCG would you like the results from?"
    for i in range(len(mostRecent[0])):
        print str(i+1) + ": " + str(mostRecent[0][i][0]) + ": " + mostRecent[0][i][1]
    uinput = int(raw_input(""))

    jcgPull(mostRecent[0][uinput-1][0])
    main()
elif (uinput == "y"):
    print "Which patch would you like the full results from?"
elif (uinput == "a"):
    jcgPull(mostRecent[0][0][0])
    main()
else:
    print "y/n only"


#if combining
#initCombMat(comMatrix)
#comMatrix = collapseRows(comMatrix)
#printInfo(comMatrix)
