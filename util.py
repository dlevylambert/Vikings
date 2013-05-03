import urllib
import json
import sys
import time
import base64
import random
import math
import copy
from pymongo import Connection
from gridfs import GridFS
from collections import defaultdict

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
    print allAnswers
    return True

def createUser(user,password,age,realname,gender,hobbies):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp, "age": age, "realname":realname, "gender":gender, "hobbies": hobbies}
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

def deleteSurvey(name):
    surveys.remove({"name": name})
    return True

def findDiffs(surveyName, user):
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    allUsers = thisSurvey['useranswers']
    thisUser = allUsers[user]
    thisSurvey['userdifferences'][user] = {}

    for x in allUsers:

        if x != user:
            diffs = [math.fabs(ord(allUsers[x][i]) - ord(thisUser[i])) for i in range(0, len(thisUser))]
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
    print thisSurvey
    for x in thisSurvey['useranswers']:
        findDiffs(surveyName, x)
        findPercents(surveyName, x)
    percents = thisSurvey['userpercentages'][user]

    print thisSurvey

    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    matchesData[0] = max(percents[x] for x in percents)
    matchesData[1] = min(percents[x] for x in percents)
    
    matchesData[2] = [x for x in percents if percents[x] == matchesData[0]]
    matchesData[3] = [x for x in percents if percents[x] == matchesData[1]]
    matchesData[4] = tracePaths(surveyName, user)
    
    print matchesData
    return matchesData


def tracePaths(surveyname, username):
    thisSurvey = dict(surveys.find_one({'name':surveyname}))
    allPercents = thisSurvey['userpercentages']
    allPaths = []
    allMatches = []
    recursePaths(username, allPercents, 0, {}, allPaths, allMatches)
    bestPath = max(allPaths)
    bestMatches = [allMatches[i] for i in range(0, len(allPaths)) if allPaths[i] == bestPath ]
    print bestMatches
    return [x[username] for x in bestMatches]
	
def recursePaths(username, allPers, sum, matches, allPaths, allMatches):
    if (len(allPers.keys()) < 2):
        allPaths.append(sum)
        allMatches.append(matches)
        return
    if sum == 0:
        currUser = username
    else:
        currUser = allPers.keys()[0]
    for x in allPers[currUser]:
        ap = copy.deepcopy(allPers)
        ap.pop(currUser, None)
        ap.pop(x, None)
        for y in ap:
            ap[y].pop(currUser, None)
            ap[y].pop(x, None)
			
        m = copy.deepcopy(matches)
        m[currUser] = x
        m[x] = currUser
		
        recursePaths(username, ap, sum + allPers[currUser][x], m, allPaths, allMatches)


def getSurveyQs(surveyName):
    survey = dict(surveys.find_one({'name':surveyName}))
    qs = survey['questions']
    return qs

#not tested
def getSurveyNames():
    names = []
    for surv in surveys.find({"type": "survey"}):
        names.append(surv["name"])
    return names


def getUser(userName):
    userInfo = dict(users.find_one({'user':userName}))
    result = [userInfo[x] for x in userInfo]
    return result[1:]

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
#    deleteSurvey("prom date")
