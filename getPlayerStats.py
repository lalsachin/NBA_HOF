from bs4 import BeautifulSoup
import urllib2
import requests
import csv
import os.path
import string
import shutil
import glob
import os
from os import listdir
from os.path import isfile, join

def getPlayerStats(url):
    """Get all the players stats from the url and returns them in a list of lists"""
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    name = soup.find('h1')
    name = name.renderContents()
    allTotal = soup.find('div', attrs={'id':'all_totals'})
    table = allTotal.find('table', attrs={'id':'totals'})
    tableBody = table.find('tbody')
    rows = tableBody.find_all('tr')
    seasons = []
    for tr in rows:
        cols = tr.find_all('td')
        yearStats = []
        for td in cols:
            text = td.find(text=True)
            if text is None:
                text = '0'
            yearStats.append(text.encode('ascii', 'ignore'))
        seasons.append(yearStats)
    returnValue = [seasons, name]
    return returnValue
    
def makePlayerCareerStatisticsFile(url):
    """makes a csv file of the players statistics given a url"""
    header =['Season','Age','Tm','Lg','Pos','G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%',
             'FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS']
    seasonStats = (getPlayerStats(url)[0])
    name = (getPlayerStats(url)[1])
    nameFile = name.replace(' ', '_')

    savePath = '/Users/Sachin/Desktop/NBA_DATA/'
    completeFileName = os.path.join(savePath, nameFile+'.csv')
    f = open(completeFileName, 'w+')
    wr = csv.writer(f)
    wr.writerow(header)
    for i in seasonStats:
        wr.writerow(i)
    f.close()

alphabet = list(string.ascii_lowercase)
def getPlayerLinksPerLetter(url="http://www.basketball-reference.com/players/",letter="a"):
    content = urllib2.urlopen(url+letter).read()
    soup = BeautifulSoup(content)
    link = "/players/"+ letter
    namesRaw = soup.find_all('tr', attrs={'class':""})
    returnNames = []
    for i in range(1,len(namesRaw)):
         returnNames.append(namesRaw[i].find("a")['href'])
    return returnNames
         
def getAllPlayers():
    """gets the links of all players"""
    namesTotal = []
    for char in alphabet:
        for num in range(0,26):
            char = alphabet[num]
            namesTotal.append(getPlayerLinksPerLetter(letter=char))
        #print("done with: " + char)

    return namesTotal

def getAllPlayerStatistics():
    links = getAllPlayers()
    for letter in links:
        for l in letter:
            url = 'http://www.basketball-reference.com'+l
            print url
            makePlayerCareerStatisticsFile(url)
        print('DONE WITH PLAYERS FROM A LETTER')
            

def isVeteran(csvFile):
    with open(csvFile, 'rb') as f:
        reader = csv.reader(f)
        row_count = sum(1 for row in reader)
    if row_count > 8:
        directory = 'NBA_DATA_CLEAN/'
        shutil.copy(csvFile,directory)

def moveVeterans():
##    for name in os.listdir('NBA_DATA_RAW'):
##        print name
    for name in glob.glob('NBA_DATA_NO_INJURY/*.csv'):
        isVeteran(name)


def yearsInCareer():
    mypath='NBA_DATA_VETERAN/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in onlyfiles:
        with open(mypath+f,'rb') as fi:
            reader = csv.reader(fi)
            years=[]
            seasons=[]
            for row in reader:
                if row[0] not in years:
                    years.append(row[0])
                    seasons.append(row)
            completeFileName = os.path.join('NBA_DATA_VETERAN_CLEAN/', f)
            w = open(completeFileName, 'w+')
            wr = csv.writer(w)
            for r in seasons:
                wr.writerow(r)
            w.close()

def checkForNBACareer():
    mypath='NBA_DATA_VETERANS/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in onlyfiles:
        with open(mypath+f,'rb') as fi:
            reader = csv.reader(fi)
            seasons=[]
            for row in reader:
                if len(row[2])<5:
                    seasons.append(row)
            completeFileName = os.path.join('NBA_DATA_VETERAN_CLEAN/', f)
            w = open(completeFileName, 'w+')
            wr = csv.writer(w)
            for r in seasons:
                wr.writerow(r)
            w.close()
                
        
def isYearAfter1979():
    mypath='NBA_DATA_VETERANS/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in onlyfiles:           
        with open(mypath+f, 'rb') as fi:
            reader = csv.reader(fi)
            seasons=[]
            for row in reader:
                y=row[0]
                if y=='Season':
                    seasons.append(row)
                elif int(y[0:4])>1978:
                    seasons.append(row)
            completeFileName = os.path.join('NBA_DATA_AFTER_1979/', f)
            w = open(completeFileName, 'w+')
            wr = csv.writer(w)
            for r in seasons:
                wr.writerow(r)
            w.close()

def noLockoutYears():
    mypath='NBA_DATA_AFTER_1979/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in onlyfiles:           
        with open(mypath+f, 'rb') as fi:
            reader = csv.reader(fi)
            seasons=[]
            for row in reader:
                y=row[0]
                if y=='Season':
                    seasons.append(row)
                elif int(y[0:4])!=1998 and int(y[0:4])!=2011:
                    seasons.append(row)
            completeFileName = os.path.join('NBA_DATA_NO_LOCKOUT/', f)
            w = open(completeFileName, 'w+')
            wr = csv.writer(w)
            for r in seasons:
                wr.writerow(r)
            w.close()

def noInjuryYears():
    mypath='NBA_DATA_NO_LOCKOUT/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in onlyfiles:           
        with open(mypath+f, 'rb') as fi:
            reader = csv.reader(fi)
            seasons=[]
            for row in reader:
                y=row[5]
                if y=='G':
                    seasons.append(row)
                elif int(y)>41:
                    seasons.append(row)
            completeFileName = os.path.join('NBA_DATA_NO_INJURY/', f)
            w = open(completeFileName, 'w+')
            wr = csv.writer(w)
            for r in seasons:
                wr.writerow(r)
            w.close()
    
