import ast

matrixfile = open("matrix.txt", "r")

f1 = matrixfile.readlines()
comMatrix = [0,0,0,0,0,0,0,0]

def combineRows(row1,row2):
    for j in range(len(row1)):
        row1[j][0] += row2[j][0]
        row1[j][1] += row2[j][1]
    return row1

i=0
for x in f1:
    if (comMatrix[i] == 0):
        comMatrix[i] = ast.literal_eval(x)
    else:
        comMatrix[i] = combineRows(comMatrix[i], ast.literal_eval(x))
    if (i==7):
        i=0
    else:
        i+=1

for i in range(len(comMatrix)):
    print comMatrix[i]

