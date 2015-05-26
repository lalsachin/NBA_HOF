from sklearn.neighbors import KNeighborsClassifier
import glob
import csv
import numpy
import os

knn = KNeighborsClassifier(n_neighbors = 1)
print(knn)
def getData():
    #for each csv file
    #append features and target to global arrays X and y
    #convert to and return numpy ndarray
    X = []
    y = []
    for fName in glob.glob('Training/*'):
        with open(fName, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            attributesRaw = reader.next()
            attributesRaw = attributesRaw[0].split(",")
            attributesList = [attributesRaw[1]] + attributesRaw[4:len(attributesRaw)]
            tempList = []
            target = os.path.basename(fName)
            target = target[len(target)-5:len(target)-4]
            y.append(int(target))
            preAvgList = []
            for i in range(4):
                rawRow = reader.next()
                rawRow = rawRow[0].split(",")
                for j in range(len(attributesRaw)):
                    filteredList = [rawRow[1]] + [positionConvert(rawRow[4])] +  rawRow[5:len(attributesRaw)]
                    finalList = [float(elem) for elem in filteredList]
                preAvgList.append(finalList)
            absoluteFinal = []
            for attr in range(len(finalList)):
                avgAttr = 0.0
                for ls in preAvgList:
                     avgAttr += ls[attr]
                avgAttr /= 4.0
                absoluteFinal.append(avgAttr)
            X.append(absoluteFinal)
                                    

    X = numpy.array(X)
    y = numpy.array(y)
    print(X.shape)
    knn.fit(X,y)

def positionConvert(stringPos):
    returnVal = 1
    if (stringPos == "PG"):
        returnVal = 1
    elif (stringPos == "SG"):
        returnVal = 2
    elif (stringPos == "SF"):
        returnVal = 3
    elif (stringPos == "PF"):
        returnVal = 4
    elif (stringPos == "C"):
        returnVal = 5
    return returnVal
