from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import cross_validation

import glob
import csv
import numpy
import os

def getData(dataSet):
    #for each csv file
    #append features and target to global arrays X and y
    #convert to and return numpy ndarray
    X = []
    y = []
    for fName in glob.glob(dataSet + '/*'):
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
    return [X,y]
  


def trainModel(modelInstance, X, y):
    X = numpy.array(X)
    y = numpy.array(y)
    ret = modelInstance.fit(X,y)
    return ret



    
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


def test(model, X):
    x = model.predict(X)
    x = x.tolist()
    return( x)
        
def evaluate(y, yPredict):
    score = metrics.accuracy_score(y,yPredict)
    return score

def writeToCSV(X,y):
    listToCSV = []
    for i in range(len(X)):
        l=list(X[i])
        l.append(y[i])
        #print len(l)
        listToCSV.append(l)
    with open('zeroR.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(listToCSV)
    print 'Done write CSV File'

def CV(model,data,target, numFolds=10):
    print 'start CV'
    s = cross_validation.cross_val_score(model, data,target,cv=numFolds)
    print 'Done with CV'
    s = s.tolist()
    s = numpy.mean(s)
    #print s
    return s

def crossValidate():
    trainingData = getData("Training")
    for i in range(1):
        #knn = KNeighborsClassifier(n_neighbors = i+1, weights="distance")
        #DT = tree.DecisionTreeClassifier(max_depth=8,min_samples_leaf=i+1)
        #SVM = svm.SVC(kernel='sigmoid')
        LR = linear_model.LinearRegression()
        print LR
        s=CV(LR,trainingData[0],trainingData[1],5)
        d = (i+1,s)
        print str(i+1) + ',' + str(s)
        

def main():
    #knn = KNeighborsClassifier(n_neighbors = 2, weights="distance")
    SVM = svm.SVC(kernel='linear')
    print(SVM)
    trainingData = getData("Training")
    model = trainModel(SVM, trainingData[0],trainingData[1])
 #   writeToCSV(trainingData[0],trainingData[1])
    testingData = getData('Testing')
    t =  test(model, testingData[0])
    score = evaluate(testingData[1], t)
    print score
    return score
