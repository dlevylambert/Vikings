import urllib
import json
import sys
import time
import base64
import random
import math
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
    findDiffs(surveyName, user)
    findPercents(surveyName, user)
    thisSurvey = dict(surveys.find_one({'name': surveyName}))
    percents = thisSurvey['userpercentages'][user]
   
    numQs = len(thisSurvey['useranswers'][user])
    maxDiff = 4.0 * numQs
    matchesData[0] = max(percents[x] for x in percents)
    matchesData[1] = min(percents[x] for x in percents)
    
    matchesData[2] = [x for x in percents if percents[x] == matchesData[0]]
    matchesData[3] = [x for x in percents if percents[x] == matchesData[1]]
    matchesData[4] = []
    #matchesData[4] = bestOverall(sortPercentages(surveyName))
    
    print matchesData
    return matchesData

def sortPercentages(surveyname):
    sorted = {}
    thisSurvey = dict(surveys.find_one({'name':surveyname}))
    unsorted = thisSurvey['userpercentages']
    
    for x in unsorted:
        sorted[x] = [[unsorted[x][y], y] for y in unsorted[x]]
    for x in sorted:
        sorted[x].sort(reverse=True)
    for x in sorted:
        sorted[x] = [y[1] for y in sorted[x]]
    return sorted
                                                

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


#not tested
def getUser(userName):
    userInfo = dict(users.find_one({'user':userName}))
    result = [userInfo[x] for x in userInfo]
    return result[1:]
    
#not tested
def editUserInfo(userName, fieldChange, newValue):
    pass

#overall best, does nto work
def overallBest(ordered):
    final = temp = {}
	temp = defaultdict(lambda:"")
	return recurseOverall(ordered, temp, final)

def recurseOverall(ordered, temp, final):
    if (len(ordered.keys()) == 0):
        return final
    for x in ordered:
        y = temp[x]
        if (temp[x] == ""):
            coupleUp(ordered, temp, x, '')
        elif (ordered[x].index(y) != 0):
            if not coupleUp(ordered, temp, x, y):
				finalize(ordered, temp, final, x, y)
        else:
			finalize(ordered, temp, final, x, y)
            break
    return recurseOverall(ordered, temp, final)
	
def coupleUp(ordered, temp, x, stop):
    for y in ordered[x]:
        if (y == stop):
            return False
        elif (temp[y] == ""):
            if (temp[temp[x]] != ""):
                temp.pop(temp[x], None)
            temp[x] = y
            temp[y] = x
            return True
        else:
            if(ordered[y].index(x) > ordered[y].index(temp[y])):
                temp.pop(temp[y], None)
                temp[x] = y
                temp[y] = x
                return True

def finalize(ordered, temp, final, x, y):
    final[x] = y
    final[y] = x
    removeMatchedUser(ordered, temp, x)
    removeMatchedUser(ordered, temp, y)

def removeMatchedUser(ordered, temp, username):
	ordered.pop(username, None)
	for x in ordered:
		for y in ordered[x]:
			if y == username:
				ordered[x].remove(y)

	for x in temp:
		if temp[x] == username:
			temp[x] = ""

ordered = {'helen':['dina', 'shreya', 'david'],
    	'dina':['david', 'helen', 'shreya'],
		'shreya':['helen', 'david', 'dina'],
		'david':['shreya', 'dina', 'helen']
		}
print overallBest(ordered)

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
