import urllib
import json
import sys
import time
import base64
import random
import math
from pymongo import Connection
from gridfs import GridFS

connection = Connection('mongo2.stuycs.org')
db = connection.admin
res = db.authenticate('ml7','ml7')
db = connection['z-pd6']
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
    surv = surveys.find_one({'name': surveyname})
    allAnswers = dict(surv)
    allAnswers['useranswers'].update({user:ans})
    surveys.update(
        {'name':surveyname},
        allAnswers)
    return True

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

def createSurvey(name, questions):
    if surveys.find_one({"name":name}) != None:
        return False
    surveys.insert({"type": "survey", "name" : name, "questions" : questions, "useranswers": {}, "userdifferences": {}, "userpercentages": {}})
    return True

def findDiffs(surveyName, user):
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    allUsers = thisSurvey['useranswers']
    thisUser = allUsers[user]
    thisSurvey['userdifferences'][user] = {}

    for x in allUsers:
        if x != user:
            diffs = [math.fabs(allUsers[x][i] - thisUser[i]) for i in range(0, len(thisUser))]
            thisSurvey['userdifferences'][user].update({x:sum(diffs)})
            surveys.update(
                {'name':surveyName},
                thisSurvey)
    return True    

def findPercents(surveyName, user):
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    sumDiffs = thisSurvey['userdifferences'][user]
    thisSurvey['userpercentages'][user] = {}    

    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    
    for x in sumDiffs:
        percent = 100 - (sumDiffs[x] / maxDiff) * 100
        thisSurvey['userpercentages'][user].update({x:percent})
        surveys.update(
            {'name':surveyName},
            thisSurvey)
    return True

def match(surveyName, user):
    matchesData = {}
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    percents = thisSurvey['userpercentages'][user]
    
    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    matchesData['maxPercent'] = max(percents[x] for x in percents)
    matchesData['minPercent'] = min(percents[x] for x in percents)
    
    matchesData['best'] = [x for x in percents if percents[x] == matchesData['maxPercent']]
    matchesData['worst'] = [x for x in percents if percents[x] == matchesData['minPercent']]
    matchesData['overallBest'] = []
    
    return matchesData

def getSurveyQs(surveyName):
    return surveys.find_one({'name':surveyName})

#not tested
def getSurveyNames():
    names = []
    print surveys.find_one({"type": "survey"})
    for surv in surveys.find({"type": "survey"}):
        print surv
        names.append(surv["name"])
    return names


#not tested
def getUserInfo(userName):
    return users.find_one({'name':userName})

#not tested
def editUserInfo(userName, fieldChange, newValue):
    pass
    
#if __name__ == "__main__":
#    createUser("Dina", "hello")
#    print checkUserPass("Dina", "hello")
#    print checkUserPass("Dina", "he")
#    createSurvey("test", [])
#    createSurvey("test2", [])
#    print getSurveyNames()
#    takeSurvey("test", "Helen", [1, 1, 1, 1, 1])
#    takeSurvey("test", "Dina", [1, 1, 1, 1, 1])
#    takeSurvey("test", "Shreya",  [1, 1, 1, 1, 1])
#    takeSurvey("test", "David",  [2, 2, 2, 2, 2])

#    #testing algorithm
#    findDiffs('test', 'Helen')
#    findPercents('test', 'Helen')
#    match('test', 'Helen')
