import urllib
import json
import sys
import time
import base64
import random
import math
from pymongo import Connection
from gridfs import GridFS

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.VikingsUsers
surveys = db.VikingsSurveys
#pics = db.VikingsPics
#fs = GridFS(db, 'pics')

"""
Function: takeSurvey(string user, string survey, int[] ans)
Purpose: save the user's answers for the survey
Return: Boolean

Last Edited: 4/21/13 at 16:06 by Helen Nie
Tested: yes
"""
def takeSurvey(surveyname, user, ans):
    surv = surveys.find_one({"name": surveyname})
    surv["useranswers"][user] = ans
    return true

def createUser(user,password):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp}
    users.insert(newuser)
    return True

def checkUserPass(user,password):
    encpass = base64.b64encode(password)
    tmp = users.find_one({"user" : user})
    if tmp == None:
        return 0
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def createSurvey(password,name):
    if surveys.find_one({"name":name}) != None:
        return False
    newsurvey = {"name" : name, "questions" : [], "useranswers": {}, "userdifferences": {}, "userpercentage": {}} 
    surveys.insert(newsurvey)
    return True

def findDiffs(surveyName, user):
    surveys[surveyName]['userdifferences'][user] = {}
    sumDiffs = surveys[surveyName]['userdifferences'][user]
    allUsers = surveys[surveyName]['useranswers']
    thisUser = allUsers[user]

    for x in allUsers:
        if x != user:
            diffs = [math.fabs(allUsers[x][i] - thisUser[i]) for i in range(0, len(thisUser))]
            sumDiffs[x] = sum(diffs)
    return True    

def findPercents(surveyName, user):
    surveys[surveyName]['userpercentages'][user] = {}
    percents = surveys[surveyName]['userpercentages'][user]
    sumDiffs = surveys[surveyName]['userdifferences'][user]
    
    numQs = len(surveys[surveyName]['useranswers'][user])
    maxDiff = 4.0 * numQs
    
    for x in sumDiffs:
        percents[x] = 100 - (sumDiffs[x] / maxDiff) * 100
    return True

def match(surveyName, user):
    matchesData = {}
    percents = surveys[surveyName]['userpercentages'][user]
    
    numQs = len(surveys[surveyName]['useranswers'][user])
    maxDiff = 4.0 * numQs
    matchesData['maxPercent'] = max(percents[x] for x in percents)
    matchesData['minPercent'] = min(percents[x] for x in percents)
    
    matchesData['best'] = [x for x in percents if percents[x] == matchesData['maxPercent']]
    matchesData['worst'] = [x for x in percents if percents[x] == matchesData['minPercent']]
    matchesData['overallBest'] = []
    
    return matchesData
    

#if __name__ == "__main__":
#    createUser("Dina", "hello")
#    print checkUserPass("Dina", "hello")
#    print checkUserPass("Dina", "he")
#    createSurvey("hello", "test")
#    takeSurvey("Dina", "test", [1, 1, 1, 1, 1]

#    #testing algorithm
#    surveys = {'test':{'useranswers':{'Helen':[2, 2, 2], 'Shreya':[2, 2, 2], 'Dina':[2, 2, 2], 'David':[5, 5, 5]},
#                   'userdifferences':{'Helen': {'Shreya': 0.0, 'Dina': 0.0, 'David': 9.0}},
#                   'userpercentages':{'Helen': {'Shreya': 100.0, 'Dina': 100.0, 'David': 25.0}}}}

#    findDiffs('test', 'Helen')
#    findPercents('test', 'Helen')    			   
#    print surveys['test']
#    print match('test', 'Helen');
